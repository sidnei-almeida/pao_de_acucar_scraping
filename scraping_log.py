import logging
from datetime import datetime

def configurar_logger():
    """Configura o logger para o scraping."""
    # Cria um logger
    logger = logging.getLogger('scraping_pao_de_acucar')
    logger.setLevel(logging.INFO)
    
    # Cria um handler para arquivo
    log_filename = f'scraping_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Cria um handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Define o formato do log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Adiciona os handlers ao logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Cria uma instância global do logger
logger = configurar_logger() 