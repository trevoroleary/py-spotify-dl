import logging
import time
import traceback
from urllib import request
from urllib.parse import quote
from yt_dlp import YoutubeDL
import re
import os
import shutil
import eyed3
from pathlib import Path
DOWNLOADS_PATH = os.environ['DOWNLOAD_PATH']
LIBRARY_PATH = os.environ['MUSIC_LIBRARY']

logger = logging.getLogger("downloader")
logger.setLevel(logging.DEBUG)

def create_download_directory():
    path = Path(DOWNLOADS_PATH)
    if os.path.exists(path):
        return path
    try:
        os.makedirs(path)
        return path
    except OSError as e:
        logger.error("Creation of the download directory failed")
        raise e


def get_ydl_opts():
    return {
        "format": "bestaudio/best",
        "outtmpl": str(Path(DOWNLOADS_PATH, "%(id)s.%(ext)s")),
        "ignoreerrors": True,
        "logger": logging.getLogger("youtube"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],
    }


def add_track_metadata(track_id, song: dict):
    audiofile = eyed3.load(Path(DOWNLOADS_PATH, f"{track_id}.mp3"))

    if audiofile.tag is None:
        audiofile.initTag()

    # Add basic tags
    audiofile.tag.title = song["name"]
    album_name = song["album"]['name']
    audiofile.tag.album = album_name
    audiofile.tag.artist = "; ".join(artist['name'] for artist in song['artists'])
    album_artist = song['artists'][0]['name']
    audiofile.tag.album_artist = album_artist
    audiofile.tag.release_date = song['album']['release_date']
    audiofile.tag.track_num = song['track_number']

    album_art = request.urlopen(song['album']['images'][0]['url']).read()
    audiofile.tag.images.set(3, album_art, "image/jpeg")
    audiofile.tag.save()

    # Update downloaded file name
    src = Path(DOWNLOADS_PATH, f"{track_id}.mp3")
    if not os.path.exists(Path(LIBRARY_PATH, album_artist, album_name)):
        try:
            os.makedirs(Path(LIBRARY_PATH, album_artist, album_name))
        except OSError as e:
            logger.error("Creation of the download directory failed")
    dst = Path(LIBRARY_PATH, album_artist, album_name,f"{song['name']}.mp3")
    shutil.move(src, dst)


def download_track_ydl(song: dict):
    for i in range(3):
        try:
            artist_str = ""
            for artist in song['artists']:
                artist_str += " " + artist['name']
            song_name = song['name']
            logger.debug(f"Beginning a download attempt on: {song_name} by {artist_str}")
            uri = quote(
                    f'{song_name.replace(" ", "+")}+{artist_str.replace(" ", "+")}'
                )
            html = request.urlopen(
                f"https://www.youtube.com/results?search_query={uri}"
            )
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

            create_download_directory()
            if video_ids:
                with YoutubeDL(get_ydl_opts()) as ydl:
                    url = "https://www.youtube.com/watch?v=" + video_ids[0]
                    metadata = ydl.extract_info(url, download=False)
                    ydl.download([url])
                    add_track_metadata(metadata["id"], song)
                    logger.info(f"Downloaded: {metadata['title']}")
            else:
                logger.error(f"Could not find any audio for {song_name} by {artist_str}")
        except Exception as e:
            logger.error(f"An error occurred while downloading {song['name']} | Trying again {i}")
            logger.error(e)
            traceback.print_exc()
            time.sleep(0.1)
            continue
        else:
            return
