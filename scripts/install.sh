#!/bin/bash

# Script de instalação do Feedback Analyzer
# Autor: João Milanezi

echo "� Instalação do Feedback Analyzer"
echo "=================================="

# Ir para a pasta raiz do projeto
cd "$(dirname "$0")/.."

# Verificar se Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "💡 Instale o Python 3 antes de continuar"
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "🏗️  Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo "📦 Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "� Instalando dependências..."
pip install -r requirements.txt

# Criar config.ini se não existir
if [ ! -f "config.ini" ]; then
    echo "📄 Criando arquivo de configuração..."
    cat > config.ini << EOF
[GEMINI]
API_KEY = tu_api_key_aqui
EOF
    echo "⚠️  IMPORTANTE: Configure sua API key do Google Gemini em config.ini"
fi

# Verificar se existem arquivos de exemplo
if [ ! -f "dados/comentarios.txt" ] && [ ! -f "dados/feedback.csv" ]; then
    echo "� Criando arquivos de exemplo na pasta dados/..."
    
    # Criar comentarios.txt de exemplo
    cat > dados/comentarios.txt << EOF
O produto é excelente, muito bem feito!
Entrega demorou muito, não recomendo.
Qualidade boa mas preço alto.
Atendimento péssimo, ninguém responde.
Produto chegou rápido e bem embalado.
EOF

    # Criar feedback.csv de exemplo
    cat > dados/feedback.csv << EOF
data,fonte,comentario
2024-01-15,Amazon,Produto de ótima qualidade
2024-01-16,MercadoLivre,Entrega foi rápida
2024-01-17,Site Próprio,Atendimento poderia melhorar
2024-01-18,Amazon,Recomendo a todos
2024-01-19,Google Play,App funciona bem
EOF
fi

echo ""
echo "✅ Instalação concluída com sucesso!"
echo ""
echo "� Para executar: ./scripts/run.sh"
echo "📋 Para dashboard web: python3 src/feedback_analyzer/dashboard.py"
echo ""
echo "⚠️  NÃO ESQUEÇA:"
echo "   1. Configure sua API key do Google Gemini em config.ini"
echo "   2. Coloque seus dados em dados/comentarios.txt ou dados/feedback.csv"
echo ""
