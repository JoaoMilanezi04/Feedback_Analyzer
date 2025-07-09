"""
Feedback Analyzer - Sistema de Análise de Feedback de Clientes

Este módulo contém as funcionalidades principais para:
- Extração de comentários de URLs e arquivos locais
- Análise de sentimento com Google Gemini
- Geração de relatórios executivos
- Dashboard web para visualização

Versão: 1.0.0
Autor: João Milanezi
"""

__version__ = "1.0.0"
__author__ = "João Milanezi"

# Importações condicionais para evitar erros se os módulos não estiverem prontos
try:
    from .gemini_processor import analisar_comentario_individual, gerar_resumo_executivo, configurar_ia
    from .web_extractor import extrair_comentarios_de_url
    
    __all__ = [
        'analisar_comentario_individual', 
        'gerar_resumo_executivo', 
        'configurar_ia',
        'extrair_comentarios_de_url'
    ]
except ImportError:
    # Se houver problemas com dependências, apenas expor metadados
    __all__ = []
