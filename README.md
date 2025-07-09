# 🚀 Analisador de Feedback para Produtos Web

Sistema completo para extrair e analisar comentários de produtos web usando IA.

## ✨ Funcionalidades

- 🌐 **Extração automática** de comentários de URLs de produtos
- 🧠 **Análise por IA** usando Google Gemini
- 📊 **Relatórios detalhados** com insights executivos
- ⚡ **Processamento paralelo** super rápido
- 📁 **Múltiplos formatos** de entrada (URL, CSV, TXT, JSON)

## 🎯 Plataformas Suportadas

- **Amazon** (produtos)
- **MercadoLivre** (produtos) ✅ Testado
- **Google Play** (apps)
- **App Store** (apps)
- **Sites genéricos** (com comentários)

## 🚀 Como Usar

### 1. Configuração

```bash
# Ativar ambiente virtual
source venv/bin/activate  # ou venv/Scripts/activate no Windows

# Instalar dependências (já instaladas)
pip install selenium webdriver-manager beautifulsoup4 requests google-generativeai
```

### 2. Configurar API Gemini

Edite `config.ini`:
```ini
[GEMINI]
API_KEY = sua_api_key_aqui
```

### 3. Executar

```bash
# Análise completa (com IA)
python main.py

# Demo (apenas extração, sem IA)
python demo_extrator.py
```

## 📖 Exemplo de Uso

1. **Execute:** `python main.py`
2. **Escolha:** `1. 🌐 Extrair de URL`
3. **Cole a URL** do produto (ex: MercadoLivre, Amazon)
4. **Aguarde** a extração e análise
5. **Veja o relatório** gerado automaticamente

## ⚠️ Limitações da API Gratuita

A API gratuita do Gemini tem limite de **50 requests/dia**. Se atingir o limite:

### Soluções:
1. **Aguarde 24h** para renovar a cota
2. **Use o demo** para apenas extrair comentários
3. **Upgrade** para plano pago do Gemini
4. **Processe em lotes** menores

## 📊 O que Você Recebe

- **Sentimentos:** Positivo/Negativo/Neutro
- **Categorias:** Bug/Sugerência/UI-UX/Suporte
- **Resumo executivo** gerado por IA
- **Relatório Markdown** completo
- **Estatísticas** detalhadas

