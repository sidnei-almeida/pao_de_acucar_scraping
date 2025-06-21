import platform
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

def detectar_navegador():
    """
    Detecta o sistema operacional e o navegador disponível (Chrome ou Chromium).
    Retorna o caminho do binário e o tipo do navegador.
    """
    sistema = platform.system().lower()
    
    # No Linux, verifica se é CachyOS ou outra distribuição baseada em Arch
    if sistema == 'linux':
        try:
            with open('/etc/os-release', 'r') as f:
                os_info = f.read().lower()
                if 'cachyos' in os_info or 'arch' in os_info:
                    # No CachyOS/Arch, Chromium é o padrão
                    if os.path.exists('/usr/bin/chromium'):
                        return '/usr/bin/chromium', 'chromium'
        except:
            pass
    
    # Caminhos comuns para os navegadores
    caminhos_chromium = {
        'linux': [
            '/usr/bin/chromium',
            '/usr/bin/chromium-browser'
        ],
        'windows': [
            r'C:\Program Files\Chromium\Application\chrome.exe',
            r'C:\Program Files (x86)\Chromium\Application\chrome.exe'
        ],
        'darwin': [
            '/Applications/Chromium.app/Contents/MacOS/Chromium'
        ]
    }
    
    caminhos_chrome = {
        'linux': [
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable'
        ],
        'windows': [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        ],
        'darwin': [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        ]
    }
    
    # No Linux, verifica Chromium primeiro
    if sistema == 'linux':
        # Verifica Chromium primeiro no Linux
        if sistema in caminhos_chromium:
            for caminho in caminhos_chromium[sistema]:
                if os.path.exists(caminho):
                    return caminho, 'chromium'
        
        # Se não encontrar Chromium, tenta Chrome
        if sistema in caminhos_chrome:
            for caminho in caminhos_chrome[sistema]:
                if os.path.exists(caminho):
                    return caminho, 'chrome'
    else:
        # Em outros sistemas, verifica Chrome primeiro
        if sistema in caminhos_chrome:
            for caminho in caminhos_chrome[sistema]:
                if os.path.exists(caminho):
                    return caminho, 'chrome'
        
        # Se não encontrar Chrome, tenta Chromium
        if sistema in caminhos_chromium:
            for caminho in caminhos_chromium[sistema]:
                if os.path.exists(caminho):
                    return caminho, 'chromium'
    
    # Se nenhum navegador for encontrado nos caminhos padrão,
    # no Linux assume Chromium, em outros sistemas assume Chrome
    return None, 'chromium' if sistema == 'linux' else 'chrome'

def configurar_driver():
    """
    Configura e retorna uma instância do Chromium usando o chromium-driver do sistema.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/chromium"
    
    # No Arch/CachyOS, o ChromeDriver está instalado em /usr/bin/chromedriver
    service = Service('/usr/bin/chromedriver')
    
    # Cria e retorna o driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1920, 1080)
    
    print("Usando Chromium com ChromeDriver do sistema")
    return driver 