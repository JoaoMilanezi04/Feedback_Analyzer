"""
Módulo para extrair comentários de produtos de diferentes plataformas web.
Suporta Amazon, MercadoLivre, Google Play, App Store e sites genéricos.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException
import json
from urllib.parse import urlparse


def configurar_driver():
    """Configura o driver do Chrome com opções otimizadas."""
    try:
        options = Options()
        options.add_argument('--headless')  # Executa em modo headless
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"⚠️ Selenium não disponível: {e}")
        print("📝 Tentando extração alternativa com requests...")
        return None


def extrair_amazon(driver, url):
    """Extrai comentários da Amazon."""
    comentarios = []
    
    try:
        driver.get(url)
        time.sleep(3)
        
        # Tentar encontrar o link de reviews
        try:
            reviews_link = driver.find_element(By.PARTIAL_LINK_TEXT, "customer reviews")
            reviews_link.click()
            time.sleep(3)
        except:
            # Se não encontrar, tentar buscar reviews na página atual
            pass
        
        # Extrair comentários
        review_elements = driver.find_elements(By.CSS_SELECTOR, "[data-hook='review-body'] span")
        
        for review in review_elements[:50]:  # Limitar a 50 comentários
            texto = review.text.strip()
            if texto and len(texto) > 10:
                comentarios.append(texto)
        
        print(f"✅ Amazon: {len(comentarios)} comentários extraídos")
        
    except Exception as e:
        print(f"❌ Erro ao extrair da Amazon: {e}")
    
    return comentarios


def extrair_mercadolivre(driver, url):
    """Extrai comentários do MercadoLivre."""
    comentarios = []
    
    try:
        driver.get(url)
        time.sleep(3)
        
        # Tentar clicar na aba de opiniões
        try:
            opinions_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Opiniões') or contains(text(), 'Opiniones')]"))
            )
            opinions_tab.click()
            time.sleep(3)
        except:
            print("⚠️ Não foi possível encontrar a aba de opiniões")
        
        # Extrair comentários com diferentes seletores
        selectors = [
            ".ui-review-view__comment",
            ".ui-review-capability-comments__comment__text",
            "[class*='review'] [class*='comment']",
            ".review-text",
            ".opinion-text"
        ]
        
        for selector in selectors:
            review_elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if review_elements:
                break
        
        for review in review_elements[:50]:  # Limitar a 50 comentários
            texto = review.text.strip()
            if texto and len(texto) > 10:
                comentarios.append(texto)
        
        print(f"✅ MercadoLivre: {len(comentarios)} comentários extraídos")
        
    except Exception as e:
        print(f"❌ Erro ao extrair do MercadoLivre: {e}")
    
    return comentarios


def extrair_google_play(driver, url):
    """Extrai reviews do Google Play."""
    comentarios = []
    
    try:
        driver.get(url)
        time.sleep(3)
        
        # Scroll para carregar mais reviews
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        
        # Extrair reviews
        review_elements = driver.find_elements(By.CSS_SELECTOR, "[jsname='bN97Pc']")
        
        for review in review_elements[:50]:
            texto = review.text.strip()
            if texto and len(texto) > 10:
                comentarios.append(texto)
        
        print(f"✅ Google Play: {len(comentarios)} reviews extraídos")
        
    except Exception as e:
        print(f"❌ Erro ao extrair do Google Play: {e}")
    
    return comentarios


def extrair_app_store(url):
    """Extrai reviews do App Store usando requests (sem Selenium)."""
    comentarios = []
    
    try:
        # O App Store tem uma API diferente, vamos tentar uma abordagem básica
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tentar encontrar reviews (o App Store é mais complexo)
        review_elements = soup.find_all(['p', 'div'], class_=re.compile('review|comment'))
        
        for review in review_elements[:20]:
            texto = review.get_text().strip()
            if texto and len(texto) > 10:
                comentarios.append(texto)
        
        print(f"✅ App Store: {len(comentarios)} reviews extraídos")
        
    except Exception as e:
        print(f"❌ Erro ao extrair do App Store: {e}")
    
    return comentarios


def extrair_generico(driver, url):
    """Extrai comentários de sites genéricos."""
    comentarios = []
    
    try:
        driver.get(url)
        time.sleep(3)
        
        # Seletores genéricos para comentários
        selectors = [
            "[class*='comment']",
            "[class*='review']",
            "[class*='feedback']",
            "[class*='opinion']",
            ".comment-text",
            ".review-text",
            ".user-comment",
            ".customer-review"
        ]
        
        for selector in selectors:
            review_elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if review_elements:
                for review in review_elements[:30]:
                    texto = review.text.strip()
                    if texto and len(texto) > 10:
                        comentarios.append(texto)
                if comentarios:
                    break
        
        print(f"✅ Site genérico: {len(comentarios)} comentários extraídos")
        
    except Exception as e:
        print(f"❌ Erro ao extrair do site genérico: {e}")
    
    return comentarios


def identificar_plataforma(url):
    """Identifica a plataforma baseada na URL."""
    url_lower = url.lower()
    domain = urlparse(url).netloc.lower()
    
    if 'amazon' in domain:
        return 'amazon'
    elif 'mercadolivre' in domain or 'mercadolibre' in domain:
        return 'mercadolivre'
    elif 'play.google.com' in domain:
        return 'google_play'
    elif 'apps.apple.com' in domain:
        return 'app_store'
    else:
        return 'generico'


def extrair_comentarios_de_url(url):
    """
    Função principal para extrair comentários de uma URL.
    
    Args:
        url (str): URL do produto/aplicativo
    
    Returns:
        pandas.DataFrame: DataFrame com os comentários extraídos
    """
    print(f"🌐 Extraindo comentários de: {url}")
    
    plataforma = identificar_plataforma(url)
    print(f"📱 Plataforma detectada: {plataforma.title()}")
    
    comentarios = []
    
    # Tentar primeiro com Selenium (mais eficiente)
    driver = configurar_driver()
    
    if driver:
        print("🤖 Usando Selenium para extração...")
        try:
            if plataforma == 'amazon':
                comentarios = extrair_amazon(driver, url)
            elif plataforma == 'mercadolivre':
                comentarios = extrair_mercadolivre(driver, url)
            elif plataforma == 'google_play':
                comentarios = extrair_google_play(driver, url)
            elif plataforma == 'app_store':
                comentarios = extrair_app_store(url)
            else:
                comentarios = extrair_generico(driver, url)
        
        finally:
            driver.quit()
    
    # Se Selenium falhou ou não está disponível, usar requests
    if not comentarios:
        print("🌐 Tentando extração alternativa com requests...")
        comentarios = extrair_com_requests(url)
    
    if not comentarios:
        print("⚠️ Nenhum comentário foi extraído. Possíveis causas:")
        print("  • O site pode ter proteção anti-bot")
        print("  • A estrutura da página pode ter mudado")
        print("  • O produto pode não ter comentários")
        print("  • Sua conexão pode estar instável")
        print("  • Chrome não está instalado (para Selenium)")
        return pd.DataFrame()
    
    # Criar DataFrame
    df = pd.DataFrame({'comentario': comentarios})
    
    # Limpar e filtrar comentários
    df['comentario'] = df['comentario'].str.strip()
    df = df[df['comentario'].str.len() > 10]  # Remover comentários muito curtos
    df = df.drop_duplicates('comentario')  # Remover duplicatas
    df = df.reset_index(drop=True)
    
    print(f"✅ Total de comentários únicos extraídos: {len(df)}")
    
    return df


def salvar_comentarios(df, arquivo='comentarios_extraidos.csv'):
    """Salva os comentários extraídos em um arquivo."""
    try:
        df.to_csv(arquivo, index=False, encoding='utf-8')
        print(f"💾 Comentários salvos em: {arquivo}")
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")


def extrair_com_requests(url):
    """Extração alternativa usando apenas requests e BeautifulSoup."""
    comentarios = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        session = requests.Session()
        session.headers.update(headers)
        
        print("🌐 Fazendo requisição HTTP...")
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Tentar diferentes seletores para encontrar comentários/reviews
        selectors = [
            # MercadoLivre
            '.ui-review-view__comment',
            '.ui-review-capability-comments__comment__text',
            '[class*="review"] [class*="comment"]',
            '[class*="opinion"]',
            
            # Amazon
            '[data-hook="review-body"] span',
            '.review-text',
            '.cr-original-review-text',
            
            # Genéricos
            '[class*="comment"]',
            '[class*="review"]',
            '[class*="feedback"]',
            '.comment-text',
            '.review-content',
            '.user-review',
            '.customer-review'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                print(f"✅ Encontrados elementos com seletor: {selector}")
                for element in elements[:30]:  # Limitar a 30
                    text = element.get_text().strip()
                    if text and len(text) > 15 and len(text) < 1000:  # Filtrar textos muito curtos ou longos
                        comentarios.append(text)
                
                if comentarios:
                    break
        
        # Se não encontrou com seletores específicos, tentar busca por texto
        if not comentarios:
            print("🔍 Tentando busca por texto...")
            all_text = soup.get_text()
            # Procurar por padrões comuns de reviews
            patterns = [
                r'(?i)(?:excelente|ótimo|bom|ruim|péssimo|recomendo|não recomendo).{10,200}',
                r'(?i)(?:produto|app|aplicativo|serviço).{10,200}',
                r'(?i)(?:comprei|usei|testei|instalei).{10,200}'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, all_text)
                for match in matches[:10]:  # Limitar a 10 por padrão
                    if len(match.strip()) > 15:
                        comentarios.append(match.strip())
        
        print(f"📝 Extração com requests: {len(comentarios)} comentários encontrados")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição HTTP: {e}")
    except Exception as e:
        print(f"❌ Erro na extração com requests: {e}")
    
    return comentarios


if __name__ == "__main__":
    # Teste da extração
    url_teste = input("Digite a URL para teste: ")
    comentarios_df = extrair_comentarios_de_url(url_teste)
    
    if not comentarios_df.empty:
        print(f"\n📊 Primeiros 5 comentários:")
        for i, comentario in enumerate(comentarios_df['comentario'].head(), 1):
            print(f"{i}. {comentario[:100]}...")
        
        salvar = input("\nDeseja salvar os comentários? (s/n): ").lower().strip()
        if salvar == 's':
            salvar_comentarios(comentarios_df)
