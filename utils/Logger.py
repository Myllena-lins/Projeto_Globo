import logging
from datetime import datetime
from pathlib import Path
import os

class Logger:
    _instance = None
    
    def __new__(cls, logs_path=None, mode='a'):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, logs_path=None, mode='a'):
        if self._initialized:
            return
            
        # Configura o caminho dos logs
        self.logs_path = logs_path or os.getenv("CAMINHO_DIRETORIO_LOGS") 
        Path(self.logs_path).mkdir(parents=True, exist_ok=True)
        
        # Configura o formato do log
        self.log_format = '%(asctime)s - %(levelname)s - %(message)s'
        self.date_format = '%d-%m-%Y'
        self.mode = mode
        
        self._initialized = True
    
    def _get_logger(self, log_name):
        """Cria e configura um logger específico"""
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)
        
        # Remove handlers existentes para evitar duplicação
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Configura o arquivo de log diário
        today = datetime.now().strftime(self.date_format)
        log_file = Path(self.logs_path) / f"{today}.log"
        
        file_handler = logging.FileHandler(log_file, mode=self.mode, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(self.log_format))
        
        logger.addHandler(file_handler)
        return logger
    
    def registrar_info(self, message):
        """Registra uma mensagem de nível INFO"""
        logger = self._get_logger("info_logger")
        logger.info(message)
    
    def registrar_erro(self, message):
        """Registra uma mensagem de nível ERROR"""
        logger = self._get_logger("error_logger")
        logger.error(message)
    
    def registrar_aviso(self, message):
        """Registra uma mensagem de nível WARNING"""
        logger = self._get_logger("warning_logger") 
        logger.warning(message)
    
    def registrar_debug(self, message):
        """Registra uma mensagem de nível DEBUG"""
        logger = self._get_logger("debug_logger")
        logger.debug(message)