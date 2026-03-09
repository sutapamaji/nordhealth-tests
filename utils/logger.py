import logging
import os
from datetime import datetime

def get_logger(name):
    """ Creates and returns a logger instance that outputs to both console and a log file in the report/ folder. """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "report", "logs")
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d")
        file_handler = logging.FileHandler(os.path.join(log_dir, f"execution_{timestamp}.log"))
        file_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
    return logger
