import logging

logger = logging.getLogger("project")
logger.setLevel(logging.WARNING)


ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setLevel(logging.ERROR)
ch.setFormatter(formatter)

logger.addHandler(ch)