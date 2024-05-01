import logging
import os

class Logger:
    def __init__(self):
        self.__start_logger()
    
    
    def __start_logger(self):
        """Inicializa o arquivo de log."""
        logging.basicConfig(filename='.log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        if os.path.exists('.log.txt'):
            os.remove('.log.txt')
            
    
    def print(self, text):
        """Imprime uma mensagem no arquivo de log e no terminal."""
        logging.info(text)
        print(text)