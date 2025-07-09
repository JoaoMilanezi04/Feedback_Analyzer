import pandas as pd
from tqdm import tqdm
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json
import re

from gemini_processor import analisar_comentario_individual, gerar_resumo_executivo, configurar_ia
from web_extractor import extrair_comentarios_de_url

def carregar_comentarios():
    """Carrega comentários de diferentes fontes disponíveis."""
    print("📁 Escolha a fonte dos comentários:")
    print("1. 🌐 Extrair de URL (Amazon, MercadoLivre, Google Play, etc.)")
    print("2. 📄 Carregar de arquivo (CSV, TXT, JSON)")
    print("3. ✍️  Inserir manualmente")
    
    opcao = input("\nEscolha uma opção (1/2/3): ").strip()
    
    if opcao == "1":
        return extrair_de_url()
    elif opcao == "2":
        return carregar_de_arquivo()
    elif opcao == "3":
        return entrada_manual()
    else:
        print("❌ Opção inválida.")
        sys.exit(1)

def extrair_de_url():
    """Extrai comentários de uma URL de produto."""
    print("\n🌐 EXTRAÇÃO DE COMENTÁRIOS POR URL")
    print("=" * 40)
    print("Plataformas suportadas:")
    print("• Amazon (produtos)")
    print("• MercadoLivre (produtos)")
    print("• Google Play (apps)")
    print("• App Store (apps)")
    print("• Sites genéricos")
    print("=" * 40)
    
    url = input("\n🔗 Cole a URL do produto: ").strip()
    
    if not url:
        print("❌ URL não pode estar vazia.")
        sys.exit(1)
    
    # Validar se é uma URL válida
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(url):
        print("❌ URL inválida. Deve começar com http:// ou https://")
        sys.exit(1)
    
    print(f"\n🚀 Extraindo comentários de: {url}")
    print("⏳ Isso pode levar alguns minutos...")
    
    try:
        df = extrair_comentarios_de_url(url)
        
        if df.empty:
            print("\n❌ Nenhum comentário foi encontrado nesta URL.")
            print("💡 Dicas:")
            print("   • Verifique se a URL está correta")
            print("   • Alguns sites podem bloquear extração automática")
            print("   • Tente uma URL direta para a página de reviews/comentários")
            sys.exit(1)
        
        return df
        
    except Exception as e:
        print(f"\n❌ Erro ao extrair comentários: {e}")
        print("💡 Tente:")
        print("   • Verificar sua conexão com a internet")
        print("   • Usar uma URL diferente")
        print("   • Carregar comentários de arquivo")
        sys.exit(1)

def carregar_de_arquivo():
    """Carrega comentários de arquivos locais."""
    print("\n📄 CARREGAMENTO DE ARQUIVO")
    print("=" * 30)
    
    # Verificar diferentes formatos de arquivo
    arquivos_possiveis = [
        'feedback.csv',
        'comentarios.csv', 
        'reviews.csv',
        'avaliações.csv',
        'comentarios.txt',
        'feedback.json'
    ]
    
    for arquivo in arquivos_possiveis:
        if os.path.exists(arquivo):
            print(f"✅ Arquivo encontrado: {arquivo}")
            return carregar_arquivo(arquivo)
    
    print("❌ Nenhum arquivo encontrado.")
    print("📝 Arquivos suportados:")
    for arquivo in arquivos_possiveis:
        print(f"   • {arquivo}")
    
    # Permitir especificar arquivo manualmente
    arquivo_manual = input("\n📂 Digite o caminho do arquivo (ou Enter para sair): ").strip()
    
    if arquivo_manual and os.path.exists(arquivo_manual):
        return carregar_arquivo(arquivo_manual)
    else:
        print("❌ Arquivo não encontrado.")
        sys.exit(1)

def carregar_arquivo(nome_arquivo):
    """Carrega comentários de diferentes tipos de arquivo."""
    try:
        extensao = nome_arquivo.split('.')[-1].lower()
        
        if extensao == 'csv':
            df = pd.read_csv(nome_arquivo)
            # Verificar se tem as colunas necessárias
            if 'comentario' not in df.columns:
                # Tentar encontrar coluna de comentários com nomes alternativos
                colunas_comentario = ['review', 'text', 'feedback', 'comment', 'mensaje', 'texto']
                for col in colunas_comentario:
                    if col in df.columns:
                        df['comentario'] = df[col]
                        break
                else:
                    print("❌ Arquivo CSV deve ter uma coluna 'comentario' ou similar.")
                    sys.exit(1)
            
            # Adicionar colunas padrão se não existirem
            if 'data' not in df.columns:
                df['data'] = pd.Timestamp.now().strftime('%Y-%m-%d')
            if 'fonte' not in df.columns:
                df['fonte'] = 'Produto Web'
                
        elif extensao == 'txt':
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            
            comentarios = [linha.strip() for linha in linhas if linha.strip()]
            df = pd.DataFrame({
                'data': [pd.Timestamp.now().strftime('%Y-%m-%d')] * len(comentarios),
                'fonte': ['Produto Web'] * len(comentarios),
                'comentario': comentarios
            })
            
        elif extensao == 'json':
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            if isinstance(dados, list):
                # Lista de comentários
                if isinstance(dados[0], str):
                    comentarios = dados
                else:
                    comentarios = [item.get('comentario', item.get('text', str(item))) for item in dados]
            else:
                comentarios = [str(dados)]
                
            df = pd.DataFrame({
                'data': [pd.Timestamp.now().strftime('%Y-%m-%d')] * len(comentarios),
                'fonte': ['Produto Web'] * len(comentarios),
                'comentario': comentarios
            })
        
        print(f"✅ Carregados {len(df)} comentários de {nome_arquivo}")
        return df
        
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo {nome_arquivo}: {e}")
        sys.exit(1)

def entrada_manual():
    """Permite entrada manual de comentários."""
    print("\n📝 Inserção manual de comentários")
    print("Digite os comentários (linha por linha). Digite 'FIM' para terminar:")
    
    comentarios = []
    while True:
        comentario = input(f"Comentário {len(comentarios) + 1}: ").strip()
        if comentario.upper() == 'FIM':
            break
        if comentario:
            comentarios.append(comentario)
    
    if not comentarios:
        print("❌ Nenhum comentário inserido.")
        sys.exit(1)
    
    df = pd.DataFrame({
        'data': [pd.Timestamp.now().strftime('%Y-%m-%d')] * len(comentarios),
        'fonte': ['Entrada Manual'] * len(comentarios),
        'comentario': comentarios
    })
    
    return df

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
    print("🚀 Analisador de Feedback para Produtos Web")
    print("=" * 50)
    print("📊 Analise comentários de qualquer produto da web!")
    print("=" * 50)
    
    if not configurar_ia():
        print("❌ Erro ao configurar a IA.")
        sys.exit(1)

    # Carregar comentários de forma flexível
    df = carregar_comentarios()
    
    if df.empty:
        print("❌ Nenhum comentário para processar.")
        sys.exit(1)
    
    # Mostrar informações sobre os dados carregados
    print(f"\n📊 Resumo dos dados:")
    print(f"   • Total de comentários: {len(df)}")
    print(f"   • Fontes: {', '.join(df['fonte'].unique())}")
    if 'data' in df.columns:
        print(f"   • Período: {df['data'].min()} a {df['data'].max()}")
    
    # Permitir ao usuário configurar o produto
    nome_produto = input("\n🏷️  Nome do produto/serviço: ").strip()
    if not nome_produto:
        nome_produto = "Produto Analisado"

    print(f"\n🔄 Analisando feedback de '{nome_produto}'...")
    print("⚡ Usando processamento paralelo otimizado...")
    inicio = time.time()
    
    # Otimizado: mais workers e timeout menor
    resultados = processar_comentarios_otimizado(df['comentario'].tolist(), max_workers=10)
    
    fim = time.time()
    tempo_total = fim - inicio
    velocidade = len(df) / tempo_total if tempo_total > 0 else 0
    print(f"⚡ Análise concluída em {tempo_total:.1f}s ({velocidade:.1f} comentários/seg)")

    # Filtrar erros para estatísticas mais precisas
    resultados_validos = [r for r in resultados if r['sentimento'] != 'Erro']
    print(f"📊 {len(resultados_validos)}/{len(resultados)} comentários processados com sucesso")
    
    if not resultados_validos:
        print("❌ Nenhum comentário foi processado com sucesso.")
        print("💡 Tente novamente ou verifique sua conexão com a API Gemini.")
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
    nome_arquivo = f"relatorio_{nome_produto.replace(' ', '_').lower()}_{int(time.time())}.md"
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(f"# 📋 Análise de Feedback - {nome_produto}\n\n")
            f.write(f"**Produto/Serviço:** {nome_produto}\n")
            f.write(f"**Processado em:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total de comentários:** {len(df)}\n")
            f.write(f"**Comentários válidos:** {len(resultados_validos)}\n")
            f.write(f"**Tempo de processamento:** {tempo_total:.1f} segundos\n")
            f.write(f"**Velocidade:** {velocidade:.1f} comentários/seg\n\n")
            f.write("## 🚀 Resumo Executivo\n")
            f.write(resumo_executivo)
            f.write("\n\n---\n\n")
            f.write(texto_estatisticas)
            f.write("\n\n---\n\n")
            f.write("## 💬 Comentários Analisados\n\n")
            
            for i, (idx, row) in enumerate(df.iterrows()):
                if i < len(resultados):
                    resultado = resultados[i]
                    status = "✅" if resultado['sentimento'] != 'Erro' else "❌"
                    f.write(f"### {status} Comentário {i+1}\n")
                    f.write(f"**Data:** {row['data']}\n")
                    f.write(f"**Fonte:** {row['fonte']}\n")
                    f.write(f"**Texto:** _{row['comentario']}_\n")
                    f.write(f"**Sentimento:** {resultado['sentimento']}\n")
                    f.write(f"**Categoria:** {resultado['categoria']}\n")
                    f.write(f"**Resumo:** {resultado['resumo_curto']}\n\n")

        print(f"✅ Relatório salvo: {nome_arquivo}")
        
        # Mostrar resumo no terminal
        print("\n" + "="*50)
        print("📊 RESUMO RÁPIDO")
        print("="*50)
        print(f"Produto: {nome_produto}")
        print(f"Total processado: {len(resultados_validos)}/{len(df)} comentários")
        print("\nSentimentos:")
        for sentimento, count in contagem_sentimentos.items():
            print(f"  • {sentimento}: {count}")
        print("\nCategorias:")
        for categoria, count in contagem_categorias.items():
            print(f"  • {categoria}: {count}")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Erro ao criar relatório: {e}")
        sys.exit(1)
    
if __name__ == "__main__":
    main()