import google.generativeai as genai
import json
import os
import configparser


def configurar_ia():
    """Configura la API de Gemini usando la API key del archivo config.ini."""
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        api_key = config.get('GEMINI', 'API_KEY')
        if not api_key or api_key == 'tu_api_key_aqui':
            raise ValueError("La API key no está configurada en config.ini")
        
        genai.configure(api_key=api_key)
        print("[INFO] Configuración de la IA completada con éxito.")
        return True
    except Exception as e:
        print(f"[ERROR] Fallo al configurar la IA: {e}")
        print("Asegúrate de haber configurado tu API key en config.ini")
        return False

def analizar_comentario_individual(comentario: str) -> dict:
    """
    Analiza un único comentario de cliente usando la API de Gemini.
    
    Args:
        comentario: El texto del comentario a analizar.
    
    Returns:
        Diccionario con 'sentimiento', 'categoria' y 'resumen_corto'.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    Analiza el siguiente comentario de un cliente. Devuelve tu respuesta únicamente en formato JSON válido con las claves "sentimiento", "categoria" y "resumen_corto".

    - La clave "sentimiento" debe tener uno de los siguientes valores: 'Positivo', 'Negativo' o 'Neutro'.
    - La clave "categoria" debe tener uno de los siguientes valores: 'Bug', 'Sugerencia', 'UI/UX' o 'Soporte'.
    - La clave "resumen_corto" debe ser un resumen de una sola frase del punto principal del comentario.

    No incluyas ```json ni ``` al principio o al final de tu respuesta.

    Comentario: "{comentario}"
    """

    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
        
    except Exception as e:
        print(f"\n[ERROR] No se pudo analizar el comentario: '{comentario[:50]}...'")
        print(f"  Razón: {e}")
        return {
            "sentimiento": "Error",
            "categoria": "Error",
            "resumen_corto": "No se pudo analizar el comentario."
        }

def generar_resumen_ejecutivo(estadisticas: str) -> str:
    """
    Genera un resumen ejecutivo basado en las estadísticas agregadas.
    
    Args:
        estadisticas: String formateado con las estadísticas del feedback.
    
    Returns:
        Párrafo con el resumen ejecutivo.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Actúa como un Analista de Producto senior. Basado en las siguientes estadísticas y resúmenes de feedback de clientes, escribe un resumen ejecutivo de 3 a 5 frases.
    Destaca la tendencia más importante y el problema más urgente a resolver para el equipo de producto.

    Estadísticas:
    {estadisticas}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"\n[ERROR] No se pudo generar el resumen ejecutivo: {e}")
        return "No se pudo generar el resumen ejecutivo."
