import logging
import os
import colorlog
from logtail import LogtailHandler

logtail_handler = LogtailHandler(source_token=os.environ.get("LOGTAIL_SOURCE_TOKEN"))
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
# root_logger.handlers = []
root_logger.addHandler(logtail_handler)
logging.getLogger("apscheduler.scheduler").setLevel(logging.CRITICAL)
logging.getLogger("apscheduler.executors.default").setLevel(logging.CRITICAL)