import os
import json
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

# Load config
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.json"
with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)

# Resolve paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / CONFIG["log_dir"]
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / CONFIG["log_file"]


# Create logger
logger = logging.getLogger("my_app_logger")
logger.setLevel(logging.DEBUG)  # Capture all logs (DEBUG, INFO, WARNING, ERROR)

# Create a timed rotating file handler (new file every day, keep 7 days)
handler = TimedRotatingFileHandler(
    LOG_FILE, when="midnight", interval=1, backupCount=7, encoding="utf-8"
)
handler.suffix = "%Y-%m-%d"  # Each file will have date suffix (app.log.2025-08-19)

# Formatter for log messages
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)

# Add handler to logger
if not logger.handlers:  # Prevent duplicate handlers if re-imported
    logger.addHandler(handler)

# Export logger
__all__ = ["logger"]
