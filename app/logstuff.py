from datetime import date
import logging
from pythonjsonlogger import jsonlogger

def setup_logging(log_level=logging.INFO, log_file=None):
    log_file = "request.log"
    # Create a JSON logger
    logger = logging.getLogger()

    # Clear any existing handlers to avoid duplicate logs
    logger.handlers.clear()

    # Create a console handler with the JSON formatter
    console_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(fmt='%(asctime)s %(levelname)s %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add a file handler if log_file path is provided
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(log_level)


    return logger

if __name__ == "__main__":
    pass