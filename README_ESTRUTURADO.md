# 🚀 Feedback Analyzer - Sistema de Análise de Feedback de Clientes

Sistema inteligente para extrair e analisar comentários de produtos web usando Google Gemini AI.

## 📁 Estrutura do Projeto

```
Feedback_Analyzer/
├── 📂 src/                          # Código fonte
│   └── 📂 feedback_analyzer/        # Módulo principal
│       ├── __init__.py              # Inicialização do módulo
│       ├── gemini_processor.py      # Processamento com IA
│       ├── web_extractor.py         # Extração web
│       └── dashboard.py             # Dashboard Streamlit
├── 📂 dados/                        # Arquivos de entrada
│   ├── comentarios.txt              # Exemplo: comentários em texto
│   └── feedback.csv                 # Exemplo: feedback em CSV
├── 📂 relatorios/                   # Relatórios gerados
├── 📂 scripts/                      # Scripts auxiliares
│   ├── install.sh                   # Instalação automatizada
│   ├── run.sh                       # Executar o sistema
│   └── demo_extrator.py             # Demo sem IA
├── 📂 venv/                         # Ambiente virtual Python
├── main.py                          # Ponto de entrada principal
├── config.ini                       # Configuração da API
├── requirements.txt                 # Dependências Python
└── README.md                        # Este arquivo
```

## 🚀 Instalação Rápida

### 1. Clone ou baixe o projeto
```bash
git clone <repository-url>
cd Feedback_Analyzer
```

### 2. Execute a instalação automatizada
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### 3. Configure sua API key do Google Gemini
```bash
# Edite o arquivo config.ini
[GEMINI]
API_KEY = sua_api_key_aqui
```

### 4. Execute o sistema
```bash
./scripts/run.sh
```

## 📊 Como Usar

### Opção 1: Interface Principal (main.py)
```bash
python3 main.py
```
- Escolha entre URL, arquivo ou entrada manual
- Análise completa com IA
- Relatório executivo automático

### Opção 2: Dashboard Web
```bash
python3 src/feedback_analyzer/dashboard.py
```
- Interface web moderna
- Upload de arquivos
- Visualizações interativas

### Opção 3: Demo sem IA
```bash
python3 scripts/demo_extrator.py
```
- Extração pura (sem consumir API)
- Útil para testes

## 📄 Formatos Suportados

### Fontes de Dados
- **URLs**: Amazon, MercadoLivre, Google Play, App Store
- **Arquivos CSV**: Com coluna 'comentario' ou similar
- **Arquivos TXT**: Um comentário por linha
- **Arquivos JSON**: Lista de comentários
- **Entrada Manual**: Digite comentários diretamente

### Estrutura dos Dados
```csv
data,fonte,comentario
2024-01-15,Amazon,Produto excelente!
2024-01-16,Site,Entrega rápida
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```bash
export GEMINI_API_KEY="sua_api_key"  # Alternativa ao config.ini
```

### Personalizar Análise
Edite `src/feedback_analyzer/gemini_processor.py`:
- Ajustar prompts de análise
- Modificar categorias
- Alterar parâmetros da IA

## 📈 Resultados

### Relatório Markdown
- Análise quantitativa (sentimentos, categorias)
- Resumo executivo por IA
- Detalhes de cada comentário
- Estatísticas de processamento

### Dashboard Web
- Gráficos interativos
- Filtros por categoria/sentimento
- Exportação de dados
- Análise temporal

## 🔍 Exemplos de Uso

### 1. Analisar produto da Amazon
```python
# O sistema detecta automaticamente o site
URL: https://amazon.com.br/produto/reviews
```

### 2. Carregar arquivo local
```python
# Coloque na pasta dados/
dados/meus_comentarios.csv
dados/feedback_clientes.txt
```

### 3. API Programática
```python
from src.feedback_analyzer import analisar_comentario_individual

resultado = analisar_comentario_individual("Produto muito bom!")
print(resultado['sentimento'])  # Positivo
```

## 🛠️ Desenvolvimento

### Estrutura Modular
- `src/feedback_analyzer/`: Módulo principal importável
- `__init__.py`: Torna o pacote importável
- Separação clara entre dados, código e resultados

### Adicionar Nova Funcionalidade
```python
# Em src/feedback_analyzer/novo_modulo.py
def nova_funcao():
    pass

# Em src/feedback_analyzer/__init__.py
from .novo_modulo import nova_funcao
__all__.append('nova_funcao')
```

## 📋 Dependências

### Principais
- `pandas`: Manipulação de dados
- `google-generativeai`: API do Gemini
- `selenium`: Extração web avançada
- `beautifulsoup4`: Parsing HTML
- `tqdm`: Barras de progresso

### Opcionais
- `streamlit`: Dashboard web
- `plotly`: Gráficos interativos

## 🚨 Solução de Problemas

### Erro de Importação
```bash
# Verifique se está na pasta correta
pwd  # Deve mostrar .../Feedback_Analyzer

# Ative o ambiente virtual
source venv/bin/activate

# Reinstale dependências
pip install -r requirements.txt
```

### Erro de API Gemini
```bash
# Verifique config.ini
cat config.ini

# Teste sua API key
python3 -c "import google.generativeai as genai; genai.configure(api_key='SUA_KEY'); print('OK')"
```

### Erro de Extração Web
- Alguns sites bloqueiam automação
- Use arquivos locais como alternativa
- Tente URLs diretas para páginas de reviews

## 📞 Suporte

### Logs e Debug
- Mensagens detalhadas no terminal
- Relatórios salvos em `relatorios/`
- Fallbacks automáticos para erros

### Limitações Conhecidas
- API Gemini tem limite de cota
- Sites podem bloquear extração
- Selenium requer Chrome/Chromium

## 🎯 Próximos Passos

- [ ] Suporte a mais sites de e-commerce
- [ ] Análise de imagens de reviews
- [ ] API REST para integração
- [ ] Dashboard mais avançado
- [ ] Análise de tendências temporais

---

**Versão**: 1.0.0  
**Autor**: João Milanezi  
**Licença**: MIT
