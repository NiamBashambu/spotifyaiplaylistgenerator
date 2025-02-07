import os
from flask import Flask, request, redirect, session, url_for, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Blueprint

spotify_routes = Blueprint('spotify_routes',__name__)

spotify_routes.secret_key = os.environ.get('SECRET_KEY') # Replace with a secure secret key

# Set your Spotify credentials and desired scope
SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')
SCOPE = 'playlist-modify-public user-top-read'



@spotify_routes.route('/')
def index():
    return render_template('index.html')  # A simple homepage with a "Log in with Spotify" button

@spotify_routes.route('/login')
def login():
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@spotify_routes.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE
    )
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('playlist_request'))
