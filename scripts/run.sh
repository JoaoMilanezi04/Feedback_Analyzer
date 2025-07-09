#!/bin/bash

# Script para executar o Feedback Analyzer
# Autor: João Milanezi

echo "🚀 Iniciando Feedback Analyzer..."
echo "=================================="

# Ir para a pasta raiz do projeto
cd "$(dirname "$0")/.."

# Verificar se estamos na pasta correta
if [ ! -f "main.py" ]; then
    echo "❌ Erro: main.py não encontrado"
    echo "💡 Verifique se você está na pasta correta"
    exit 1
fi

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    echo "🔧 Ativando ambiente virtual..."
    source venv/bin/activate
fi

# Verificar se config.ini existe
if [ ! -f "config.ini" ]; then
    echo "❌ Arquivo config.ini não encontrado!"
    echo "💡 Execute primeiro: ./scripts/install.sh"
    exit 1
fi

# Executar o programa principal
echo "📊 Executando análise de feedback..."
python3 main.py

echo "✅ Execução concluída!"
