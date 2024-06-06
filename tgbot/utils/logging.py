import logging
import os

from data import config


def setup_logger(name: str) -> logging.Logger:
    log_dir = '/app/logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        filename=os.path.join(log_dir, 'bot.log'),
        level=config.LOGGING_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    log = logging.getLogger(name)
    return log
