from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import platform
from browser_config import configurar_driver

def extrair_dados_nutricionais(url, driver):
    """Extrai os dados nutricionais de uma URL específica."""
    try:
        print(f"\nProcessando URL: {url}")
        driver.get(url)
        time.sleep(5)  # Aguardar carregamento da página

        # Extrair o nome do produto
        nome_produto = driver.find_element(By.TAG_NAME, "h1").text
        print(f"Nome do produto: {nome_produto}")

        # Inicializar dicionário de dados
        dados = {
            'URL': url,
            'Nome': nome_produto,
            'Valor energético': None,
            'Carboidratos': None,
            'Proteínas': None,
            'Gorduras totais': None,
            'Gorduras saturadas': None,
            'Fibra alimentar': None,
            'Sódio': None,
            'Açúcares': None
        }

        # Tentar expandir a tabela nutricional usando JavaScript
        try:
            script = """
            var buttons = document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].textContent.toLowerCase().includes('tabela nutricional')) {
                    buttons[i].click();
                    return true;
                }
            }
            return false;
            """
            driver.execute_script(script)
            time.sleep(2)  # Aguardar a expansão da tabela
        except Exception as e:
            print(f"Aviso: Não foi possível expandir a tabela: {e}")

        # Tentar extrair dados do objeto window.digitalData primeiro
        try:
            script = """
            if (window.digitalData && window.digitalData.product && window.digitalData.product.nutritionalMap) {
                return window.digitalData.product.nutritionalMap;
            }
            return null;
            """
            dados_js = driver.execute_script(script)
            
            if dados_js and 'attributes' in dados_js:
                print("Dados encontrados via JavaScript!")
                for item in dados_js['attributes']:
                    label = item.get('label', '').lower()
                    valor = item.get('value', '')
                    
                    if "energético" in label or "calor" in label:
                        dados['Valor energético'] = valor
                    elif "carboidrato" in label:
                        dados['Carboidratos'] = valor
                    elif "proteína" in label:
                        dados['Proteínas'] = valor
                    elif "gorduras totais" in label:
                        dados['Gorduras totais'] = valor
                    elif "gorduras saturadas" in label:
                        dados['Gorduras saturadas'] = valor
                    elif "fibra" in label:
                        dados['Fibra alimentar'] = valor
                    elif "sódio" in label:
                        dados['Sódio'] = valor
                    elif "açúcar" in label:
                        dados['Açúcares'] = valor
                    
                    if valor:
                        print(f"Item encontrado via JS: {label} = {valor}")
        except Exception as e:
            print(f"Aviso: Não foi possível extrair dados via JavaScript: {e}")

        # Se não encontrou via JavaScript, tentar pela tabela HTML
        if all(v is None for v in dados.values() if v != url and v != nome_produto):
            print("Tentando extrair dados da tabela HTML...")
            tabelas = driver.find_elements(By.TAG_NAME, "table")
            for tabela in tabelas:
                # Verificar se é a tabela nutricional
                cabecalho = tabela.find_elements(By.TAG_NAME, "th")
                if any("QTDE. POR PORÇÃO" in th.text.upper() for th in cabecalho):
                    print("Tabela nutricional encontrada!")
                    linhas = tabela.find_elements(By.TAG_NAME, "tr")
                    for linha in linhas:
                        try:
                            colunas = linha.find_elements(By.TAG_NAME, "td")
                            if len(colunas) >= 2:
                                item = colunas[0].text.strip().lower()
                                valor = colunas[1].text.strip()
                                
                                if "energético" in item or "calor" in item:
                                    dados['Valor energético'] = valor
                                elif "carboidrato" in item:
                                    dados['Carboidratos'] = valor
                                elif "proteína" in item:
                                    dados['Proteínas'] = valor
                                elif "gorduras totais" in item:
                                    dados['Gorduras totais'] = valor
                                elif "gorduras saturadas" in item:
                                    dados['Gorduras saturadas'] = valor
                                elif "fibra" in item:
                                    dados['Fibra alimentar'] = valor
                                elif "sódio" in item:
                                    dados['Sódio'] = valor
                                elif "açúcar" in item:
                                    dados['Açúcares'] = valor
                                
                                if valor:
                                    print(f"Item encontrado via HTML: {item} = {valor}")
                        except Exception as e:
                            print(f"Erro ao processar linha: {e}")
                            continue

        print("Dados extraídos com sucesso!")
        return dados

    except Exception as e:
        print(f"Erro ao processar a URL {url}: {e}")
        return None

def processar_urls(urls):
    """Processa uma lista de URLs e salva os resultados em um CSV."""
    driver = configurar_driver()
    dados_todos = []
    
    try:
        for url in urls:
            dados = extrair_dados_nutricionais(url, driver)
            if dados:
                dados_todos.append(dados)
        
        if dados_todos:
            df = pd.DataFrame(dados_todos)
            df.to_csv('dados_nutricionais.csv', index=False)
            print("\nDados salvos com sucesso em dados_nutricionais.csv!")
    finally:
        driver.quit()

# URLs para teste
urls_teste = [
    "https://www.paodeacucar.com/produto/495095/espumante-italiano-mionetinto-proscecco-750ml",
    "https://www.paodeacucar.com/produto/460707/aveia-em-flocos-finos-quaker-caixa-450g-embalagem-economica",
    "https://www.paodeacucar.com/produto/174187/uramaki-de-salmao-8-pecas-(aprox--196g)"
]

if __name__ == "__main__":
    processar_urls(urls_teste) 