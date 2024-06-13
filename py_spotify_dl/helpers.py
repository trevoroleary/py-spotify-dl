import spotipy
from datetime import datetime
from datetime import timezone as dt_timezone
from dataclasses import dataclass
import logging


@dataclass
class NewTimeAndSongs:
    latest_time: datetime
    songs: list


def check_download_playlist_for_new_songs(sp: spotipy.Spotify) -> list:
    logger = logging.getLogger("download_playlist")
    playlist_id = "219yF8F4hh3E9xDsZLw0sF"
    playlist = sp.playlist_items(playlist_id=playlist_id)
    songs = list()
    for item in playlist['items']:
        song = item['track']
        sp.playlist_remove_all_occurrences_of_items(playlist_id=playlist_id, items=[song['id']])
        songs.append(song)
        logger.debug(f"Added {song['name']} to download list")
    return songs


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

