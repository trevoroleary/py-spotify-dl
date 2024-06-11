import py_spotify_dl.setup_logger
import py_spotify_dl.setup_dot_env
from py_spotify_dl.helpers import check_new_liked_songs
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from datetime import timezone as dt_timezone
from multiprocessing import Process
import logging
from py_spotify_dl.download_track import download_track_ydl
from pathlib import Path

SERVER_START_UP_TIME = datetime.now(dt_timezone.utc)
DATA_PATH = os.environ['DATA_PATH']

logger = logging.getLogger("LOCAL-MAIN")
logger.setLevel(logging.DEBUG)


def auth() -> spotipy.Spotify:
    scope = "user-library-read"
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            cache_path=Path(DATA_PATH, "token-cache.txt"),
            open_browser=False
        )
    )
    return sp


def main():
    sp = auth()
    last_update = SERVER_START_UP_TIME
    logger.info("Application Starting...")
    logger.info("press ctrl-C to exit")
    check_new_liked_songs(sp, last_update)
    logger.info(f"Application has started successfully!")
    time.sleep(3)
    while True:
        newtime_songs = check_new_liked_songs(sp, last_update)
        last_update = newtime_songs.latest_time
        if newtime_songs.songs:
            processes = [Process(target=download_track_ydl, args=(song,)) for song in newtime_songs.songs]
            for process in processes:
                process.start()
            for process in processes:
                process.join()
        time.sleep(3)


if __name__ == "__main__":
    main()
