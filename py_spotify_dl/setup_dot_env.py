import os
import sys
import logging
from dotenv import load_dotenv
from pathlib import Path

logging.basicConfig()

if not os.path.exists(Path(Path.home(), "spotify-dl")):
    os.mkdir("spotify-dl")
    os.mkdir(Path(Path.home(), "spotify-dl", "downloads"))
    with open(Path(Path.home(), "spotify-dl", "spotify-credentials.txt"), "w") as f:
        f.writelines(
            [
                "SPOTIPY_CLIENT_ID=\n",
                "SPOTIPY_CLIENT_SECRET=\n",
                "SPOTIPY_REDIRECT_URI=\n",
                "USER_ID=\n",
                "DOWNLOAD_PATH=\n",
            ]
        )
    print(
        f"Please fill in variables made in {Path(Path.home(), 'spotify-dl', 'spotify-credentials.txt')}\n"
        f"Learn more from the README.md\n"
        f"Run again when you're done"
    )
    sys.exit()

print(Path(Path.home(), "spotify-dl", "spotify-credentials.txt"))
load_dotenv(Path(Path.home(), "spotify-dl", "spotify-credentials.txt"))
