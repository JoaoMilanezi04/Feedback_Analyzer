# Feedback Analyzer

Analizador de feedback de clientes usando IA de Google Gemini.

## Configuración

1. Copia el archivo de ejemplo:
   ```bash
   cp config.ini.example config.ini
   ```

2. Edita `config.ini` y coloca tu API key de Google Gemini:
   ```ini
   [GEMINI]
   API_KEY = tu_api_key_real_aqui
   ```

3. Instala las dependencias:
   ```bash
   pip install google-generativeai pandas
   ```

## Uso

```python
from gemini_processor import configurar_ia, analizar_comentario_individual

# Configurar la IA
if configurar_ia():
    # Analizar un comentario
    resultado = analizar_comentario_individual("Me encanta la app!")
    print(resultado)
```

## Archivos

- `gemini_processor.py` - Funciones para procesar feedback con IA
- `feedback.csv` - Datos de ejemplo
- `config.ini.example` - Plantilla de configuración
- `main.py` - Archivo principal (por implementar)

## Seguridad

⚠️ **IMPORTANTE**: Nunca subas tu `config.ini` real al repositorio. El archivo está excluido en `.gitignore`.
