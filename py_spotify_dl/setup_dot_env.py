import os
import sys

from dotenv import load_dotenv
from pathlib import Path

if not os.path.exists(Path("spotify-dl")):
    os.mkdir("spotify-dl")
    os.mkdir(Path("spotify-dl", "downloads"))
    with open(Path("spotify-dl", "spotify-credentials.txt"), "w") as f:
        f.writelines(
            [
                "SPOTIPY_CLIENT_ID=\n",
                "SPOTIPY_CLIENT_SECRET=\n",
                "SPOTIPY_REDIRECT_URI=\n"
                "USER_ID=\n"
            ]
        )
    print(f'Please fill in variables made in {Path("spotify-dl", "spotify-credentials.txt")}')
    sys.exit()

load_dotenv(Path("spotify-dl", "spotify-credentials.txt"))
