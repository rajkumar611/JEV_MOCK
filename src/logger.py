import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from src.config import Config


def setup_logger(name: str) -> logging.Logger:
    """Setup logger with file and console handlers"""

    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL)

    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(Config.LOG_LEVEL)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_dir / "jev_claim_processor.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(Config.LOG_LEVEL)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
