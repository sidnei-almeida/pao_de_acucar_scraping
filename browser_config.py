import platform
import os
import subprocess
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from scraping_log import logger

def detectar_navegador():
    """
    Detecta qual navegador está disponível no sistema.
    Retorna o tipo do navegador e o caminho do binário.
    """
    sistema = platform.system().lower()
    logger.info(f"Sistema operacional detectado: {sistema}")
    
    # Caminhos dos navegadores por sistema operacional
    navegadores = {
        'linux': {
            'chrome': [
                '/usr/bin/google-chrome',
                '/usr/bin/google-chrome-stable',
                '/usr/bin/google-chrome-beta',
                '/usr/bin/google-chrome-unstable',
                '/usr/local/bin/google-chrome',
                '/opt/google/chrome/google-chrome',
                '/snap/bin/chromium'
            ],
            'chromium': [
                '/usr/bin/chromium',
                '/usr/bin/chromium-browser',
                '/usr/bin/chromium-bsu',
                '/usr/local/bin/chromium',
                '/var/lib/snapd/snap/bin/chromium'
            ]
        },
        'windows': {
            'chrome': [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                r'C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe'.format(os.environ.get('USERNAME', '')),
                r'C:\Users\{}\AppData\Local\Google\Chrome SxS\Application\chrome.exe'.format(os.environ.get('USERNAME', ''))
            ],
            'chromium': [
                r'C:\Program Files\Chromium\Application\chrome.exe',
                r'C:\Program Files (x86)\Chromium\Application\chrome.exe',
                r'C:\Users\{}\AppData\Local\Chromium\Application\chrome.exe'.format(os.environ.get('USERNAME', ''))
            ]
        },
        'darwin': {  # macOS
            'chrome': [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
            ],
            'chromium': [
                '/Applications/Chromium.app/Contents/MacOS/Chromium'
            ]
        }
    }
    
    # Se o sistema não for reconhecido, usa as configurações padrão
    if sistema not in navegadores:
        logger.warning(f"Sistema {sistema} não reconhecido. Usando configurações padrão do Chrome.")
        return 'chrome', None
    
    # Verifica se é uma distribuição baseada em Arch/CachyOS
    if sistema == 'linux':
        try:
            with open('/etc/os-release', 'r') as f:
                os_info = f.read().lower()
                if 'arch' in os_info or 'cachyos' in os_info:
                    logger.info("Distribuição baseada em Arch/CachyOS detectada")
                    # Tenta Chromium primeiro em distribuições Arch
                    for path in navegadores[sistema]['chromium']:
                        if os.path.exists(path):
                            logger.info(f"Chromium encontrado em: {path}")
                            return 'chromium', path
        except Exception as e:
            logger.warning(f"Erro ao verificar distribuição Linux: {str(e)}")
    
    # Tenta encontrar navegadores na ordem de preferência
    for browser_type in ['chrome', 'chromium']:
        for path in navegadores[sistema][browser_type]:
            if os.path.exists(path):
                logger.info(f"Navegador encontrado: {browser_type} em {path}")
                return browser_type, path
    
    # Se nenhum navegador for encontrado, usa o Chrome como padrão
    logger.warning("Nenhum navegador encontrado. Usando Chrome como padrão.")
    return 'chrome', None

def verificar_driver_sistema():
    """
    Verifica se existe um driver no sistema antes de baixar.
    """
    sistema = platform.system().lower()
    drivers_possiveis = []
    
    if sistema == 'windows':
        drivers_possiveis = ['chromedriver.exe']
    else:
        drivers_possiveis = [
            'chromedriver',
            '/usr/bin/chromedriver',
            '/usr/local/bin/chromedriver'
        ]
    
    for driver_path in drivers_possiveis:
        if shutil.which(driver_path) or os.path.exists(driver_path):
            try:
                # Testa se o driver funciona
                result = subprocess.run([driver_path, '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    logger.info(f"Driver encontrado no sistema: {driver_path}")
                    logger.info(f"Versão: {result.stdout.strip()}")
                    return driver_path
            except Exception as e:
                logger.warning(f"Erro ao verificar driver {driver_path}: {e}")
                continue
    
    return None

def configurar_driver():
    """
    Configura e retorna uma instância do navegador usando webdriver-manager.
    Detecta automaticamente o navegador disponível e baixa o driver apropriado.
    """
    logger.info("Iniciando configuração do WebDriver...")
    
    # Detecta o navegador disponível
    browser_type, binary_location = detectar_navegador()
    
    # Verifica se existe driver no sistema
    driver_sistema = verificar_driver_sistema()
    
    # Configura as opções do navegador
    options = Options()
    opcoes_comuns = [
        "--headless=new",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--window-size=1920,1080",
        "--disable-gpu",
        "--disable-extensions",
        "--disable-dev-tools",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-blink-features=AutomationControlled",
        "--disable-setuid-sandbox",
        "--disable-software-rasterizer",
        "--disable-background-timer-throttling",
        "--disable-renderer-backgrounding",
        "--disable-backgrounding-occluded-windows",
        "--disable-features=TranslateUI",
        "--disable-ipc-flooding-protection",
        "--disable-hang-monitor",
        "--disable-popup-blocking",
        "--disable-prompt-on-repost",
        "--disable-sync",
        "--disable-web-security",
        "--disable-features=VizDisplayCompositor",
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ]
    
    for opcao in opcoes_comuns:
        options.add_argument(opcao)
    
    # Configurações específicas para ambiente de produção
    if os.environ.get('RENDER') or os.environ.get('HEROKU'):
        options.binary_location = "/usr/bin/google-chrome-stable"
    elif binary_location:
        options.binary_location = binary_location
    
    # Lista de tentativas para configurar o driver
    tentativas = []
    
    # Tentativa 1: Usar driver do sistema se disponível (prioridade alta)
    if driver_sistema:
        tentativas.append(('sistema', driver_sistema, 'chrome'))
    
    # Tentativa 2: Forçar uso do chromedriver padrão do sistema  
    tentativas.append(('sistema', '/usr/bin/chromedriver', 'chrome'))
    
    # Tentativa 3: Usar webdriver-manager para o navegador detectado
    tentativas.append(('webdriver-manager', None, browser_type))
    
    # Tentativa 4: Fallback para Chrome se não for Chrome
    if browser_type != 'chrome':
        tentativas.append(('webdriver-manager', None, 'chrome'))
    
    for i, (metodo, driver_path, tipo_navegador) in enumerate(tentativas, 1):
        try:
            logger.info(f"Tentativa {i}: {metodo} com {tipo_navegador}")
            
            if metodo == 'sistema':
                # Verifica se o driver existe antes de tentar usar
                if not os.path.exists(driver_path):
                    raise Exception(f"Driver não encontrado em: {driver_path}")
                
                # Usa explicitamente o chromedriver do sistema
                service = Service(executable_path=driver_path)
                driver = webdriver.Chrome(service=service, options=options)
            else:  # webdriver-manager
                # Tenta baixar e configurar o driver automaticamente
                try:
                    # Primeiro tenta com o tipo específico detectado
                    if tipo_navegador == 'chromium':
                        chrome_type = ChromeType.CHROMIUM
                    else:
                        chrome_type = ChromeType.GOOGLE
                    
                    # Configura o webdriver manager com cache
                    driver_manager = ChromeDriverManager(chrome_type=chrome_type)
                    driver_path = driver_manager.install()
                    
                    # Verifica se o driver baixado é válido
                    if os.path.exists(driver_path):
                        service = Service(executable_path=driver_path)
                        driver = webdriver.Chrome(service=service, options=options)
                    else:
                        raise Exception(f"Driver baixado não encontrado em: {driver_path}")
                        
                except Exception as inner_e:
                    # Se falhar, tenta com o tipo padrão
                    logger.warning(f"Erro com {chrome_type}, tentando com GOOGLE: {inner_e}")
                    driver_manager = ChromeDriverManager(chrome_type=ChromeType.GOOGLE)
                    driver_path = driver_manager.install()
                    service = Service(executable_path=driver_path)
                    driver = webdriver.Chrome(service=service, options=options)
            
            # Testa se o driver funciona
            driver.get("data:text/html,<html><body><h1>Teste</h1></body></html>")
            logger.info(f"WebDriver configurado com sucesso usando {metodo} com {tipo_navegador}")
            return driver
            
        except Exception as e:
            logger.warning(f"Falha na tentativa {i} ({metodo} com {tipo_navegador}): {str(e)}")
            try:
                if 'driver' in locals():
                    driver.quit()
            except:
                pass
            continue
    
    # Se todas as tentativas falharam
    logger.error("Falha ao configurar WebDriver com todas as tentativas")
    raise Exception("Não foi possível configurar o WebDriver. Verifique se Chrome ou Chromium estão instalados.") 