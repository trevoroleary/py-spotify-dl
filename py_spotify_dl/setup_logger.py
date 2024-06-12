import logging
import os
import colorlog
from logtail import LogtailHandler

# logtail_handler = LogtailHandler(source_token=os.environ.get("LOGTAIL_SOURCE_TOKEN"))
logging.basicConfig(level=logging.DEBUG)
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

root_logger.debug("TESTING!!")
# root_logger.handlers = []
# root_logger.addHandler(logtail_handler)
logging.getLogger("apscheduler.scheduler").setLevel(logging.CRITICAL)
logging.getLogger("apscheduler.executors.default").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)
logging.getLogger("spotipy.client").setLevel(logging.CRITICAL)
logging.getLogger("eyed3.id3.frames").setLevel(logging.CRITICAL)
logging.getLogger("eyed3.id3.tag").setLevel(logging.CRITICAL)