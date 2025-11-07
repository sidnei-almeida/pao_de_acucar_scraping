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
from scraping_log import logger
import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os

# ============================================================================
# CHECKPOINT & RECOVERY UTILITIES
# ============================================================================

def salvar_checkpoint(arquivo, urls, num_scrolls, posicao_scroll=0):
    """
    Persist a checkpoint with URLs and metadata for crash recovery.

    Args:
        arquivo (str): Checkpoint filename
        urls (list): URLs collected so far
        num_scrolls (int): Number of scroll operations executed
        posicao_scroll (int): Current scroll position on the page
    """
    try:
        checkpoint = {
            'urls': urls,
            'num_scrolls': num_scrolls,
            'posicao_scroll': posicao_scroll,
            'timestamp': datetime.now().isoformat(),
            'total_produtos': len(urls)
        }
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2)
        logger.info(f"✅ Checkpoint saved: {len(urls)} product(s), {num_scrolls} scroll(s)")
    except Exception as e:
        logger.error(f"❌ Failed to save checkpoint: {e}")

def carregar_checkpoint(arquivo):
    """
    Load a checkpoint if one is available.

    Args:
        arquivo (str): Checkpoint filename

    Returns:
        dict | None: Checkpoint payload or None when not found
    """
    try:
        if os.path.exists(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)
            logger.info(
                f"📦 Checkpoint loaded: {checkpoint['total_produtos']} product(s), "
                f"{checkpoint['num_scrolls']} scroll(s)"
            )
            logger.info(f"   Timestamp: {checkpoint['timestamp']}")
            return checkpoint
    except Exception as e:
        logger.error(f"❌ Failed to load checkpoint: {e}")
    return None

def limpar_checkpoint(arquivo):
    """
    Remove a checkpoint after a successful run.

    Args:
        arquivo (str): Checkpoint filename
    """
    try:
        if os.path.exists(arquivo):
            os.remove(arquivo)
            logger.info(f"🗑️  Checkpoint removed: {arquivo}")
    except Exception as e:
        logger.error(f"❌ Failed to remove checkpoint: {e}")

# ============================================================================
# URL HARVESTING UTILITIES
# ============================================================================

def scroll_ate_o_fim(driver, max_scrolls=None):
    """
    Scroll the page until the end to load every product card.
    Returns False when no additional content can be loaded.
    """
    num_scrolls = 0
    produtos_antes = len(driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-card'], a[href*='/produto/']"))
    contagem_mesma_quantidade = 0
    max_tentativas_mesma_quantidade = 3  # Max times we tolerate seeing the same count
    ultima_quantidade = produtos_antes
    
    logger.info(f"Starting harvest with {produtos_antes} product(s)")
    
    while True:
        # Stop if we hit the max allowed scroll count
        if max_scrolls and num_scrolls >= max_scrolls:
            logger.info("Maximum scroll threshold reached")
            return True
            
        # Scroll by one-third of the total height
        altura_viewport = driver.execute_script("return window.innerHeight")
        altura_total = driver.execute_script("return document.body.scrollHeight")
        posicao_atual = driver.execute_script("return window.pageYOffset")
        
        # Calculate next scroll position (1/3 of total height)
        proxima_posicao = min(posicao_atual + (altura_total / 3), altura_total - altura_viewport)
        
        # Execute the scroll
        driver.execute_script(f"window.scrollTo(0, {proxima_posicao});")
        time.sleep(5)  # Allow lazy-loaded cards to render
        
        # Count product cards after scrolling
        produtos_depois = len(driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-card'], a[href*='/produto/']"))
        
        # If the product count has not changed
        if produtos_depois == ultima_quantidade:
            contagem_mesma_quantidade += 1
            logger.info(
                f"Product count unchanged: {produtos_depois} "
                f"(attempt {contagem_mesma_quantidade} of {max_tentativas_mesma_quantidade})"
            )
            
            # Stop if we already tried enough times without any change
            if contagem_mesma_quantidade >= max_tentativas_mesma_quantidade:
                logger.info(
                    "End of page detected — product count remained stable after "
                    f"{max_tentativas_mesma_quantidade} attempts"
                )
                return False
        else:
            # Reset counter when new products appear
            logger.info(
                f"New products loaded: {produtos_depois - ultima_quantidade} "
                f"(total: {produtos_depois})"
            )
            contagem_mesma_quantidade = 0
            ultima_quantidade = produtos_depois
        
        num_scrolls += 1
        logger.info(f"Scroll {num_scrolls} - Total products: {produtos_depois}")
        
        # Attempt to click “load more” button when present
        try:
            botao_carregar = driver.find_element(By.CSS_SELECTOR, "button[class*='load-more']")
            if botao_carregar.is_displayed():
                botao_carregar.click()
                time.sleep(5)  # Give time for new cards to load
                logger.info("Clicked the 'load more' button")
        except:
            pass

def extrair_urls_produtos(driver, max_urls=None, urls_ja_coletadas=None):
    """
    Extract every product URL and name currently visible on the page.

    Args:
        driver: Selenium WebDriver instance
        max_urls: Optional cap for the number of URLs to collect
        urls_ja_coletadas: Set of URLs already collected to avoid duplicates

    Returns:
        list: List of dicts containing product `url` and `nome`
        bool: True when new products were found, otherwise False
    """
    produtos_info = []
    urls_ja_coletadas = urls_ja_coletadas or set()
    produtos_novos = False
    
    # Give the page a moment to finish rendering
    time.sleep(5)
    
    try:
        # Try multiple selectors because the layout may vary
        selectors = [
            "div[data-testid='product-card']",             # Current layout pattern
            "div.product-card",                            # Direct class
            "div[class*='product-card']",                  # Partial match
            "div[class*='ProductCard']",                   # CamelCase variant
            "div.vtex-product-summary-2-x-container",      # VTEX pattern
            "div.shelf-product",                           # Legacy markup
            "article[data-testid='product-card']",         # Article variant
            "a[href*='/produto/']"                         # Direct product anchor
        ]
        
        cards = None
        for selector in selectors:
            logger.debug(f"Trying selector: {selector}")
            cards = driver.find_elements(By.CSS_SELECTOR, selector)
            if cards:
                logger.info(f"Found {len(cards)} product(s) with selector: {selector}")
                break
        
        if not cards:
            logger.info("No products found using the available selectors")
            return [], False
            
        for card in cards:
            try:
                # Attempt different strategies to fetch URL and title
                url = None
                nome = None
                
                # Retrieve the product URL
                if '/produto/' in card.get_attribute('href'):
                    url = card.get_attribute('href')
                else:
                    link = card.find_element(By.CSS_SELECTOR, "a[href*='/produto/']")
                    url = link.get_attribute('href')
                
                # Skip duplicates
                if url in urls_ja_coletadas:
                    continue
                
                # Try multiple selectors for the product name
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
                
                # Fallback: derive name from the URL slug
                if not nome and url:
                    nome = url.split('/')[-1].replace('-', ' ').strip()
                
                if url and nome and url not in [p['url'] for p in produtos_info]:
                    produtos_info.append({
                        'url': url,
                        'nome': nome
                    })
                    urls_ja_coletadas.add(url)
                    produtos_novos = True
                    logger.debug(f"Product captured: {nome} - {url}")
                
                # Honor the max limit when running in test mode
                if max_urls and len(produtos_info) >= max_urls:
                    logger.info(f"Reached maximum URL cap ({max_urls})")
                    break
                    
            except Exception as e:
                logger.error(f"Failed to extract product information: {str(e)}")
                continue
    
        logger.info(f"Products captured on this page: {len(produtos_info)}")
        
    except Exception as e:
        logger.error(f"Failed to parse page: {str(e)}")
    
    return produtos_info, produtos_novos

def coletar_urls_categoria(url_categoria, categoria_nome, max_paginas=None, max_urls_por_pagina=None, max_scrolls=None):
    """Collect every product URL for a given category page."""
    driver = configurar_driver()
    todas_urls = []
    urls_ja_coletadas = set()
    pagina = 1
    paginas_sem_produtos_novos = 0
    max_paginas_sem_produtos = 3  # When 3 consecutive pages add nothing new, stop
    
    try:
        # Strip page parameter if present
        url_base = re.sub(r'[?&]p=\d+', '', url_categoria)
        # Ensure the URL is ready for pagination
        if '?' not in url_base:
            url_base += '?'
        elif not url_base.endswith('&') and not url_base.endswith('?'):
            url_base += '&'
        
        while True:
            # Stop when we reach the configured page limit
            if max_paginas and pagina > max_paginas:
                logger.info(f"Maximum page limit reached ({max_paginas})")
                break
                
            url_paginada = f"{url_base}p={pagina}"
            logger.info(f"Processing page {pagina}: {url_paginada}")
            
            driver.get(url_paginada)
            time.sleep(3)  # Allow initial content to render
            
            # Scroll to the end so every product appears
            tem_mais_conteudo = scroll_ate_o_fim(driver, max_scrolls)
            
            # Extract product URLs and names
            produtos_pagina, encontrou_novos = extrair_urls_produtos(
                driver, 
                max_urls_por_pagina,
                urls_ja_coletadas
            )
            
            # Track consecutive pages without new results
            if not encontrou_novos:
                paginas_sem_produtos_novos += 1
                logger.info(
                    f"Page {pagina} returned no new products "
                    f"({paginas_sem_produtos_novos}/{max_paginas_sem_produtos})"
                )
                
                # Stop once the threshold is reached
                if paginas_sem_produtos_novos >= max_paginas_sem_produtos:
                    logger.info(
                        "Category appears exhausted — "
                        f"{max_paginas_sem_produtos} consecutive pages without new products"
                    )
                    break
            else:
                paginas_sem_produtos_novos = 0  # Reset counter when new products are found
            
            # Enrich every product with metadata
            for produto in produtos_pagina:
                produto.update({
                    'categoria': categoria_nome,
                    'pagina': pagina,
                    'data_coleta': datetime.now().isoformat()
                })
            
            todas_urls.extend(produtos_pagina)
            logger.info(f"Running total of products collected: {len(todas_urls)}")
            
            # Break if the page has no more content and no new products were found
            if not tem_mais_conteudo and not encontrou_novos:
                logger.info("Category seems finished — no additional content available")
                break
            
            pagina += 1
            
    except Exception as e:
        logger.error(f"Failed to process category: {e}")
    finally:
        driver.quit()
    
    return todas_urls

class URLCollector:
    def __init__(self):
        """Initialize the URL collector helper."""
        self.driver = None
        
    def inicializar_driver(self):
        """Spin up a new configured browser driver."""
        try:
            self.driver = configurar_driver()
            if not self.driver:
                raise Exception("Failed to configure the driver")
            return self.driver
        except Exception as e:
            logger.error(f"Error bootstrapping driver: {str(e)}")
            return None
        
    def scroll_pagina(self, driver):
        """Scroll the page to trigger lazy loading of additional products."""
        try:
            # Scroll to the page bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new content
            
            # Click the “load more” button when present
            try:
                botao_carregar = driver.find_element(By.CSS_SELECTOR, "button[class*='load-more']")
                if botao_carregar.is_displayed():
                    botao_carregar.click()
                    time.sleep(2)
            except:
                pass
                
        except Exception as e:
            logger.error(f"Error while scrolling: {str(e)}")
            
    def coletar_urls(self, url_categoria, modo_teste=False, categoria_nome=None):
        """
        Collect product URLs from a category with checkpointing and crash recovery.

        Args:
            url_categoria: Category URL to harvest
            modo_teste: When True, limit results to a small sample for validation
            categoria_nome: Human-readable category name to stamp onto products

        Returns:
            list: Aggregated list of harvested product dictionaries
        """
        driver = None
        
        # Checkpoint and restart configuration
        BATCH_SIZE = 1000  # Persist every 1000 products
        RESTART_INTERVAL = 100  # Restart browser every 100 scrolls
        MAX_RETRY_CRASHES = 3  # Maximum number of retries after crashes
        
        try:
            # Use the supplied category name or infer one from the URL
            if not categoria_nome:
                categoria_nome = 'Unknown category'
                try:
                    # Extract category name from URL fragments
                    if '/c/' in url_categoria:
                        categoria_nome = url_categoria.split('/c/')[-1].split('?')[0].split('#')[0]
                        categoria_nome = categoria_nome.replace('-', ' ').replace('_', ' ').title()
                    elif '/categoria/' in url_categoria:
                        categoria_nome = url_categoria.split('/categoria/')[-1].split('?')[0].split('#')[0]
                        # Remove the "alimentos/" prefix when present
                        if categoria_nome.lower().startswith('alimentos/'):
                            categoria_nome = categoria_nome[10:]
                        categoria_nome = categoria_nome.replace('-', ' ').replace('_', ' ').title()
                    else:
                        categoria_nome = 'Unknown category'
                except:
                    categoria_nome = 'Unknown category'
            
            # Build checkpoint filename
            categoria_slug = categoria_nome.lower().replace(' ', '_').replace('(', '').replace(')', '')
            checkpoint_file = f"urls_checkpoint_{categoria_slug}.json"
            
            # Check for previously stored checkpoints
            checkpoint = carregar_checkpoint(checkpoint_file)
            if checkpoint:
                logger.warning("⚠️  Existing checkpoint found! Resuming from last saved state...")
                todas_urls = checkpoint['urls']
                urls_ja_coletadas = set(p['url'] for p in todas_urls)
                num_scrolls_inicial = checkpoint['num_scrolls']
                posicao_scroll_inicial = checkpoint['posicao_scroll']
                logger.info(f"📊 Resuming with {len(todas_urls)} product(s) already collected")
            else:
                todas_urls = []
                urls_ja_coletadas = set()
                num_scrolls_inicial = 0
                posicao_scroll_inicial = 0
            
            # Adjust limits for test mode
            max_scrolls = 2 if modo_teste else None
            max_urls = 5 if modo_teste else None  # None => unlimited
            
            # Crash counter
            crash_count = 0
            
            # Main loop with crash recovery
            while crash_count < MAX_RETRY_CRASHES:
                try:
                    # Initialize or reinitialize the browser instance
                    if driver is None:
                        driver = self.inicializar_driver()
                        if not driver:
                            raise Exception("Failed to initialize driver")
                        
                        logger.info(f"🌐 Opening category: {url_categoria}")
                        driver.get(url_categoria)
                        time.sleep(5)
                        
                        # Jump to previously saved scroll position when resuming
                        if posicao_scroll_inicial > 0:
                            logger.info(f"⏩ Jumping to scroll position: {posicao_scroll_inicial}")
                            driver.execute_script(f"window.scrollTo(0, {posicao_scroll_inicial});")
                            time.sleep(3)
                    
                    # Scroll control variables
                    num_scrolls = num_scrolls_inicial
                    produtos_antes = len(driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-card'], a[href*='/produto/']"))
                    contagem_mesma_quantidade = 0
                    max_tentativas_mesma_quantidade = 3
                    ultima_quantidade = len(todas_urls)
                    ultimo_checkpoint_size = len(todas_urls)
                    
                    logger.info(f"🔄 Starting harvesting loop (current total: {len(todas_urls)})")
                    
                    # Scroll + collect loop
                    while True:
                        # Stop when the test-mode limit is hit
                        if max_scrolls and num_scrolls >= (max_scrolls + num_scrolls_inicial):
                            logger.info("✅ Test mode scroll limit reached")
                            break
                        
                        # Restart browser periodically to free memory
                        if not modo_teste and num_scrolls > 0 and (num_scrolls - num_scrolls_inicial) % RESTART_INTERVAL == 0 and (num_scrolls - num_scrolls_inicial) > 0:
                            logger.info(f"🔄 Restarting browser to free memory (scroll {num_scrolls})")
                            
                            # Save current position
                            posicao_atual = driver.execute_script("return window.pageYOffset")
                            
                            # Persist checkpoint before restarting
                            salvar_checkpoint(checkpoint_file, todas_urls, num_scrolls, posicao_atual)
                            
                            # Close the current driver
                            driver.quit()
                            time.sleep(2)
                            
                            # Boot a fresh driver
                            driver = self.inicializar_driver()
                            if not driver:
                                raise Exception("Failed to reinitialize driver")
                            
                            driver.get(url_categoria)
                            time.sleep(5)
                            
                            # Jump back to where we left off
                            logger.info(f"⏩ Returning to scroll position {posicao_atual}")
                            driver.execute_script(f"window.scrollTo(0, {posicao_atual});")
                            time.sleep(3)
                        
                        # Perform scroll
                        altura_viewport = driver.execute_script("return window.innerHeight")
                        altura_total = driver.execute_script("return document.body.scrollHeight")
                        posicao_atual = driver.execute_script("return window.pageYOffset")
                        
                        # Compute next scroll target
                        proxima_posicao = min(posicao_atual + (altura_total / 3), altura_total - altura_viewport)
                        
                        # Scroll
                        driver.execute_script(f"window.scrollTo(0, {proxima_posicao});")
                        time.sleep(5)
                        
                        # Extract product URLs after scrolling
                        urls_pagina, encontrou_novos = extrair_urls_produtos(
                            driver,
                            max_urls=max_urls,
                            urls_ja_coletadas=urls_ja_coletadas
                        )
                        
                        # Add metadata to each newly found product
                        # (extrair_urls_produtos already filters duplicates)
                        for produto in urls_pagina:
                            produto.update({
                                'categoria': categoria_nome,
                                'data_coleta': datetime.now().isoformat()
                            })
                            todas_urls.append(produto)
                            urls_ja_coletadas.add(produto['url'])
                        
                        # Check whether new products were added this round
                        if len(todas_urls) == ultima_quantidade:
                            contagem_mesma_quantidade += 1
                            logger.info(
                                f"⏸️  Product count unchanged: {len(todas_urls)} "
                                f"(attempt {contagem_mesma_quantidade}/{max_tentativas_mesma_quantidade})"
                            )
                            
                            if contagem_mesma_quantidade >= max_tentativas_mesma_quantidade:
                                logger.info("✅ Category appears exhausted — count remained stable")
                                break
                        else:
                            novos = len(todas_urls) - ultima_quantidade
                            logger.info(f"✨ New products discovered: +{novos} (total: {len(todas_urls)})")
                            contagem_mesma_quantidade = 0
                            ultima_quantidade = len(todas_urls)
                        
                        num_scrolls += 1
                        logger.info(f"📜 Scroll {num_scrolls} - Total products: {len(todas_urls)}")
                        
                        # Persist checkpoint once the batch size is reached
                        if len(todas_urls) - ultimo_checkpoint_size >= BATCH_SIZE:
                            salvar_checkpoint(checkpoint_file, todas_urls, num_scrolls, proxima_posicao)
                            ultimo_checkpoint_size = len(todas_urls)
                        
                        # Stop early when running in test mode
                        if modo_teste and len(todas_urls) >= 5:
                            logger.info("✅ Test mode limit of 5 URLs reached")
                            break
                        
                        # Click the “load more” button when available
                        try:
                            botao_carregar = driver.find_element(By.CSS_SELECTOR, "button[class*='load-more']")
                            if botao_carregar.is_displayed():
                                botao_carregar.click()
                                time.sleep(5)
                                logger.info("🔘 Clicked the 'load more' button")
                        except:
                            pass
                    
                    # Successful completion
                    logger.info(f"🎉 Harvest finished: {len(todas_urls)} product(s) collected")
                    
                    # Remove checkpoint now that the run succeeded
                    limpar_checkpoint(checkpoint_file)
                    
                    return todas_urls
                    
                except Exception as e:
                    error_str = str(e)
                    
                    # Identify browser crashes
                    if "tab crashed" in error_str.lower() or "session deleted" in error_str.lower():
                        crash_count += 1
                        logger.error(f"💥 Tab crashed! (attempt {crash_count}/{MAX_RETRY_CRASHES})")
                        logger.warning(f"⚠️  Error: {error_str}")
                        
                        # Persist state before retrying
                        if todas_urls:
                            posicao_atual = 0
                            try:
                                posicao_atual = driver.execute_script("return window.pageYOffset")
                            except:
                                pass
                            salvar_checkpoint(checkpoint_file, todas_urls, num_scrolls, posicao_atual)
                        
                        # Close the crashed driver
                        try:
                            if driver:
                                driver.quit()
                        except:
                            pass
                        driver = None
                        
                        # Retry if we still have attempts left
                        if crash_count < MAX_RETRY_CRASHES:
                            logger.info("⏳ Waiting 10 seconds before retrying...")
                            time.sleep(10)
                            
                            # Reload checkpoint to ensure state is up to date
                            checkpoint = carregar_checkpoint(checkpoint_file)
                            if checkpoint:
                                todas_urls = checkpoint['urls']
                                urls_ja_coletadas = set(p['url'] for p in todas_urls)
                                num_scrolls_inicial = checkpoint['num_scrolls']
                                posicao_scroll_inicial = checkpoint['posicao_scroll']
                            
                            continue  # Try again
                        else:
                            logger.error("❌ Maximum number of retries reached after crashes")
                            logger.info(f"📊 Returning {len(todas_urls)} product(s) collected so far")
                            return todas_urls
                    else:
                        # Propagate non-crash errors
                        raise
            
            # If we exit the loop without returning, hand back what we gathered
            logger.info(f"📊 Returning {len(todas_urls)} product(s) collected")
            return todas_urls
            
        except Exception as e:
            logger.error(f"❌ Unexpected error while collecting URLs: {str(e)}")
            
            # Attempt to persist state even when an unexpected error occurs
            if 'todas_urls' in locals() and todas_urls:
                try:
                    salvar_checkpoint(checkpoint_file, todas_urls, num_scrolls if 'num_scrolls' in locals() else 0, 0)
                    logger.info(f"💾 Emergency checkpoint saved with {len(todas_urls)} product(s)")
                except:
                    pass
            
            return todas_urls if 'todas_urls' in locals() else []
            
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception as e:
                    logger.error(f"Error while closing driver: {str(e)}")
                driver = None
    
    def salvar_urls_csv(self, urls, nome_arquivo=None):
        """Persist collected URLs to a CSV file."""
        try:
            if not urls:
                logger.warning("No URLs to persist — skipping export")
                return
                
            if not nome_arquivo:
                nome_arquivo = f"urls_produtos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                
            # Create DataFrame and save
            df = pd.DataFrame(urls)
            df.to_csv(nome_arquivo, index=False)
            logger.info(f"URLs exported to: {nome_arquivo}")
            
        except Exception as e:
            logger.error(f"Failed to export URLs: {str(e)}")

if __name__ == "__main__":
    logger.info("This module is not meant to be executed directly. Use main.py or the CLI entry points.") 
