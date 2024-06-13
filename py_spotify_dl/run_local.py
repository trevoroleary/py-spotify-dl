import py_spotify_dl.setup_dot_env
import py_spotify_dl.setup_logger
from py_spotify_dl.helpers import check_new_liked_songs, check_download_playlist_for_new_songs
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
    scope = "user-library-modify user-library-read user-read-private playlist-modify-private playlist-modify-public playlist-read-collaborative playlist-read-private"
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
        other_songs = check_download_playlist_for_new_songs(sp)
        songs = newtime_songs.songs

        # Make sure we don't download the same song twice
        for song in other_songs:
            already_exists = False
            for s in songs:
                if s['id'] == song['id']:
                    already_exists = True
            if not already_exists:
                songs.append(song)
        if songs:
            for song in songs:
                download_track_ydl(song)
            # processes = [Process(target=download_track_ydl, args=(song,)) for song in songs]
            # for process in processes:
            #     process.start()
            # for process in processes:
            #     process.join()
        time.sleep(3)


if __name__ == "__main__":
    main()
