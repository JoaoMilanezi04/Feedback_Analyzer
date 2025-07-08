import google.generativeai as genai
import json
import configparser
import time


def configurar_ia():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        
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
    Analise o seguinte comentário de um cliente. Retorne apenas em formato JSON válido com as chaves "sentimento", "categoria" e "resumo_curto".

    - "sentimento": 'Positivo', 'Negativo' ou 'Neutro'
    - "categoria": 'Bug', 'Sugestão', 'UI/UX' ou 'Suporte'  
    - "resumo_curto": uma frase resumindo o ponto principal

    Comentário: "{comentario}"
    """

    for tentativa in range(3):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=150
                )
            )
            texto_limpo = response.text.strip().replace("```json", "").replace("```", "")
            return json.loads(texto_limpo)
            
        except Exception as e:
            if tentativa < 2:
                time.sleep(0.3)
                continue
            else:
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