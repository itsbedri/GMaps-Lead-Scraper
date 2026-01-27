import logging
from logging import basicConfig
import os
import sys

log_dir = "app/common"
os.makedirs(log_dir, exist_ok=True)


log_file = os.path.join(log_dir, "log.log")

basicConfig(level=logging.INFO,
            filename= log_file, filemode="w",
            format="%(asctime)s - %(levelname)s - %(message)s"
            )

logger = logging.getLogger(__name__)
handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# for terminal output
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter('%(levelname)s - %(asctime)s - %(name)s  - %(message)s'))
logger.addHandler(stream_handler)

handler.setFormatter(formatter)
logger.addHandler(handler)
