import logging
import os
from logging.handlers import RotatingFileHandler
from from_root import from_root
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = f"{datetime.now().strftime('%m_%d_%y_%H_%M_%S')}.log"
MAX_LOG_SIZE_FILE = 5 * 1024 *1024
BACKUP_FILES = 3

log_dir_path = os.path.join(from_root(), LOG_DIR)
os.makedirs(log_dir_path, exist_ok= True)
log_file_path = os.path.join(log_dir_path, LOG_FILE)

def configure_logger():
    """
    Basically yha pe hum log configure kr rhe h console aur log file dir me using console file handler and
    roatating file handler
    
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    format_for_logging = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE_FILE, backupCount=BACKUP_FILES)
    file_handler.setFormatter(format_for_logging)
    file_handler.setLevel(logging.DEBUG)
    
    console_handler_for_this  =logging.StreamHandler()
    console_handler_for_this.setFormatter(format_for_logging)
    console_handler_for_this.setLevel(logging.INFO)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler_for_this)
    
configure_logger()
