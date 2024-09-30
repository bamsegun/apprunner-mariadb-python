import logging
import os


if not os.path.isdir(os.environ.get('LOG_PATH', 'log')):
  os.mkdir(os.environ.get('LOG_PATH', 'log'))

# Create a custom logger
logger = logging.getLogger(__name__)
formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


# Create handlers
debug_handler = logging.FileHandler(f'{os.environ.get("LOG_PATH", "log")}/debug.log')
info_handler = logging.FileHandler(f'{os.environ.get("LOG_PATH", "log")}/info.log')
error_handler = logging.FileHandler(f'{os.environ.get("LOG_PATH", "log")}/error.log')

debug_handler.setLevel(logging.DEBUG)
info_handler.setLevel(logging.INFO)
error_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
debug_handler.setFormatter(formater)
info_handler.setFormatter(formater)
error_handler.setFormatter(formater)

# Add handlers to the logger
logger.addHandler(debug_handler)
logger.addHandler(info_handler)
logger.addHandler(error_handler)

# logger.warning('This is a warning')
# logger.error('This is an error')