import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class ExtractorComentarios:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def detectar_plataforma(self, url):
        """Detecta a plataforma baseada na URL"""
        url_lower = url.lower()
        
        if 'amazon.com' in url_lower or 'amazon.' in url_lower:
            return 'amazon'
        elif 'mercadolivre.com' in url_lower or 'mercadolibre.' in url_lower:
            return 'mercadolivre'
        elif 'americanas.com' in url_lower:
            return 'americanas'
        elif 'shopee.com' in url_lower:
            return 'shopee'
        elif 'aliexpress.com' in url_lower:
            return 'aliexpress'
        elif 'booking.com' in url_lower:
            return 'booking'
        elif 'tripadvisor.com' in url_lower:
            return 'tripadvisor'
        elif 'play.google.com' in url_lower:
            return 'google_play'
        elif 'apps.apple.com' in url_lower:
            return 'app_store'
        else:
            return 'generico'

    def extrair_comentarios_amazon(self, url):
        """Extrai comentários do Amazon"""
        comentarios = []
        try:
            # Modificar URL para ir direto às reviews
            if '/dp/' in url:
                product_id = url.split('/dp/')[1].split('/')[0]
                reviews_url = f"https://www.amazon.com/product-reviews/{product_id}"
            else:
                reviews_url = url

            response = self.session.get(reviews_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Seletores para comentários do Amazon
            review_elements = soup.find_all('div', {'data-hook': 'review'})
            
            for review in review_elements[:20]:  # Limitar a 20 comentários
                texto_element = review.find('span', {'data-hook': 'review-body'})
                if texto_element:
                    texto = texto_element.get_text().strip()
                    if len(texto) > 10:  # Filtrar comentários muito curtos
                        comentarios.append({
                            'texto': texto,
                            'fonte': 'Amazon',
                            'data': time.strftime('%Y-%m-%d')
                        })
                        
        except Exception as e:
            print(f"Erro ao extrair comentários do Amazon: {e}")
            
        return comentarios

    def extrair_comentarios_mercadolivre(self, url):
        """Extrai comentários do MercadoLivre"""
        comentarios = []
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Seletores para comentários do MercadoLivre
            review_elements = soup.find_all('div', class_=re.compile('review|opinion|comment'))
            
            for review in review_elements[:15]:
                texto = review.get_text().strip()
                if len(texto) > 10 and len(texto) < 500:
                    comentarios.append({
                        'texto': texto,
                        'fonte': 'MercadoLivre',
                        'data': time.strftime('%Y-%m-%d')
                    })
                    
        except Exception as e:
            print(f"Erro ao extrair comentários do MercadoLivre: {e}")
            
        return comentarios

    def extrair_comentarios_google_play(self, url):
        """Extrai comentários do Google Play usando Selenium"""
        comentarios = []
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            
            # Esperar a página carregar
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-g="review"]'))
            )
            
            # Rolar para baixo para carregar mais comentários
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Extrair comentários
            review_elements = driver.find_elements(By.CSS_SELECTOR, '[data-g="review"]')
            
            for review in review_elements[:20]:
                try:
                    texto_element = review.find_element(By.CSS_SELECTOR, '[jsname="bN97Pc"]')
                    texto = texto_element.text.strip()
                    if len(texto) > 10:
                        comentarios.append({
                            'texto': texto,
                            'fonte': 'Google Play',
                            'data': time.strftime('%Y-%m-%d')
                        })
                except:
                    continue
                    
            driver.quit()
            
        except Exception as e:
            print(f"Erro ao extrair comentários do Google Play: {e}")
            
        return comentarios

    def extrair_comentarios_generico(self, url):
        """Extrai comentários de sites genéricos"""
        comentarios = []
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar por padrões comuns de comentários
            selectors = [
                'div[class*="review"]',
                'div[class*="comment"]',
                'div[class*="feedback"]',
                'div[class*="opinion"]',
                'p[class*="review"]',
                '.review-text',
                '.comment-text',
                '.user-review'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements[:10]:
                    texto = element.get_text().strip()
                    if 20 < len(texto) < 500:  # Filtrar textos muito curtos ou longos
                        comentarios.append({
                            'texto': texto,
                            'fonte': 'Web',
                            'data': time.strftime('%Y-%m-%d')
                        })
                        
                if comentarios:  # Se encontrou comentários, parar
                    break
                    
        except Exception as e:
            print(f"Erro ao extrair comentários genéricos: {e}")
            
        return comentarios

    def extrair_comentarios_url(self, url):
        """Método principal para extrair comentários de qualquer URL"""
        print(f"🔍 Analisando URL: {url}")
        
        plataforma = self.detectar_plataforma(url)
        print(f"🏪 Plataforma detectada: {plataforma}")
        
        comentarios = []
        
        if plataforma == 'amazon':
            comentarios = self.extrair_comentarios_amazon(url)
        elif plataforma == 'mercadolivre':
            comentarios = self.extrair_comentarios_mercadolivre(url)
        elif plataforma == 'google_play':
            comentarios = self.extrair_comentarios_google_play(url)
        else:
            # Tentar extração genérica
            comentarios = self.extrair_comentarios_generico(url)
        
        if comentarios:
            print(f"✅ Extraídos {len(comentarios)} comentários")
            # Converter para DataFrame
            df = pd.DataFrame(comentarios)
            df.columns = ['comentario', 'fonte', 'data']  # Renomear para compatibilidade
            return df
        else:
            print("❌ Nenhum comentário encontrado")
            return pd.DataFrame()


def extrair_comentarios_de_url(url):
    """Função pública para extrair comentários de uma URL"""
    extractor = ExtractorComentarios()
    return extractor.extrair_comentarios_url(url)
