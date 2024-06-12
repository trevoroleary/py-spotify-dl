import os
import sys

from dotenv import load_dotenv
from pathlib import Path
import logging

logger = logging.getLogger("ENV-SETUP-LOCAL")
logger.setLevel(level=logging.DEBUG)

def make_local_path():
    if not os.path.exists(Path(Path.home(), "spotify-dl")):
        os.mkdir(Path(Path.home(), "spotify-dl"))
    if not os.path.exists(Path(Path.home(), "spotify-dl", "downloads")):
        os.mkdir(Path(Path.home(), "spotify-dl", "downloads"))
    if not os.path.exists(Path(Path.home(), "spotify-dl", "music")):
        os.mkdir(Path(Path.home(), "spotify-dl", "music"))
    if not os.path.exists(Path(Path.home(), "spotify-dl", "data")):
        os.mkdir(Path(Path.home(), "spotify-dl", "data"))

    with open(Path(os.environ['DATA_PATH'], "spotify-credentials.txt"), "w") as f:
        f.writelines(
            [
                "SPOTIPY_CLIENT_ID=\n",
                "SPOTIPY_CLIENT_SECRET=\n",
                "SPOTIPY_REDIRECT_URI=http://localhost:8080/callback\n",
                "USER_ID=\n",
            ]
        )
    logger.debug(
        f"Please fill in variables made in {Path(os.environ['DATA_PATH'], 'spotify-credentials.txt')}\n"
        f"Learn more from the README.md\n"
        f"Run again when you're done"
    )
    sys.exit()


def setup_env():
    required_variables = [
        "SPOTIPY_CLIENT_ID", "SPOTIPY_CLIENT_SECRET", "SPOTIPY_REDIRECT_URI", "USER_ID"
    ]

    if "DOCKER_CONTAINER" in os.environ:
        os.environ['DOWNLOAD_PATH'] = "/downloads"
        os.environ['DATA_PATH'] = "/data"
        os.environ['MUSIC_LIBRARY'] = "/music"
        with open(Path(os.environ['DATA_PATH'], "test.txt"), 'w') as f:
            f.write("test")

    else:
        os.environ['DOWNLOAD_PATH'] = str(Path(Path.home(), "spotify-dl", "downloads"))
        os.environ['MUSIC_LIBRARY'] = str(Path(Path.home(), "spotify-dl", "music"))
        os.environ['DATA_PATH'] = str(Path(Path.home(), "spotify-dl", "data"))
        if not os.path.exists(Path(os.environ['DATA_PATH'], "spotify-credentials.txt")):
            make_local_path()
        else:
            load_dotenv(Path(os.environ['DATA_PATH'], "spotify-credentials.txt"))

    for required_variable in required_variables:
        if required_variable not in os.environ and "DOCKER_CONTAINER" not in os.environ:
            raise ValueError(f"Please set {required_variable} in the environment variables")


setup_env()
