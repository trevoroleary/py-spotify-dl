import py_spotify_dl.setup_dot_env
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from datetime import timezone as dt_timezone
from multiprocessing import Process

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
    latest_songs = sp.current_user_saved_tracks()
    latest_albums = sp.current_user_saved_albums()
    songs = list()
    update_dates = [last_update]
    for idx, item in enumerate(latest_songs['items']):
        added_time = datetime.strptime(item['added_at'], "%Y-%m-%dT%H:%M:%SZ")
        added_time = added_time.replace(tzinfo=dt_timezone.utc)
        if added_time > last_update:
            songs.append(item['track'])
            update_dates.append(added_time)

    for idx, item in enumerate(latest_albums['items']):
        added_time = datetime.strptime(item['added_at'], "%Y-%m-%dT%H:%M:%SZ")
        added_time = added_time.replace(tzinfo=dt_timezone.utc)
        if added_time > last_update:
            update_dates.append(added_time)
            album = {
                "name": item['album']['name'],
                "release_date": item['album']['release_date'],
                "images": item['album']['images'],
                "artists": item['album']['artists'],
                "total_tracks": item['album']['total_tracks'],
                "uri": item['album']['uri']
            }
            for track in item['album']['tracks']['items']:
                track['album'] = album
                songs.append(track)

    update_dates.sort(reverse=True)

    return NewTimeAndSongs(songs=songs, latest_time=update_dates[0])


def main():
    sp = auth()
    last_update = SERVER_START_UP_TIME
    print("Application Started...")
    print("press ctrl-C to exit")
    check_new_liked_songs(sp, last_update)
    print(f"Application has started successfully")
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
