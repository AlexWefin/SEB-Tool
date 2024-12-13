import os
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILENAME = os.path.join(LOG_DIR, 'app.log')

logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler = RotatingFileHandler(LOG_FILENAME, maxBytes=5*1024*1024, backupCount=5)
handler.setFormatter(formatter)

logger.addHandler(handler)

def get_logger():
    return logger
