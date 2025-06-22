import platform
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

def get_chrome_version(binary_path):
    """
    Tenta obter a versão do Chrome/Chromium usando o binário especificado.
    """
    try:
        if platform.system().lower() == 'windows':
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
            version, _ = winreg.QueryValueEx(key, 'version')
            return version
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
    Procura o chromedriver no sistema.
    """
    system = platform.system().lower()
    if system == 'windows':
        paths = ['chromedriver.exe']
    else:
        paths = [
            '/usr/bin/chromedriver',
            '/usr/local/bin/chromedriver',
            'chromedriver'
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
                    print(f"ChromeDriver encontrado em: {path}")
                    print(f"Versão do ChromeDriver: {output.decode().strip()}")
                    return path
        except Exception:
            continue
    
    return None

def detectar_navegador():
    """
    Detecta o navegador disponível (Chrome ou Chromium) baseado no sistema operacional.
    Retorna o tipo do navegador e o caminho do binário (se encontrado).
    """
    sistema = platform.system().lower()
    print(f"Sistema operacional detectado: {sistema}")
    
    # Caminhos dos navegadores por sistema operacional
    navegadores = {
        'linux': {
            'chrome': ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable'],
            'chromium': ['/usr/bin/chromium', '/usr/bin/chromium-browser']
        },
        'windows': {
            'chrome': [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
            ],
            'chromium': [
                r'C:\Program Files\Chromium\Application\chrome.exe',
                r'C:\Program Files (x86)\Chromium\Application\chrome.exe'
            ]
        },
        'darwin': {  # macOS
            'chrome': ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'],
            'chromium': ['/Applications/Chromium.app/Contents/MacOS/Chromium']
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
    
    # No Windows, tenta Chrome primeiro
    if sistema == 'windows':
        # Procura o Chrome primeiro no Windows
        for path in navegadores[sistema]['chrome']:
            if os.path.exists(path):
                print(f"Chrome encontrado em: {path}")
                return ChromeType.GOOGLE, path
    
    # Para outros sistemas ou se não encontrou o navegador preferido,
    # tenta todos os navegadores disponíveis
    for browser_type, paths in navegadores[sistema].items():
        for path in paths:
            if os.path.exists(path):
                print(f"Navegador encontrado: {browser_type} em {path}")
                version = get_chrome_version(path)
                if version:
                    print(f"Versão do navegador: {version}")
                return ChromeType.CHROMIUM if browser_type == 'chromium' else ChromeType.GOOGLE, path
    
    # Se nenhum navegador for encontrado, usa o padrão do sistema
    default_type = ChromeType.CHROMIUM if sistema == 'linux' else ChromeType.GOOGLE
    print(f"Nenhum navegador encontrado. Usando tipo padrão: {default_type}")
    return default_type, None

def configurar_driver():
    """
    Configura e retorna uma instância do Chrome/Chromium usando o webdriver-manager.
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
    
    # Define o caminho do binário se foi encontrado
    if binary_location:
        print(f"Usando binário do navegador em: {binary_location}")
        options.binary_location = binary_location
    
    # Primeiro, tenta usar o chromedriver do sistema
    chromedriver_path = find_chromedriver()
    if chromedriver_path:
        try:
            print(f"Tentando usar ChromeDriver do sistema em: {chromedriver_path}")
            service = Service(executable_path=chromedriver_path)
            driver = webdriver.Chrome(service=service, options=options)
            print("Driver configurado com sucesso usando ChromeDriver do sistema")
            return driver
        except Exception as e:
            print(f"Erro ao usar ChromeDriver do sistema: {str(e)}")
    
    try:
        # Se não encontrou ou falhou com o chromedriver do sistema,
        # tenta baixar e usar o webdriver-manager
        print("Baixando/verificando webdriver...")
        driver_path = ChromeDriverManager(chrome_type=browser_type).install()
        print(f"Driver path: {driver_path}")
        service = Service(driver_path)
        
        # Cria e retorna o driver
        print("Iniciando o webdriver...")
        driver = webdriver.Chrome(service=service, options=options)
        print(f"Driver configurado com sucesso usando {'Chromium' if browser_type == ChromeType.CHROMIUM else 'Chrome'}")
        return driver
    except Exception as e:
        print(f"Erro ao configurar o driver: {str(e)}")
        # Se falhar com Chromium, tenta com Chrome
        if browser_type == ChromeType.CHROMIUM:
            print("Tentando configurar com Chrome como fallback...")
            try:
                driver_path = ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install()
                service = Service(driver_path)
                driver = webdriver.Chrome(service=service, options=options)
                print("Driver configurado com sucesso usando Chrome")
                return driver
            except Exception as e2:
                print(f"Erro ao configurar Chrome como fallback: {str(e2)}")
                raise
        raise 