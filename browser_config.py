import platform
import os
import subprocess
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from scraping_log import logger


def build_options(browser_type, binary_location=None):
    """Create Selenium options according to the browser type."""
    if browser_type in {'chrome', 'chromium'}:
        options = ChromeOptions()
        chrome_flags = [
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
        for flag in chrome_flags:
            options.add_argument(flag)

        if os.environ.get('RENDER') or os.environ.get('HEROKU'):
            options.binary_location = "/usr/bin/google-chrome-stable"
        elif binary_location:
            options.binary_location = binary_location

        return options

    # Firefox defaults
    options = FirefoxOptions()
    options.headless = True
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("privacy.trackingprotection.enabled", True)
    if binary_location:
        options.binary_location = binary_location
    return options

def detectar_navegador():
    """
    Detect which browser is available on the host system.

    Returns:
        tuple[str, str | None]: Browser type and binary path (when found)
    """
    sistema = platform.system().lower()
    logger.info(f"Detected operating system: {sistema}")
    
    # Browser lookup table per operating system
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
            ],
            'firefox': [
                '/usr/bin/firefox',
                '/usr/local/bin/firefox',
                '/var/lib/snapd/snap/bin/firefox',
                '/opt/firefox/firefox'
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
            ],
            'firefox': [
                r'C:\Program Files\Mozilla Firefox\firefox.exe',
                r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe',
                r'C:\Users\{}\AppData\Local\Mozilla Firefox\firefox.exe'.format(os.environ.get('USERNAME', ''))
            ]
        },
        'darwin': {  # macOS
            'chrome': [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
            ],
            'chromium': [
                '/Applications/Chromium.app/Contents/MacOS/Chromium'
            ],
            'firefox': [
                '/Applications/Firefox.app/Contents/MacOS/firefox',
                '/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox'
            ]
        }
    }
    
    # Fall back to Chrome defaults when the OS is not recognized
    if sistema not in navegadores:
        logger.warning(f"Unsupported OS '{sistema}'. Falling back to default Chrome settings.")
        return 'chrome', None
    
    # Detect Arch/CachyOS-based distributions
    if sistema == 'linux':
        try:
            with open('/etc/os-release', 'r') as f:
                os_info = f.read().lower()
                if 'arch' in os_info or 'cachyos' in os_info:
                    logger.info("Arch/CachyOS-based distribution detected")
                    # Prefer Chromium first on Arch-based systems
                    for path in navegadores[sistema]['chromium']:
                        if os.path.exists(path):
                            logger.info(f"Chromium found at: {path}")
                            return 'chromium', path
        except Exception as e:
            logger.warning(f"Failed to detect Linux distribution: {str(e)}")
    
    # Search for browsers in the preferred order
    for browser_type in ['chrome', 'chromium', 'firefox']:
        for path in navegadores[sistema][browser_type]:
            if os.path.exists(path):
                logger.info(f"Browser found: {browser_type} at {path}")
                return browser_type, path
    
    # Default to Chrome if nothing is discovered
    logger.warning("No browser binary detected. Defaulting to Chrome.")
    return 'chrome', None

def verificar_driver_sistema(browser_type):
    """
    Check whether a compatible driver already exists on the machine.
    """
    sistema = platform.system().lower()
    drivers_possiveis = []
    
    if browser_type == 'firefox':
        drivers_possiveis = [
            'geckodriver',
            '/usr/bin/geckodriver',
            '/usr/local/bin/geckodriver',
            'geckodriver.exe'
        ]
    elif sistema == 'windows':
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
                # Ensure the driver executable runs correctly
                result = subprocess.run([driver_path, '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    logger.info(f"Driver located on the system: {driver_path}")
                    logger.info(f"Version: {result.stdout.strip()}")
                    return driver_path
            except Exception as e:
                logger.warning(f"Failed to validate driver {driver_path}: {e}")
                continue
    
    return None

def configurar_driver():
    """
    Configure and return a Selenium WebDriver instance.

    Automatically detects the available browser and fetches the proper driver.
    """
    logger.info("Starting WebDriver setup...")
    
    # Detect the available browser
    browser_type, binary_location = detectar_navegador()
    
    # Check for existing system drivers
    driver_sistema = verificar_driver_sistema(browser_type)
    
    # Possible setup strategies
    tentativas = []
    
    # Strategy 1: Use system driver when available
    if driver_sistema:
        tentativas.append(('sistema', driver_sistema, browser_type, binary_location))
    
    # Strategy 2: Force default driver path on Linux for Chrome/Chromium
    if browser_type in {'chrome', 'chromium'}:
        tentativas.append(('sistema', '/usr/bin/chromedriver', 'chrome', binary_location))
    
    # Strategy 3: Use webdriver-manager for the detected browser
    tentativas.append(('webdriver-manager', None, browser_type, binary_location))
    
    # Strategy 4: Fallback to Chrome webdriver-manager when using Chromium or Firefox
    if browser_type not in {'chrome'}:
        tentativas.append(('webdriver-manager', None, 'chrome', None))
    
    for i, (metodo, driver_path, tipo_navegador, binary_override) in enumerate(tentativas, 1):
        try:
            logger.info(f"Attempt {i}: {metodo} with {tipo_navegador}")
            options = build_options(tipo_navegador, binary_override if tipo_navegador != 'chrome' else binary_override)
            
            if metodo == 'sistema':
                # Ensure the driver exists before using it
                if not os.path.exists(driver_path):
                    raise Exception(f"Driver not found at: {driver_path}")
                
                if tipo_navegador == 'firefox':
                    service = FirefoxService(executable_path=driver_path)
                    driver = webdriver.Firefox(service=service, options=options)
                else:
                    service = ChromeService(executable_path=driver_path)
                    driver = webdriver.Chrome(service=service, options=options)
            else:  # webdriver-manager
                # Attempt to download and configure the driver automatically
                try:
                    # Try the detected browser type first
                    if tipo_navegador == 'firefox':
                        driver_path = GeckoDriverManager().install()
                        service = FirefoxService(executable_path=driver_path)
                        driver = webdriver.Firefox(service=service, options=options)
                    else:
                        if tipo_navegador == 'chromium':
                            chrome_type = ChromeType.CHROMIUM
                        else:
                            chrome_type = ChromeType.GOOGLE
                        
                        driver_manager = ChromeDriverManager(chrome_type=chrome_type)
                        driver_path = driver_manager.install()
                        
                        if os.path.exists(driver_path):
                            service = ChromeService(executable_path=driver_path)
                            driver = webdriver.Chrome(service=service, options=options)
                        else:
                            raise Exception(f"Downloaded driver not found at: {driver_path}")
                        
                except Exception as inner_e:
                    # Fallback to the default Chrome driver
                    if tipo_navegador == 'firefox':
                        logger.warning(f"Driver setup failed with GeckoDriverManager: {inner_e}")
                        raise
                    else:
                        logger.warning(f"Driver setup failed with {chrome_type}, retrying with GOOGLE: {inner_e}")
                        driver_manager = ChromeDriverManager(chrome_type=ChromeType.GOOGLE)
                        driver_path = driver_manager.install()
                        service = ChromeService(executable_path=driver_path)
                        driver = webdriver.Chrome(service=service, options=build_options('chrome', binary_override))
            
            # Smoke-test the driver
            driver.get("data:text/html,<html><body><h1>Test</h1></body></html>")
            logger.info(f"WebDriver configured successfully via {metodo} using {tipo_navegador}")
            return driver
            
        except Exception as e:
            logger.warning(f"Setup attempt {i} failed ({metodo} with {tipo_navegador}): {str(e)}")
            try:
                if 'driver' in locals():
                    driver.quit()
            except:
                pass
            continue
    
    # Exhausted every strategy
    logger.error("Unable to configure the WebDriver after all attempts")
    raise Exception("Could not configure the WebDriver. Ensure Chrome/Chromium/Firefox is installed.")