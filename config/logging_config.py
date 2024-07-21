import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging():
    # Path relative to the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    log_dir = os.path.join(script_dir, "..", "logging")
    log_file = "netflix_data.log"

    # Create the directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # maximum log file size of 5 MB and up to 1 backup log data.
    handler = RotatingFileHandler(
        os.path.join(log_dir, log_file), maxBytes=5 * 1024 * 1024, backupCount=1
    )
    handler.setFormatter(log_formatter)

    # Get the root logger and set the handler
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)
