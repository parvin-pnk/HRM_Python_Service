
import logging
from pythonjsonlogger import jsonlogger

def setup_logging():
   
    logger = logging.getLogger('sisuni_app')
    logger.setLevel(logging.INFO)
    
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(module)s %(funcName)s %(line)d %(message)s'
    )
    logHandler.setFormatter(formatter)
    
    if not logger.hasHandlers():
        logger.addHandler(logHandler)
    
    return logger

log = setup_logging()