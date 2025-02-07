from flask import Flask
import os
from backend.spotify_routes.spotify_routes import spotify_routes
from backend.llm_routes.llm_routes import llm_routes
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    load_dotenv()


    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SPOTIPY_CLIENT_ID'] = os.environ.get('SPOTIPY_CLIENT_ID')
    app.config['SPOTIPY_CLIENT_SECRET'] = os.environ.get('SPOTIPY_CLIENT_SECRET')
    app.config['SPOTIPY_REDIRECT_URI'] = os.environ.get('SPOTIPY_REDIRECT_URI')
    
    
    app.logger.info('current_app(): registering blueprints with Flask app object.')   

    app.register_blueprint(spotify_routes,url_prefix='/s')
    app.register_blueprint(llm_routes,url_prefix='/l')

    return app






