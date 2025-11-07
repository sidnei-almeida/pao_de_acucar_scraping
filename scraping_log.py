import logging
import os
from datetime import datetime

def configurar_logger():
    """Configure the logger used across the scraping modules."""
    # Instantiate logger
    logger = logging.getLogger('scraping_pao_de_acucar')
    logger.setLevel(logging.INFO)
    
    # Create the logs directory if missing
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # File handler inside the logs directory
    log_filename = f'scraping_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    log_path = os.path.join(logs_dir, log_filename)
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Console handler (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Shared formatter configuration
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Attach handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create a global logger instance
logger = configurar_logger() 