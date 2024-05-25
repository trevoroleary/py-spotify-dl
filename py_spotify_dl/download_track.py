from urllib import request
from urllib.parse import quote
from yt_dlp import YoutubeDL
import re
import os
import eyed3
from pathlib import Path


def create_download_directory():
    path = f"./downloads"

    if os.path.exists(path):
        return path

    try:
        os.makedirs(path)
        return path
    except OSError:
        print("Creation of the download directory failed")


def get_ydl_opts():
    return {
        "format": "bestaudio/best",
        "outtmpl": f"downloads/%(id)s.%(ext)s",
        "ignoreerrors": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }
        ],
    }


def add_track_metadata(track_id, song: dict):
    audiofile = eyed3.load(Path("spotify-dl", "downloads", f"{track_id}.mp3"))

    if audiofile.tag is None:
        audiofile.initTag()

    # Add basic tags
    audiofile.tag.title = song["name"]
    audiofile.tag.album = song["album"]['name']
    audiofile.tag.artist = ", ".join(artist['name'] for artist in song['artists'])
    audiofile.tag.release_date = song['album']['release_date']
    audiofile.tag.track_num = song['track_number']

    album_art = request.urlopen(song['album']['images'][0]['url']).read()
    audiofile.tag.images.set(3, album_art, "image/jpeg")
    audiofile.tag.save()

    # Update downloaded file name
    src = Path("spotify-dl", "downloads", f"{track_id}.mp3")
    dst = Path("spotify-dl", "downloads", f"{song['name']}.mp3")
    os.rename(src, dst)


def download_track_ydl(song: dict):
    artist_str = ""
    for artist in song['artists']:
        artist_str += artist['name']
    song_name = song['name']
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
            downloaded_track = ydl.download([url])
            add_track_metadata(metadata["id"], song)