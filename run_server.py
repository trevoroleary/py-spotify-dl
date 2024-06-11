import py_spotify_dl.setup_logger
from flask import Flask, request, redirect
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import requests
import os
import spotipy
from flask_apscheduler import APScheduler
from py_spotify_dl.run_local import check_new_liked_songs
from py_spotify_dl.download_track import download_track_ydl
from datetime import datetime
from datetime import timezone as dt_timezone
import logging



class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(Config())

SP_CLIENT = None
LAST_UPDATE = datetime.now(dt_timezone.utc)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
logger = logging.getLogger("SPOTIFY-SERVER")
logger.setLevel(logging.DEBUG)


def download_latest():
    global SP_CLIENT
    global LAST_UPDATE

    if not isinstance(SP_CLIENT, spotipy.Spotify):
        logger.debug(f"No Files to download")
        return

    newtime_songs = check_new_liked_songs(SP_CLIENT, LAST_UPDATE)
    LAST_UPDATE = newtime_songs.latest_time
    if newtime_songs.songs:
        for song in newtime_songs.songs:
            download_track_ydl(song)
        # processes = [Process(target=download_track_ydl, args=(song,)) for song in newtime_songs.songs]
        # for process in processes:
        #     process.start()
        # for process in processes:
        #     process.join()


scheduler.add_job(id='Download Latest', func=download_latest, trigger='interval', seconds=3)


AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]  # "http://localhost:8080/callback"
CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SCOPE = ['user-library-read', 'user-read-currently-playing']


def get_headers(token):
    return {"Authorization": "Bearer " + token}


@app.route("/")
def root_message():
    app.logger.info('hello! root accessed')
    return 'I am a spotify server'


@app.route("/login")
def login():
    app.logger.info('login logged in successfully')
    spotify = OAuth2Session(CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI)
    authorization_url, state = spotify.authorization_url(AUTH_URL)
    return redirect(authorization_url)


# Your redirect URI's path
# http://localhost:3000/callback?code=AQDTZDK66wl...se8A1YTe&state=kt4H....963Nd
@app.route("/callback", methods=['GET'])
def callback():
    global SP_CLIENT

    # get access token
    code = request.args.get('code')
    resp = requests.post(TOKEN_URL,
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        })
    access_token = resp.json()['access_token']
    SP_CLIENT = spotipy.Spotify(auth=access_token)
    if SP_CLIENT.current_user()['id'] != os.environ["USER_ID"]:
        SP_CLIENT = None
        return 'Not Found', 404

    return "You're Logged In!"


if __name__ == '__main__':
    logger.info("TEST TEST TEST")
    app.run(host='0.0.0.0', port=8080, debug=False)