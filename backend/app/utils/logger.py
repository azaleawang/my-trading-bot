import watchtower, logging
import os

def setup_logger():
    environment = os.getenv('PY_ENV', 'development')

    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    
        
    if environment == 'development':
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    else:
        cloudwatch_handler = watchtower.CloudWatchLogHandler(log_group='AutoMate-main')
        cloudwatch_handler.setFormatter(formatter)
        logger.addHandler(cloudwatch_handler)

        
    logger.error("Hi, logging test")

# setup_logger()