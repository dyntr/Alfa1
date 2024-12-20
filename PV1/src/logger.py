import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


class Logger:
    LOG_FOLDER = "logs"
    LOG_FILE = os.path.join(LOG_FOLDER, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

    def __init__(self, log_file=LOG_FILE, max_size=5 * 1024 * 1024, backup_count=3, console_output=True):
        """
        Inicializuje logger s podporou rotace souborů a volitelným výstupem do konzole.

        Args:
            log_file (str): Cesta k logovacímu souboru.
            max_size (int): Maximální velikost logovacího souboru před rotací (výchozí 5 MB).
            backup_count (int): Počet záložních logů, které se uchovávají (výchozí 3).
            console_output (bool): Povolit výstup do konzole (výchozí True).
        """
        self.log_file = log_file
        self.max_size = max_size
        self.backup_count = backup_count
        self.console_output = console_output

        # Zajištění existence složky pro logy
        if not os.path.exists(self.LOG_FOLDER):
            os.makedirs(self.LOG_FOLDER)

        # Konfigurace logování
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logging.DEBUG)

        # Rotující souborový handler
        file_handler = RotatingFileHandler(
            self.log_file, maxBytes=self.max_size, backupCount=self.backup_count
        )
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(file_handler)

        # Konzolový výstup (volitelný)
        if self.console_output:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(console_handler)

    def info(self, message):
        """Logování informací."""
        self.logger.info(message)

    def error(self, message):
        """Logování chyb."""
        self.logger.error(message)

    def warning(self, message):
        """Logování varování."""
        self.logger.warning(message)

    def debug(self, message):
        """Logování pro ladění."""
        self.logger.debug(message)

    def critical(self, message):
        """Logování kritických chyb."""
        self.logger.critical(message)

    def set_level(self, level):
        """
        Nastaví úroveň logování.

        Args:
            level (str): Úroveň logování ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
        """
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        self.logger.setLevel(levels.get(level.upper(), logging.INFO))

    def clear_log(self):
        """Vymaže obsah logovacího souboru."""
        open(self.log_file, 'w').close()
        self.info("Log file cleared.")
