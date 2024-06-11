import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from datetime import timezone as dt_timezone
from multiprocessing import Process
import logging
from dataclasses import dataclass
from py_spotify_dl.download_track import download_track_ydl
from pathlib import Path


@dataclass
class NewTimeAndSongs:
    latest_time: datetime
    songs: list


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

