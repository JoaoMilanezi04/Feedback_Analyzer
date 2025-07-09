import google.generativeai as genai
import json
import configparser
import time
import os


def configurar_ia():
    try:
        config = configparser.ConfigParser()
        
        # Tentar carregar config.ini da pasta raiz do projeto
        config_paths = [
            'config.ini',  # Pasta atual
            '../../config.ini',  # Subindo duas pastas (de src/feedback_analyzer)
            os.path.join(os.path.dirname(__file__), '../../config.ini')  # Caminho absoluto
        ]
        
        config_loaded = False
        for config_path in config_paths:
            if os.path.exists(config_path):
                config.read(config_path)
                config_loaded = True
                break
        
        if not config_loaded:
            raise ValueError("Arquivo config.ini não encontrado")
        
        api_key = config.get('GEMINI', 'API_KEY')
        if not api_key or api_key == 'tu_api_key_aqui':
            raise ValueError("A API key não está configurada no config.ini")
        
        genai.configure(api_key=api_key)
        print("[INFO] Configuração da IA concluída com sucesso.")
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao configurar a IA: {e}")
        return False

def analisar_comentario_individual(comentario: str) -> dict:
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Analise este comentário de cliente e responda APENAS com JSON válido:

    {{
      "sentimento": "Positivo" ou "Negativo" ou "Neutro",
      "categoria": "Bug" ou "Sugestão" ou "UI/UX" ou "Suporte",
      "resumo_curto": "resumo em uma frase"
    }}

    Comentário: "{comentario}"
    """

    for tentativa in range(3):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=100
                )
            )
            texto = response.text.strip()
            
            # Limpar resposta mais agressivamente
            if "```" in texto:
                texto = texto.split("```")[1] if "```json" in texto else texto.split("```")[0]
            
            # Remover texto antes e depois do JSON
            inicio = texto.find('{')
            fim = texto.rfind('}') + 1
            if inicio != -1 and fim != 0:
                texto = texto[inicio:fim]
            
            resultado = json.loads(texto)
            
            # Validar campos obrigatórios
            if all(key in resultado for key in ['sentimento', 'categoria', 'resumo_curto']):
                return resultado
            else:
                raise ValueError("Campos obrigatórios ausentes")
            
        except Exception as e:
            if tentativa < 2:
                time.sleep(0.5)
                continue
            else:
                print(f"[ERRO] Falha ao processar: '{comentario[:30]}...' - {e}")
                return {
                    "sentimento": "Erro",
                    "categoria": "Erro",
                    "resumo_curto": "Erro no processamento."
                }

def gerar_resumo_executivo(estatisticas: str) -> str:
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Como Analista de Produto, escreva um resumo executivo de 3-4 frases baseado nas estatísticas:
    
    {estatisticas}
    
    Destaque a tendência principal e problema mais urgente.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Erro ao gerar resumo executivo."