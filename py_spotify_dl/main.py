import py_spotify_dl.setup_dot_env
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from datetime import timezone as dt_timezone

from dataclasses import dataclass
from py_spotify_dl.download_track import download_track_ydl
from pathlib import Path
SERVER_START_UP_TIME = datetime.now(dt_timezone.utc)
DATA_PATH = os.environ['DATA_PATH']

@dataclass
class NewTimeAndSongs:
    latest_time: datetime
    songs: list


def auth() -> spotipy.Spotify:
    scope = "user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, cache_path=Path(DATA_PATH, "token-cache.txt"), open_browser=False))
    return sp


def check_new_liked_songs(sp: spotipy.Spotify, last_update: datetime) -> NewTimeAndSongs:
    results = sp.current_user_saved_tracks()
    songs = list()
    update_dates = [last_update]
    for idx, item in enumerate(results['items']):
        added_time = datetime.strptime(item['added_at'], "%Y-%m-%dT%H:%M:%SZ")
        added_time = added_time.replace(tzinfo=dt_timezone.utc)
        if added_time > last_update:
            songs.append(item['track'])
            update_dates.append(added_time)
    update_dates.sort(reverse=True)

    return NewTimeAndSongs(songs=songs, latest_time=update_dates[0])


def main():
    sp = auth()
    last_update = SERVER_START_UP_TIME
    print("Application Started...")
    print("press ctrl-C to exit")
    while True:
        newtime_songs = check_new_liked_songs(sp, last_update)
        last_update = newtime_songs.latest_time
        if newtime_songs.songs:
            for song in newtime_songs.songs:
                download_track_ydl(song)
        time.sleep(5)


if __name__ == "__main__":
    main()
