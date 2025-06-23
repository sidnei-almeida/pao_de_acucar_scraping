import platform
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.opera import OperaDriverManager

def get_chrome_version(binary_path):
    """
    Tenta obter a versão do Chrome/Chromium/Opera usando o binário especificado.
    """
    try:
        if platform.system().lower() == 'windows':
            import winreg
            # Tenta diferentes caminhos de registro para diferentes navegadores
            registry_paths = [
                (winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon'),
                (winreg.HKEY_CURRENT_USER, r'Software\Opera Software\Opera GX Stable'),
                (winreg.HKEY_CURRENT_USER, r'Software\Opera Software\Opera Stable')
            ]
            
            for root_key, sub_key in registry_paths:
                try:
                    key = winreg.OpenKey(root_key, sub_key)
                    version, _ = winreg.QueryValueEx(key, 'version')
                    return version
                except:
                    continue
            return None
        else:
            cmd = [binary_path, '--version']
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()
            version = output.decode().strip().split()[-1]
            return version
    except Exception as e:
        print(f"Aviso: Não foi possível obter a versão do navegador: {e}")
        return None

def find_chromedriver():
    """
    Procura o chromedriver/operadriver no sistema.
    """
    system = platform.system().lower()
    if system == 'windows':
        paths = ['chromedriver.exe', 'operadriver.exe']
    else:
        paths = [
            '/usr/bin/chromedriver',
            '/usr/local/bin/chromedriver',
            '/usr/bin/operadriver',
            '/usr/local/bin/operadriver',
            'chromedriver',
            'operadriver'
        ]
    
    for path in paths:
        try:
            if os.path.exists(path):
                # Testa se o arquivo é executável
                process = subprocess.Popen([path, '--version'], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
                output, _ = process.communicate()
                if process.returncode == 0:
                    print(f"Driver encontrado em: {path}")
                    print(f"Versão do driver: {output.decode().strip()}")
                    return path
        except Exception:
            continue
    
    return None

def detectar_navegador():
    """
    Detecta o navegador disponível (Chrome, Chromium ou Opera) baseado no sistema operacional.
    Retorna o tipo do navegador e o caminho do binário (se encontrado).
    """
    sistema = platform.system().lower()
    print(f"Sistema operacional detectado: {sistema}")
    
    # Caminhos dos navegadores por sistema operacional
    navegadores = {
        'linux': {
            'chrome': ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable'],
            'chromium': ['/usr/bin/chromium', '/usr/bin/chromium-browser'],
            'opera': ['/usr/bin/opera', '/usr/bin/opera-gx']
        },
        'windows': {
            'chrome': [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
            ],
            'chromium': [
                r'C:\Program Files\Chromium\Application\chrome.exe',
                r'C:\Program Files (x86)\Chromium\Application\chrome.exe'
            ],
            'opera': [
                r'C:\Program Files\Opera GX\opera.exe',
                r'C:\Program Files\Opera\opera.exe',
                r'C:\Program Files (x86)\Opera GX\opera.exe',
                r'C:\Program Files (x86)\Opera\opera.exe'
            ]
        },
        'darwin': {  # macOS
            'chrome': ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'],
            'chromium': ['/Applications/Chromium.app/Contents/MacOS/Chromium'],
            'opera': [
                '/Applications/Opera GX.app/Contents/MacOS/Opera',
                '/Applications/Opera.app/Contents/MacOS/Opera'
            ]
        }
    }
    
    # Se o sistema não for reconhecido, usa as configurações padrão
    if sistema not in navegadores:
        print(f"Sistema {sistema} não reconhecido. Usando configurações padrão do Chrome.")
        return ChromeType.GOOGLE, None
    
    # No Linux, verifica se é uma distribuição baseada em Arch
    if sistema == 'linux':
        try:
            with open('/etc/os-release', 'r') as f:
                os_info = f.read().lower()
                if 'arch' in os_info or 'cachyos' in os_info:
                    print("Distribuição baseada em Arch detectada")
                    # Tenta Chromium primeiro em distribuições Arch
                    for path in navegadores[sistema]['chromium']:
                        if os.path.exists(path):
                            print(f"Chromium encontrado em: {path}")
                            return ChromeType.CHROMIUM, path
        except Exception as e:
            print(f"Erro ao verificar distribuição Linux: {str(e)}")
    
    # Tenta encontrar o Opera primeiro
    for path in navegadores[sistema]['opera']:
        if os.path.exists(path):
            print(f"Opera encontrado em: {path}")
            return 'opera', path
    
    # Depois tenta Chrome/Chromium
    for browser_type in ['chrome', 'chromium']:
        for path in navegadores[sistema][browser_type]:
            if os.path.exists(path):
                print(f"Navegador encontrado: {browser_type} em {path}")
                version = get_chrome_version(path)
                if version:
                    print(f"Versão do navegador: {version}")
                return ChromeType.CHROMIUM if browser_type == 'chromium' else ChromeType.GOOGLE, path
    
    # Se nenhum navegador for encontrado, usa o padrão do sistema
    print("Nenhum navegador encontrado. Usando Chrome como padrão.")
    return ChromeType.GOOGLE, None

def configurar_driver():
    """
    Configura e retorna uma instância do navegador usando o webdriver-manager.
    O webdriver será baixado automaticamente se necessário.
    """
    # Detecta o tipo de navegador
    browser_type, binary_location = detectar_navegador()
    
    # Configura as opções do navegador
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")  # Importante para modo headless
    options.add_argument("--disable-extensions")  # Desativa extensões
    options.add_argument("--disable-dev-tools")  # Desativa ferramentas de desenvolvimento
    options.add_argument("--no-first-run")  # Pula a primeira execução
    options.add_argument("--no-default-browser-check")  # Não verifica navegador padrão
    options.add_argument("--disable-blink-features=AutomationControlled")  # Evita detecção de automação
    
    # Define o caminho do binário se foi encontrado
    if binary_location:
        print(f"Usando binário do navegador em: {binary_location}")
        options.binary_location = binary_location
    
    try:
        # Se for Opera, usa o OperaDriverManager
        if browser_type == 'opera':
            print("Configurando Opera WebDriver...")
            driver_path = OperaDriverManager().install()
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            print("Driver do Opera configurado com sucesso")
            return driver
        
        # Para Chrome/Chromium
        print(f"Configurando {'Chrome' if browser_type == ChromeType.GOOGLE else 'Chromium'} WebDriver...")
        
        try:
            # Tenta primeiro com o chromedriver do sistema
            system_driver = '/usr/bin/chromedriver'
            if os.path.exists(system_driver):
                print(f"Usando chromedriver do sistema em: {system_driver}")
                service = Service(system_driver)
                driver = webdriver.Chrome(service=service, options=options)
                print("Driver configurado com sucesso usando chromedriver do sistema")
                return driver
        except Exception as e:
            print(f"Não foi possível usar o chromedriver do sistema: {str(e)}")
        
        # Se não funcionar com o chromedriver do sistema, tenta com o webdriver-manager
        try:
            driver_path = ChromeDriverManager(chrome_type=browser_type).install()
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            print("Driver configurado com sucesso usando webdriver-manager")
            return driver
        except Exception as e:
            print(f"Erro ao configurar com webdriver-manager: {str(e)}")
            
            # Última tentativa: usar o Chrome como fallback
            if browser_type != ChromeType.GOOGLE:
                print("Tentando configurar com Chrome como última opção...")
                driver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
                service = Service(driver_path)
                driver = webdriver.Chrome(service=service, options=options)
                print("Driver configurado com sucesso usando Chrome")
                return driver
            
            raise e
        
    except Exception as e:
        print(f"Erro fatal ao configurar o driver: {str(e)}")
        raise Exception(f"Não foi possível configurar o WebDriver. Certifique-se de que o Chrome, Chromium ou Opera esteja instalado. Erro: {str(e)}") 