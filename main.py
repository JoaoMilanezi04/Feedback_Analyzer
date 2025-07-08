import pandas as pd
from tqdm import tqdm
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import asyncio

from gemini_processor import analisar_comentario_individual, gerar_resumo_executivo, configurar_ia

def processar_comentarios_otimizado(comentarios, max_workers=8):
    print(f"[INFO] Processando {len(comentarios)} comentários com {max_workers} workers...")
    
    resultados = [None] * len(comentarios)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(analisar_comentario_individual, comentario): i 
            for i, comentario in enumerate(comentarios)
        }
        
        with tqdm(total=len(comentarios), desc="Processando") as pbar:
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    resultado = future.result(timeout=15)
                    resultados[index] = resultado
                except Exception as e:
                    resultados[index] = {
                        "sentimento": "Erro",
                        "categoria": "Erro", 
                        "resumo_curto": "Erro de processamento."
                    }
                pbar.update(1)
    
    return resultados

def main():
    print("🚀 Iniciando processamento otimizado de comentários...")
    
    if not configurar_ia():
        print("❌ Erro ao configurar a IA.")
        sys.exit(1)

    try:
        df = pd.read_csv('feedback.csv')
        print(f"✅ Carregados {len(df)} comentários.")
    except FileNotFoundError:
        print("❌ Arquivo 'feedback.csv' não encontrado.")
        sys.exit(1)

    print("🔄 Analisando comentários...")
    inicio = time.time()
    
    # Otimizado: mais workers e timeout menor
    resultados = processar_comentarios_otimizado(df['comentario'].tolist(), max_workers=10)
    
    fim = time.time()
    tempo_total = fim - inicio
    velocidade = len(df) / tempo_total
    print(f"⚡ Análise concluída em {tempo_total:.1f}s ({velocidade:.1f} comentários/seg)")

    # Filtrar erros para estatísticas mais precisas
    resultados_validos = [r for r in resultados if r['sentimento'] != 'Erro']
    print(f"📊 {len(resultados_validos)}/{len(resultados)} comentários processados com sucesso")
    
    if not resultados_validos:
        print("❌ Nenhum comentário foi processado com sucesso.")
        sys.exit(1)

    contagem_sentimentos = pd.Series([r['sentimento'] for r in resultados_validos]).value_counts()    
    contagem_categorias = pd.Series([r['categoria'] for r in resultados_validos]).value_counts()

    texto_estatisticas = "## 📊 Análise Quantitativa\n\n"
    texto_estatisticas += "### Distribuição de Sentimento:\n"
    texto_estatisticas += contagem_sentimentos.to_string() + "\n\n"
    texto_estatisticas += "### Tópicos Mais Comuns:\n"
    texto_estatisticas += contagem_categorias.to_string()

    print("🤖 Gerando resumo executivo...")
    resumo_executivo = gerar_resumo_executivo(texto_estatisticas)

    print("💾 Criando relatório...")
    nome_arquivo = f"relatorio_feedback_{int(time.time())}.md"
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write("# 📋 Relatório de Análise de Feedback\n\n")
            f.write(f"**Processado em:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Tempo total:** {tempo_total:.1f} segundos\n")
            f.write(f"**Velocidade:** {velocidade:.1f} comentários/seg\n\n")
            f.write("## 🚀 Resumo Executivo\n")
            f.write(resumo_executivo)
            f.write("\n\n---\n\n")
            f.write(texto_estatisticas)
            f.write("\n\n---\n\n")
            f.write("## 💬 Comentários Processados\n\n")
            
            for i, (idx, row) in enumerate(df.iterrows()):
                if i < len(resultados):
                    resultado = resultados[i]
                    status = "✅" if resultado['sentimento'] != 'Erro' else "❌"
                    f.write(f"### {status} Comentário {i+1}\n")
                    f.write(f"**Data:** {row['fecha']}\n")
                    f.write(f"**Fonte:** {row['fuente']}\n")
                    f.write(f"**Texto:** {row['comentario']}\n")
                    f.write(f"**Sentimento:** {resultado['sentimento']}\n")
                    f.write(f"**Categoria:** {resultado['categoria']}\n")
                    f.write(f"**Resumo:** {resultado['resumo_curto']}\n\n")

        print(f"✅ Relatório salvo: {nome_arquivo}")
    except Exception as e:
        print(f"❌ Erro ao criar relatório: {e}")
        sys.exit(1)
    
if __name__ == "__main__":
    main()