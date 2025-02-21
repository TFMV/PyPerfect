import sys
from loguru import logger

def configure_logging():
    logger.remove()
    logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")
