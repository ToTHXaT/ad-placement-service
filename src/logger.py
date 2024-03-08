import sys
import logging

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[%(levelname)s] %(asctime)s: %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)

logger.addHandler(handler)
