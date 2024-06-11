import logging
import colorlog

handler = logging.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
))

logger = logging.getLogger('ENV-SETUP')
logger.setLevel(logging.DEBUG)  # set logger level
logger.addHandler(handler)  # add color handler to logger

logger.info("Setting up environment variables")

logging.getLogger("apscheduler.scheduler").setLevel(logging.CRITICAL)
logging.getLogger("apscheduler.executors.default").setLevel(logging.CRITICAL)