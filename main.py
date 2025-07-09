
import sys
import os

# Adicionar src ao path para permitir importações
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Agora podemos importar normalmente
from feedback_analyzer_main import main as main_func

if __name__ == "__main__":
    main_func()