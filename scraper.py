from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from browser_config import configurar_driver
from scraping_log import logger
import time
from datetime import datetime
import re
import numpy as np
import logging
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'scraping_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)

class Scraper:
    def __init__(self):
        self.driver = None
    
    def inicializar_driver(self):
        """Inicializa o driver do navegador."""
        if not self.driver:
            self.driver = configurar_driver()
        return self.driver
    
    def fechar_driver(self):
        """Fecha o driver do navegador."""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def extrair_nome_da_url(self, url):
        """Extrai o nome do produto da URL."""
        try:
            # Pega a última parte da URL após a última barra
            nome = url.split('/')[-1]
            # Remove qualquer parâmetro de query
            nome = nome.split('?')[0]
            # Substitui hífens por espaços
            nome = nome.replace('-', ' ')
            return nome.strip()
        except:
            return "Nome não encontrado"

    def extrair_valor_numerico(self, texto):
        """Extrai apenas o valor numérico e a unidade de um texto."""
        if not texto or texto == "Sem informação":
            return texto
        
        # Remove espaços extras e caracteres especiais
        texto = texto.strip()
        
        # Tenta extrair número e unidade
        match = re.search(r'([\d,.]+)\s*([a-zA-Z%]+)?', texto)
        if match:
            numero = match.group(1)
            unidade = match.group(2) if match.group(2) else ''
            return f"{numero}{unidade}"
        
        return texto

    def extrair_dados_nutricionais(self, url):
        """Extrai dados nutricionais de um produto usando JavaScript."""
        try:
            if not self.driver:
                self.inicializar_driver()

            logger.info(f"Processando URL: {url}")
            self.driver.get(url)
            time.sleep(10)  # Espera a página carregar

            # Executa o JavaScript para extrair os dados
            resultado = self.driver.execute_script("""
                // Mapeamento de nomes alternativos para nomes padronizados
                const mapaNomes = {
                    'valor calórico': 'calorias',
                    'valor energético': 'calorias',
                    'calorias': 'calorias',
                    'energia': 'calorias',
                    'kcal': 'calorias',
                    'carboidrato': 'carboidratos',
                    'carboidratos totais': 'carboidratos',
                    'carboidratos': 'carboidratos',
                    'proteína': 'proteinas',
                    'proteínas': 'proteinas',
                    'gordura total': 'gorduras',
                    'gorduras totais': 'gorduras',
                    'gordura': 'gorduras',
                    'gorduras': 'gorduras',
                    'gordura saturada': 'gorduras_saturadas',
                    'gorduras saturadas': 'gorduras_saturadas',
                    'fibra': 'fibras',
                    'fibras': 'fibras',
                    'fibra alimentar': 'fibras',
                    'fibras alimentares': 'fibras',
                    'sódio': 'sodio',
                    'açúcar': 'acucares',
                    'açúcares': 'acucares',
                    'açucares': 'acucares',
                    'acucar': 'acucares',
                    'açucar': 'acucares'
                };

                // Função para padronizar o nome do item
                function padronizarNome(nome) {
                    nome = nome.toLowerCase().trim();
                    return mapaNomes[nome] || nome;
                }

                // Função para extrair apenas o valor numérico
                function extrairValorNumerico(texto) {
                    const match = texto.match(/(\\d+[,.]?\\d*)/);
                    if (match) {
                        // Substitui vírgula por ponto para garantir formato numérico
                        return match[1].replace(',', '.');
                    }
                    return "0";
                }

                // Extrai o nome do produto
                const nome = document.querySelector('h1')?.textContent?.trim() || "Sem informação";

                // Extrai a porção
                let porcao = "0";
                const elementos = document.querySelectorAll('*');
                for (const elemento of elementos) {
                    const texto = elemento.textContent;
                    if (texto.toLowerCase().includes('porção') || texto.toLowerCase().includes('porcao')) {
                        console.log('Texto com porção:', texto);
                        const match = texto.match(/[Pp]or[cç][aã]o\\s+(?:de\\s+)?(\\d+)\\s*(?:g|G|gr|GR|grama|gramas|GRAMAS)(?:\\s*[-]\\s*.*)?/);
                        if (match) {
                            porcao = match[1];
                            console.log('Porção encontrada:', porcao);
                            break;
                        }
                    }
                }

                // Inicializa dados com valores zerados
                const dados = {
                    nome: nome,
                    url: window.location.href,
                    porcao: porcao,
                    calorias: "0",
                    carboidratos: "0",
                    proteinas: "0",
                    gorduras: "0",
                    gorduras_saturadas: "0",
                    fibras: "0",
                    acucares: "0",
                    sodio: "0"
                };

                // Procura por tabelas e elementos que podem conter informações nutricionais
                document.querySelectorAll('table').forEach(tabela => {
                    const linhas = tabela.querySelectorAll('tr');
                    linhas.forEach(linha => {
                        const colunas = linha.querySelectorAll('td, th');
                        if (colunas.length >= 2) {
                            const textoColuna = colunas[0].textContent.trim();
                            const valorColuna = colunas[1].textContent.trim();
                            
                            Object.keys(mapaNomes).forEach(nomeAlternativo => {
                                if (textoColuna.toLowerCase().includes(nomeAlternativo.toLowerCase())) {
                                    const nomePadronizado = padronizarNome(nomeAlternativo);
                                    const valorNumerico = extrairValorNumerico(valorColuna);
                                    if (valorNumerico !== "0") {
                                        dados[nomePadronizado] = valorNumerico;
                                    }
                                }
                            });
                        }
                    });
                });

                // Procura também por elementos de texto
                document.querySelectorAll('*').forEach(elemento => {
                    const texto = elemento.textContent?.trim();
                    if (!texto) return;

                    Object.keys(mapaNomes).forEach(nomeAlternativo => {
                        if (texto.toLowerCase().includes(nomeAlternativo.toLowerCase())) {
                            const padrao = new RegExp(`${nomeAlternativo}[:\\s]*(\\d+[,.]?\\d*)`, 'i');
                            const match = texto.match(padrao);
                            if (match) {
                                const valorNumerico = match[1].replace(',', '.');
                                const nomePadronizado = padronizarNome(nomeAlternativo);
                                if (dados[nomePadronizado] === "0") {
                                    dados[nomePadronizado] = valorNumerico;
                                }
                            }
                        }
                    });
                });

                console.log("Dados extraídos:", dados);
                return dados;
            """)

            if resultado:
                logger.info(f"Dados extraídos com sucesso para: {resultado['nome']}")
                logger.info("Dados nutricionais:")
                for chave, valor in resultado.items():
                    if chave not in ['nome', 'url']:
                        logger.info(f"{chave}: {valor}")
                return resultado
            else:
                logger.error(f"Não foi possível extrair dados da URL {url}")
                return None

        except Exception as e:
            logger.error(f"Erro ao processar URL {url}: {str(e)}")
            return None

    def processar_arquivo_urls(self, arquivo_urls):
        """
        Processa um arquivo CSV contendo URLs dos produtos.
        
        Args:
            arquivo_urls (str): Caminho para o arquivo CSV com as URLs
        """
        try:
            # Lê o arquivo de URLs
            df_urls = pd.read_csv(arquivo_urls)
            total_produtos = len(df_urls)
            logging.info(f"Iniciando coleta de dados para {total_produtos} produtos")
            
            # Lista para armazenar os dados coletados
            dados_coletados = []
            
            # Configura e abre o navegador
            driver = self.inicializar_driver()
            
            # Processa cada URL
            for idx, row in df_urls.iterrows():
                try:
                    url = row['url']
                    nome = row['nome']
                    
                    # Log detalhado do progresso
                    logging.info(f"Coletando dados do produto: {nome} ({idx + 1} de {total_produtos})")
                    
                    # Acessa a URL do produto
                    driver.get(url)
                    time.sleep(3)  # Espera o carregamento
                    
                    # Coleta os dados nutricionais
                    dados = self.extrair_dados_nutricionais(url)
                    if dados:
                        dados['URL'] = url
                        dados['NOME_PRODUTO'] = nome
                        dados_coletados.append(dados)
                        
                except Exception as e:
                    logging.error(f"Erro ao processar produto {nome}: {str(e)}")
                    continue
            
            # Fecha o navegador
            self.fechar_driver()
            
            # Cria o DataFrame com os dados coletados
            if dados_coletados:
                df_dados = pd.DataFrame(dados_coletados)
                
                # Salva os dados
                modo_arquivo = 'a' if os.path.exists('dados_nutricionais.csv') else 'w'
                df_dados.to_csv('dados_nutricionais.csv', mode=modo_arquivo, header=(modo_arquivo == 'w'), index=False)
                
                logging.info(f"Dados coletados com sucesso para {len(dados_coletados)} produtos")
            else:
                logging.warning("Nenhum dado foi coletado")
                
        except Exception as e:
            logging.error(f"Erro ao processar arquivo de URLs: {str(e)}")
            raise e

if __name__ == "__main__":
    logger.info("Este arquivo não deve ser executado diretamente. Use o main.py")

def processar_urls(urls, limite_teste=None):
    """Processa uma lista de URLs para extrair dados nutricionais."""
    logger.info(f"Iniciando processamento de URLs...")
    
    dados_nutricionais = []
    driver = configurar_driver()
    
    try:
        # Se limite_teste for especificado, limita o número de URLs
        urls_processar = urls[:limite_teste] if limite_teste else urls
        
        for url_info in urls_processar:
            url = url_info['url'] if isinstance(url_info, dict) else url_info
            dados = extrair_dados_nutricionais(url, driver)
            
            if dados:
                if isinstance(url_info, dict):
                    dados['categoria'] = url_info.get('categoria', '')
                dados_nutricionais.append(dados)
        
        # Cria DataFrame e salva em CSV
        if dados_nutricionais:
            df = pd.DataFrame(dados_nutricionais)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"dados_nutricionais_{timestamp}.csv"
            df.to_csv(nome_arquivo, index=False)
            logger.info(f"Dados salvos em {nome_arquivo}")
            
    except Exception as e:
        logger.error(f"Erro durante o processamento: {str(e)}")
    finally:
        driver.quit()
    
    return dados_nutricionais

def teste_url():
    """Função para testar o scraper com uma única URL."""
    url_teste = "https://www.paodeacucar.com/produto/298933/leite-condensado-moca-lata-395g"
    driver = configurar_driver()
    try:
        dados = extrair_dados_nutricionais(url_teste, driver)
        print("\nDados extraídos:")
        for chave, valor in dados.items():
            print(f"{chave}: {valor}")
    finally:
        driver.quit()

# URLs para teste
urls_teste = [
    "https://www.paodeacucar.com/produto/495095/espumante-italiano-mionetinto-proscecco-750ml",
    "https://www.paodeacucar.com/produto/460707/aveia-em-flocos-finos-quaker-caixa-450g-embalagem-economica",
    "https://www.paodeacucar.com/produto/174187/uramaki-de-salmao-8-pecas-(aprox--196g)",
    "https://www.paodeacucar.com/produto/339743/queijo-mussarela-fatiado-president-150g",
    "https://www.paodeacucar.com/produto/106824/queijo-mussarela-importado-fatiado-150g"
]

def teste_url_especifica():
    """Função para testar a extração de dados de uma URL específica."""
    url = "https://www.paodeacucar.com/produto/1376996/queijo-minas-padrao-vegetal-vida-veg-200g"
    driver = configurar_driver()
    
    try:
        print("\nTestando URL específica...")
        driver.get(url)
        time.sleep(5)  # Aguardar carregamento da página
        
        # Tentar encontrar a porção diretamente
        script = """
        function encontrarPorcao() {
            // Tenta encontrar o elemento h2 com texto "Tabela nutricional"
            let elementos = document.evaluate(
                "//h2[contains(text(), 'Tabela nutricional')]",
                document,
                null,
                XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
                null
            );
            
            if (elementos.snapshotLength > 0) {
                let tituloTabela = elementos.snapshotItem(0);
                let elementoPai = tituloTabela.parentElement;
                
                // Procura por todos os elementos de texto dentro do pai
                let textos = [];
                let walker = document.createTreeWalker(
                    elementoPai,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );
                
                let node;
                while (node = walker.nextNode()) {
                    textos.push(node.textContent.trim());
                }
                
                // Procura por um texto que começa com "Porção"
                for (let texto of textos) {
                    if (texto.startsWith('Porção')) {
                        console.log("Porção encontrada:", texto);
                        return texto;
                    }
                }
            }
            
            // Se não encontrou, tenta outros seletores
            let seletores = [
                'div[class*="portion"]',
                'div[class*="porcao"]',
                'p[class*="portion"]',
                'p[class*="porcao"]',
                'span[class*="portion"]',
                'span[class*="porcao"]'
            ];
            
            for (let seletor of seletores) {
                let elementos = document.querySelectorAll(seletor);
                for (let elem of elementos) {
                    let texto = elem.textContent.trim();
                    if (texto.startsWith('Porção')) {
                        console.log("Porção encontrada via seletor:", texto);
                        return texto;
                    }
                }
            }
            
            // Última tentativa: procura por qualquer elemento com texto começando com "Porção"
            let todosElementos = document.evaluate(
                "//*[starts-with(text(), 'Porção')]",
                document,
                null,
                XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
                null
            );
            
            if (todosElementos.snapshotLength > 0) {
                let texto = todosElementos.snapshotItem(0).textContent.trim();
                console.log("Porção encontrada via XPath geral:", texto);
                return texto;
            }
            
            return null;
        }
        return encontrarPorcao();
        """
        
        porcao = driver.execute_script(script)
        print(f"\nPorção encontrada: {porcao}")
        
        # Agora vamos tentar expandir a tabela nutricional
        try:
            script_expandir = """
            var buttons = document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].textContent.toLowerCase().includes('tabela nutricional')) {
                    buttons[i].click();
                    return true;
                }
            }
            return false;
            """
            driver.execute_script(script_expandir)
            time.sleep(2)  # Aguardar a expansão da tabela
            
            # Tenta encontrar a porção novamente após expandir
            porcao_apos_expandir = driver.execute_script(script)
            print(f"Porção após expandir tabela: {porcao_apos_expandir}")
            
        except Exception as e:
            print(f"Erro ao expandir tabela: {e}")
        
    except Exception as e:
        print(f"Erro ao testar URL: {e}")
    finally:
        driver.quit()

def testar_url_margarina():
    """Função para testar a extração de dados da margarina Qualy."""
    url = "https://www.paodeacucar.com/produto/71812/margarina-cremosa-com-sal-qualy-pote-500g"
    driver = configurar_driver()
    
    try:
        dados = extrair_dados_nutricionais(url, driver)
        if dados:
            print("\nDados extraídos da margarina Qualy:")
            for chave, valor in dados.items():
                print(f"{chave}: {valor}")
        else:
            print("Não foi possível extrair os dados")
    finally:
        driver.quit()

def testar_salvamento_csv():
    """Função para testar o salvamento dos dados em CSV."""
    url = "https://www.paodeacucar.com/produto/71812/margarina-cremosa-com-sal-qualy-pote-500g"
    
    # Cria uma lista com a URL de teste
    urls = [{
        'url': url,
        'categoria': 'alimentos_refrigerados',
        'pagina': 1,
        'data_coleta': pd.Timestamp.now().isoformat()
    }]
    
    # Processa a URL e obtém o DataFrame
    df = processar_urls(urls)
    
    if df is not None:
        # Salva em CSV
        nome_arquivo = 'teste_dados_nutricionais_margarina.csv'
        df.to_csv(nome_arquivo, index=False)
        print(f"\nDados salvos em {nome_arquivo}")
        print("\nConteúdo do arquivo CSV:")
        print(df.to_string())
    else:
        print("Não foi possível criar o DataFrame")

def testar_produtos_especificos():
    """Função para testar a extração de dados de produtos específicos."""
    urls = [
        "https://www.paodeacucar.com/produto/66261/queijo-minas-frescal-fazenda-bela-vista-500g",
        "https://www.paodeacucar.com/produto/66262/queijo-mussarela-tirolez-fatiado-bandeja-150g"
    ]
    
    driver = configurar_driver()
    try:
        for url in urls:
            dados = extrair_dados_nutricionais(url, driver)
            if dados:
                print(f"\nDados extraídos do produto {dados.get('nome', 'Desconhecido')}:")
                print(f"Porção: {dados.get('porcao', 'Não encontrada')}")
                print("Dados nutricionais:")
                for chave, valor in dados.items():
                    if chave not in ['url', 'nome', 'porcao']:
                        print(f"{chave}: {valor}")
            else:
                print(f"\nNão foi possível extrair os dados da URL: {url}")
    finally:
        driver.quit()

def testar_url_queijo():
    """Função para testar a extração de dados do queijo mussarela."""
    url = "https://www.paodeacucar.com/produto/339743/queijo-mussarela-fatiado-president-150g"
    driver = configurar_driver()
    try:
        print("\nTestando URL do queijo mussarela Président...")
        dados = extrair_dados_nutricionais(url, driver)
        if dados:
            print("\nDados extraídos da tabela nutricional:")
            print("-" * 50)
            for chave, valor in dados.items():
                print(f"{chave}: {valor}")
        else:
            print("Não foi possível extrair os dados")
    except Exception as e:
        print(f"Erro ao processar URL: {str(e)}")
    finally:
        driver.quit()

def testar_url_president():
    """Testa a extração de dados nutricionais para o queijo mussarela Président."""
    logger.info("Iniciando teste com queijo mussarela Président...")
    url = "https://www.paodeacucar.com/produto/339743/queijo-mussarela-fatiado-president-150g"
    
    driver = configurar_driver()
    try:
        dados = extrair_dados_nutricionais(url, driver)
        if dados:
            # Salva os dados em um arquivo CSV
            df = pd.DataFrame([dados])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"dados_nutricionais_{timestamp}.csv"
            df.to_csv(nome_arquivo, index=False)
            logger.info(f"Dados salvos em {nome_arquivo}")
        else:
            logger.error("Não foi possível extrair os dados")
    finally:
        driver.quit()

if __name__ == "__main__":
    # URLs de teste
    urls_teste = [
        "https://www.paodeacucar.com/produto/339743/queijo-mussarela-fatiado-president-150g",
        "https://www.paodeacucar.com/produto/106824/queijo-mussarela-importado-fatiado-150g"
    ]

    # Cria DataFrame vazio com as colunas necessárias e suas unidades
    colunas = [
        'nome',
        'url', 
        'porcao (g)',
        'calorias (kcal)',
        'carboidratos (g)',
        'proteinas (g)',
        'gorduras (g)',
        'gorduras_saturadas (g)',
        'fibras (g)',
        'acucares (g)',
        'sodio (mg)'
    ]

    # Mapeamento de colunas para suas unidades padrão
    unidades_padrao = {
        'porcao': 'g',
        'calorias': 'kcal',
        'carboidratos': 'g',
        'proteinas': 'g',
        'gorduras': 'g',
        'gorduras_saturadas': 'g',
        'fibras': 'g',
        'acucares': 'g',
        'sodio': 'mg'
    }

    df_produtos = pd.DataFrame(columns=colunas)

    # Configura o driver
    driver = configurar_driver()

    try:
        # Testa as URLs
        print("\nTestando URLs dos queijos...")
        for url in urls_teste:
            logger.info(f"Processando URL: {url}")
            try:
                dados = extrair_dados_nutricionais(url, driver)
                if dados:
                    logger.info(f"Dados extraídos com sucesso para: {dados['nome']}")
                    logger.info("Dados nutricionais:")
                    
                    # Converte valores para as unidades padrão
                    for campo, unidade in unidades_padrao.items():
                        valor = dados.get(campo, "0")
                        # Remove a unidade atual se existir
                        if isinstance(valor, str):
                            valor = re.sub(r'[a-zA-Z]+$', '', valor).strip()
                        try:
                            valor_numerico = float(str(valor).replace(',', '.'))
                            
                            # Converte mg para g se necessário
                            if unidade == 'g' and 'mg' in str(valor).lower():
                                valor_numerico = valor_numerico / 1000
                            
                            # Converte g para mg se necessário
                            if unidade == 'mg' and 'g' in str(valor).lower() and 'mg' not in str(valor).lower():
                                valor_numerico = valor_numerico * 1000
                            
                            dados[campo] = valor_numerico
                        except (ValueError, TypeError):
                            dados[campo] = 0
                    
                    # Renomeia as chaves para incluir unidades
                    dados_com_unidades = {
                        'nome': dados['nome'],
                        'url': dados['url'],
                        'porcao (g)': dados['porcao'],
                        'calorias (kcal)': dados['calorias'],
                        'carboidratos (g)': dados['carboidratos'],
                        'proteinas (g)': dados['proteinas'],
                        'gorduras (g)': dados['gorduras'],
                        'gorduras_saturadas (g)': dados['gorduras_saturadas'],
                        'fibras (g)': dados['fibras'],
                        'acucares (g)': dados['acucares'],
                        'sodio (mg)': dados['sodio']
                    }
                    
                    # Adiciona os dados ao DataFrame
                    df_produtos = pd.concat([df_produtos, pd.DataFrame([dados_com_unidades])], ignore_index=True)
                    
                    print("\nDados extraídos da tabela nutricional:")
                    print("-" * 50)
                    for chave, valor in dados_com_unidades.items():
                        print(f"{chave}: {valor}")
            except Exception as e:
                logger.error(f"Erro ao processar URL {url}: {str(e)}")
        
        # Salva o DataFrame completo em CSV
        nome_arquivo = f"dados_nutricionais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_produtos.to_csv(nome_arquivo, index=False)
        logger.info(f"Dados salvos em {nome_arquivo}")

    finally:
        driver.quit()

    logger.info("Este arquivo não deve ser executado diretamente. Use o main.py") 