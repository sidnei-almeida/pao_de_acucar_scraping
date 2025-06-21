from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import json
from datetime import datetime
import platform
from browser_config import configurar_driver

def scroll_ate_o_fim(driver, max_scrolls=None):
    """Rola a página até o fim para carregar todos os produtos."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    num_scrolls = 0
    
    while True:
        # Se atingiu o número máximo de scrolls, para
        if max_scrolls and num_scrolls >= max_scrolls:
            print("Número máximo de scrolls atingido")
            break
            
        # Rola até o fim da página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Espera o carregamento
        time.sleep(2)
        
        # Calcula a nova altura
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # Se a altura não mudou, chegamos ao fim
        if new_height == last_height:
            break
            
        last_height = new_height
        num_scrolls += 1
        print(f"Rolando a página... (scroll {num_scrolls})")

def extrair_urls_produtos(driver, max_urls=None):
    """Extrai todas as URLs dos produtos da página atual."""
    urls = []
    produtos = driver.find_elements(By.CSS_SELECTOR, "a[href*='/produto/']")
    
    for produto in produtos:
        try:
            url = produto.get_attribute('href')
            if url and '/produto/' in url and url not in urls:
                urls.append(url)
                print(f"URL encontrada: {url}")
                
                # Se atingiu o número máximo de URLs, para
                if max_urls and len(urls) >= max_urls:
                    print(f"Número máximo de URLs atingido ({max_urls})")
                    break
        except Exception as e:
            print(f"Erro ao extrair URL: {e}")
            continue
    
    return urls

def coletar_urls_categoria(url_categoria, categoria_nome, max_paginas=None, max_urls_por_pagina=None, max_scrolls=None):
    """Coleta todas as URLs dos produtos de uma categoria."""
    driver = configurar_driver()
    todas_urls = []
    pagina = 1
    
    try:
        while True:
            # Se atingiu o número máximo de páginas, para
            if max_paginas and pagina > max_paginas:
                print(f"Número máximo de páginas atingido ({max_paginas})")
                break
                
            url_paginada = f"{url_categoria}&p={pagina}"
            print(f"\nProcessando página {pagina}: {url_paginada}")
            
            driver.get(url_paginada)
            time.sleep(3)  # Aguarda carregamento inicial
            
            # Rola até o fim para carregar todos os produtos
            scroll_ate_o_fim(driver, max_scrolls)
            
            # Extrai URLs dos produtos
            urls_pagina = extrair_urls_produtos(driver, max_urls_por_pagina)
            
            if not urls_pagina:  # Se não encontrou produtos, chegamos ao fim
                break
                
            # Adiciona informações extras para cada URL
            urls_com_info = [
                {
                    'url': url,
                    'categoria': categoria_nome,
                    'pagina': pagina,
                    'data_coleta': datetime.now().isoformat()
                }
                for url in urls_pagina
            ]
            
            todas_urls.extend(urls_com_info)
            print(f"Total de URLs encontradas até agora: {len(todas_urls)}")
            
            pagina += 1
            
    except Exception as e:
        print(f"Erro ao processar categoria: {e}")
    finally:
        driver.quit()
    
    return todas_urls

def salvar_dados(dados, prefixo=''):
    """Salva os dados em CSV e JSON."""
    # Cria DataFrame para CSV
    df = pd.DataFrame(dados)
    csv_file = f'{prefixo}urls.csv'
    df.to_csv(csv_file, index=False)
    print(f"\nURLs salvas em {csv_file}")
    
    # Cria estrutura de dados para JSON
    dados_json = {
        'metadata': {
            'total_urls': len(dados),
            'data_extracao': datetime.now().isoformat(),
            'categorias': list(set(d['categoria'] for d in dados))
        },
        'urls': dados
    }
    
    # Salva JSON
    json_file = f'{prefixo}urls.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(dados_json, f, ensure_ascii=False, indent=2)
    print(f"URLs salvas em {json_file}")

def teste_rapido():
    """Função para teste rápido do coletor de URLs."""
    print("Iniciando teste rápido...")
    
    categorias = {
        'alimentos_refrigerados': 'https://www.paodeacucar.com/categoria/alimentos/alimentos-refrigerados?s=relevance',
        'doces_sobremesas': 'https://www.paodeacucar.com/categoria/alimentos/doces-e-sobremesas?s=relevance'
    }
    
    # Configurações de teste
    max_paginas = 2        # 2 páginas por categoria
    max_urls_por_pagina = 25  # 25 URLs por página (25 * 2 páginas * 2 categorias = 100 URLs no máximo)
    max_scrolls = 3        # 3 scrolls por página
    
    todas_urls = []
    
    for nome, url in categorias.items():
        print(f"\nTestando categoria: {nome}")
        urls_categoria = coletar_urls_categoria(
            url,
            categoria_nome=nome,
            max_paginas=max_paginas,
            max_urls_por_pagina=max_urls_por_pagina,
            max_scrolls=max_scrolls
        )
        todas_urls.extend(urls_categoria)
        
        # Salva os dados desta categoria separadamente
        salvar_dados(urls_categoria, prefixo=f'teste_{nome}_')
        
        # Se já atingiu 100 URLs no total, para
        if len(todas_urls) >= 100:
            print("Limite de 100 URLs atingido!")
            break
    
    # Salva todos os dados em um único arquivo
    salvar_dados(todas_urls, prefixo='teste_todas_')
    print(f"\nTeste concluído! Total de URLs únicas coletadas: {len(set(d['url'] for d in todas_urls))}")

def coletar_todas_urls():
    """Função para coletar todas as URLs sem limitações."""
    print("Iniciando coleta completa de URLs...")
    
    categorias = {
        'alimentos_refrigerados': 'https://www.paodeacucar.com/categoria/alimentos/alimentos-refrigerados?s=relevance',
        'doces_sobremesas': 'https://www.paodeacucar.com/categoria/alimentos/doces-e-sobremesas?s=relevance'
    }
    
    todas_urls = []
    
    for nome, url in categorias.items():
        print(f"\nColetando URLs da categoria: {nome}")
        urls_categoria = coletar_urls_categoria(url, categoria_nome=nome)
        todas_urls.extend(urls_categoria)
        
        # Salva os dados desta categoria separadamente
        salvar_dados(urls_categoria, prefixo=f'{nome}_')
    
    # Salva todos os dados em um único arquivo
    salvar_dados(todas_urls)
    print(f"\nTotal de URLs únicas coletadas: {len(set(d['url'] for d in todas_urls))}")

if __name__ == "__main__":
    # Executa o teste rápido
    teste_rapido()
    
    # Para coletar todas as URLs, descomente a linha abaixo:
    # coletar_todas_urls() 