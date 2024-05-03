from loguru import logger
import logging
import json
from pathlib import Path
import sys

LOG_LEVEL = 'DEBUG'
discord_logger = None

"""
Creates and configures a logger with specified log level and formats for console and file logging.

Args:
    None

Returns:
    None

Raises:
    None
"""

def create_logger():
    logs_path = Path('logs')
    logs_path.mkdir(exist_ok=True)
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>" if LOG_LEVEL != 'DEBUG' else "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <red>{file}</red> | <yellow>{function}</yellow> | <level>{message}</level>"
    logger.add(sys.stdout, level=LOG_LEVEL, colorize=True, format=log_format)
    logger.add(logs_path / 'retrocord.log', level=LOG_LEVEL, colorize=True, format=log_format)

"""
Switches the logger configuration based on the log level.

Args:
    None

Returns:
    None

Raises:
    ValueError: If the log level is invalid
"""

def switch_logger():
    logger.remove()
    if LOG_LEVEL in ['DEBUG', 'INFO']:
        create_logger()
    else:
        raise ValueError("Invalid log level")

def log_json(json_obj, level='DEBUG'):
    pretty_json = json.dumps(json_obj, indent=4)
    logger.log(level, pretty_json)

def setup_discord_logging():
    global discord_logger
    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.DEBUG)
    discord_handler = DiscordHandler()
    discord_logger.handlers = [discord_handler]
    discord_logger.propagate = False

class DiscordHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        logger.log(record.levelno, log_entry)
        if len(discord_logger.handlers) > 1:
            discord_logger.handlers = [self]

switch_logger()
setup_discord_logging()