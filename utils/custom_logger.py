from loguru import logger
import logging
import json
import sys
import os

LOG_LEVEL = 'DEBUG'

# Function to switch the logger according to the LOG_LEVEL variable
def switch_logger():
    logger.remove()
    if LOG_LEVEL in ['DEBUG', 'INFO']:
        if not os.path.exists('logs'):
            os.makedirs('logs')
        log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>"
        if LOG_LEVEL == 'DEBUG':
            log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <red>{file}</red> | <yellow>{function}</yellow> | <level>{message}</level>"
        logger.add(sys.stdout, level=LOG_LEVEL, colorize=True, format=log_format)
        logger.add('logs/retrocord.log', level=LOG_LEVEL, colorize=True, format=log_format)
    else:
        raise ValueError("Invalid log level")

# Call the function to set the logger according to the LOG_LEVEL variable
switch_logger()

# Function to log JSON objects
def log_json(json_obj, level='DEBUG'):
    pretty_json = json.dumps(json_obj, indent=4)
    logger.log(level, pretty_json)

# Class to handle Discord's logging
class DiscordHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        logger.log(record.levelno, log_entry)
        # Ensure that this handler is the only one
        if len(discord_logger.handlers) > 1:
            discord_logger.handlers = [self]

# Add Discord's logging to Loguru
discord_logger = logging.getLogger('discord')
discord_logger.handlers = []  # Remove all handlers
discord_logger.setLevel(logging.DEBUG)
discord_logger.addHandler(DiscordHandler())
discord_logger.propagate = False  # Disable propagation