"""
Logging configuration for the surveillance system
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from utils.config import Config

def setup_logger(name, log_file=None):
    """
    Setup logger with file and console handlers
    
    Args:
        name: Logger name
        log_file: Optional log file path
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # Create formatters
    formatter = logging.Formatter(Config.LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file or name:
        log_path = os.path.join(Config.LOG_DIR, log_file or f'{name}.log')
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger
