import os
import sys
import logging

from app.config.config_manager import ensure_configurations, CONFIG_FILE
from app.interface.game_lib_window import main_window
from app.utils.others.app_logger import get_logger

import ctypes

ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

if not os.path.exists(CONFIG_FILE):
    ensure_configurations()

logger = get_logger()

class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

sys.stdout = StreamToLogger(logger, logging.INFO)
sys.stderr = StreamToLogger(logger, logging.ERROR)

def main():
    try:
        main_window()
    except FileNotFoundError as e:
        logger.error(f"An error occurred: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
