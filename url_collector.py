from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from datetime import datetime
import platform
from browser_config import configurar_driver
import logging
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def scroll_ate_o_fim(driver, max_scrolls=None):
    """
    Rola a página até o fim para carregar todos os produtos.
    Retorna False se não houver mais conteúdo para carregar.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    num_scrolls = 0
    num_tentativas_mesma_altura = 0
    max_tentativas_mesma_altura = 3  # Número máximo de tentativas na mesma altura
    
    while True:
        # Se atingiu o número máximo de scrolls, para
        if max_scrolls and num_scrolls >= max_scrolls:
            logging.info("Número máximo de scrolls atingido")
            return True
            
        # Rola até o fim da página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Espera o carregamento
        time.sleep(2)
        
        # Calcula a nova altura
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Se a altura não mudou, pode ser fim da página ou conteúdo ainda carregando
        if new_height == last_height:
            num_tentativas_mesma_altura += 1
            if num_tentativas_mesma_altura >= max_tentativas_mesma_altura:
                logging.info("Fim da página detectado - altura não mudou após várias tentativas")
                return False
        else:
            num_tentativas_mesma_altura = 0
            last_height = new_height
            num_scrolls += 1
            logging.debug(f"Rolando a página... (scroll {num_scrolls})")

def extrair_urls_produtos(driver, max_urls=None, urls_ja_coletadas=None):
    """
    Extrai todas as URLs e nomes dos produtos da página atual.
    
    Args:
        driver: WebDriver do Selenium
        max_urls: Número máximo de URLs a coletar
        urls_ja_coletadas: Set de URLs já coletadas para evitar duplicatas
    
    Returns:
        list: Lista de dicionários com 'url' e 'nome' dos produtos
        bool: True se encontrou produtos novos, False se não
    """
    produtos_info = []
    urls_ja_coletadas = urls_ja_coletadas or set()
    produtos_novos = False
    
    # Aguarda um pouco mais para garantir que a página carregou completamente
    time.sleep(5)
    
    try:
        # Primeiro tenta encontrar os produtos usando diferentes seletores comuns
        selectors = [
            "div[data-testid='product-card']",  # Novo padrão comum
            "div.product-card",                  # Classe direta
            "div[class*='product-card']",        # Classe parcial
            "div[class*='ProductCard']",         # Variação CamelCase
            "div.vtex-product-summary-2-x-container",  # Padrão VTEX
            "div.shelf-product",                 # Padrão antigo
            "article[data-testid='product-card']"  # Variação com article
        ]
        
        for selector in selectors:
            logging.debug(f"Tentando seletor: {selector}")
            logger.debug(f"Tentando seletor: {selector}")
            cards = driver.find_elements(By.CSS_SELECTOR, selector)
            if cards:
                logger.info(f"Encontrados {len(cards)} produtos com seletor: {selector}")
                break
        
        if not cards:
            # Se não encontrou com os seletores anteriores, tenta encontrar qualquer link de produto
            logger.info("Tentando encontrar links de produtos diretamente...")
            cards = driver.find_elements(By.CSS_SELECTOR, "a[href*='/produto/']")
            
        for card in cards:
            try:
                # Tenta diferentes maneiras de obter a URL e o nome
                url = None
                nome = None
                
                # Tenta encontrar a URL
                if '/produto/' in card.get_attribute('href'):
                    url = card.get_attribute('href')
                else:
                    link = card.find_element(By.CSS_SELECTOR, "a[href*='/produto/']")
                    url = link.get_attribute('href')
                
                # Se a URL já foi coletada, pula
                if url in urls_ja_coletadas:
                    continue
                
                # Tenta diferentes seletores para o nome
                nome_selectors = [
                    "h2[class*='product-card__title']",
                    "h2[class*='ProductCard__title']",
                    "span[class*='product-name']",
                    "div[class*='product-name']",
                    "h2",
                    "h3",
                    "span[class*='title']"
                ]
                
                for nome_selector in nome_selectors:
                    try:
                        nome_element = card.find_element(By.CSS_SELECTOR, nome_selector)
                        nome = nome_element.text.strip()
                        if nome:
                            break
                    except:
                        continue
                
                # Se não encontrou o nome pelos seletores, tenta extrair da URL
                if not nome and url:
                    nome = url.split('/')[-1].replace('-', ' ').strip()
                
                if url and nome and url not in [p['url'] for p in produtos_info]:
                    produtos_info.append({
                        'url': url,
                        'nome': nome
                    })
                    urls_ja_coletadas.add(url)
                    produtos_novos = True
                    logger.debug(f"Produto encontrado: {nome} - {url}")
                    
                    # Se atingiu o número máximo de URLs, para
                    if max_urls and len(produtos_info) >= max_urls:
                        logger.info(f"Número máximo de URLs atingido ({max_urls})")
                        break
                        
            except Exception as e:
                logger.error(f"Erro ao extrair informações do produto: {str(e)}")
                continue
        
        logger.info(f"Total de produtos encontrados nesta página: {len(produtos_info)}")
        
    except Exception as e:
        logger.error(f"Erro ao processar página: {str(e)}")
    
    return produtos_info, produtos_novos

def coletar_urls_categoria(url_categoria, categoria_nome, max_paginas=None, max_urls_por_pagina=None, max_scrolls=None):
    """Coleta todas as URLs dos produtos de uma categoria."""
    driver = configurar_driver()
    todas_urls = []
    urls_ja_coletadas = set()
    pagina = 1
    paginas_sem_produtos_novos = 0
    max_paginas_sem_produtos = 3  # Se não encontrar produtos novos em 3 páginas seguidas, considera fim da categoria
    
    try:
        # Remove o parâmetro de página se existir na URL base
        url_base = re.sub(r'[?&]p=\d+', '', url_categoria)
        # Garante que temos um '?' ou '&' apropriado para adicionar parâmetros
        if '?' not in url_base:
            url_base += '?'
        elif not url_base.endswith('&') and not url_base.endswith('?'):
            url_base += '&'
        
        while True:
            # Se atingiu o número máximo de páginas, para
            if max_paginas and pagina > max_paginas:
                logger.info(f"Número máximo de páginas atingido ({max_paginas})")
                break
                
            url_paginada = f"{url_base}p={pagina}"
            logger.info(f"Processando página {pagina}: {url_paginada}")
            
            driver.get(url_paginada)
            time.sleep(3)  # Aguarda carregamento inicial
            
            # Rola até o fim para carregar todos os produtos
            tem_mais_conteudo = scroll_ate_o_fim(driver, max_scrolls)
            
            # Extrai URLs e nomes dos produtos
            produtos_pagina, encontrou_novos = extrair_urls_produtos(
                driver, 
                max_urls_por_pagina,
                urls_ja_coletadas
            )
            
            # Se não encontrou produtos novos, incrementa o contador
            if not encontrou_novos:
                paginas_sem_produtos_novos += 1
                logger.info(f"Página {pagina} não trouxe produtos novos. ({paginas_sem_produtos_novos}/{max_paginas_sem_produtos})")
                
                # Se atingiu o limite de páginas sem produtos novos, considera fim da categoria
                if paginas_sem_produtos_novos >= max_paginas_sem_produtos:
                    logger.info(f"Fim da categoria detectado - {max_paginas_sem_produtos} páginas sem produtos novos")
                    break
            else:
                paginas_sem_produtos_novos = 0  # Reseta o contador se encontrou produtos novos
            
            # Adiciona informações extras para cada produto
            for produto in produtos_pagina:
                produto.update({
                    'categoria': categoria_nome,
                    'pagina': pagina,
                    'data_coleta': datetime.now().isoformat()
                })
            
            todas_urls.extend(produtos_pagina)
            logger.info(f"Total de produtos encontrados até agora: {len(todas_urls)}")
            
            # Se não tem mais conteúdo para carregar e não encontrou produtos novos, chegamos ao fim
            if not tem_mais_conteudo and not encontrou_novos:
                logger.info("Fim da categoria detectado - não há mais conteúdo para carregar")
                break
            
            pagina += 1
            
    except Exception as e:
        logger.error(f"Erro ao processar categoria: {e}")
    finally:
        driver.quit()
    
    return todas_urls

class URLCollector:
    def __init__(self, modo_teste=False):
        """
        Inicializa o coletor de URLs.
        
        Args:
            modo_teste (bool): Se True, limita a quantidade de URLs coletadas
        """
        self.modo_teste = modo_teste
        
        # Configurações para o modo de teste
        self.max_urls_teste = 50  # Limite de URLs no modo teste
        self.max_paginas_teste = 2  # Limite de páginas no modo teste
        self.max_scrolls_teste = 3  # Limite de scrolls no modo teste

    def coletar_urls(self, categoria_url):
        """
        Coleta URLs dos produtos.
        
        Args:
            categoria_url (str): URL da categoria para coletar
        
        Returns:
            list: Lista de dicionários contendo as URLs coletadas
        """
        logger.info("Coletando URLs dos produtos...")
        
        # Extrai o nome da categoria da URL
        categoria_nome = "Alimentos Congelados" if "congelados" in categoria_url.lower() else "Doces e Sobremesas"
        
        if self.modo_teste:
            logger.info("Modo de teste ativado - limitando quantidade de URLs...")
            urls = coletar_urls_categoria(
                categoria_url,
                categoria_nome,
                max_paginas=self.max_paginas_teste,
                max_urls_por_pagina=self.max_urls_teste // self.max_paginas_teste,  # Distribui o limite entre as páginas
                max_scrolls=self.max_scrolls_teste
            )
        else:
            urls = coletar_urls_categoria(categoria_url, categoria_nome)
            
        logger.info(f"Total de URLs coletadas: {len(urls)}")
        return urls

    def salvar_urls_csv(self, urls, nome_arquivo=None):
        """
        Salva as URLs coletadas em um arquivo CSV.
        
        Args:
            urls (list): Lista de dicionários contendo as URLs
            nome_arquivo (str, optional): Nome do arquivo CSV para salvar. Se None, usa o nome padrão.
        """
        try:
            nome_arquivo = nome_arquivo or "urls_coletadas.csv"
            df = pd.DataFrame(urls)
            df.to_csv(nome_arquivo, index=False)
            logger.info(f"URLs salvas com sucesso em {nome_arquivo}")
        except Exception as e:
            logger.error(f"Erro ao salvar URLs em CSV: {str(e)}")
            raise

if __name__ == "__main__":
    logger.info("Este arquivo não deve ser executado diretamente. Use o main.py") 