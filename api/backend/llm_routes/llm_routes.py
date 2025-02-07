import os
from flask import Flask, request, render_template, session
import openai
import json
import spotipy
from flask import Blueprint


llm_routes = Blueprint('llm_routes',__name__)

@llm_routes.route('/playlist_request', methods=['GET', 'POST'])
def playlist_request():
    if request.method == 'POST':
        user_query = request.form.get('query')
        
        # Build the prompt for the LLM
        prompt = (
            f"Extract the music attributes from this playlist request into a JSON object with keys "
            f"'activity', 'genre', 'mood', 'tempo', and optionally 'decade'. Request: '{user_query}'"
        )
        
        # Call the LLM (e.g., OpenAI)
        response = openai.Completion.create(
            engine='text-davinci-003',  # or another model
            prompt=prompt,
            max_tokens=100,
            temperature=0.5
        )
        # Assuming the LLM returns valid JSON text:
        try:
            attributes = json.loads(response.choices[0].text.strip())
        except json.JSONDecodeError:
            return "Error parsing LLM response. Please try again."
        
        # Use the attributes to generate recommendations from Spotify
        sp = spotipy.Spotify(auth=session.get('token_info')['access_token'])
        
        # Example: Using the recommendations endpoint
        # Here you might map attributes to Spotify parameters (seed_genres, target_tempo, etc.)
        # For instance, if genre is provided, use it as a seed.
        seed_genres = attributes.get('genre', '')
        target_tempo = 120  # default value; you could adjust based on 'tempo' from attributes
        
        recommendations = sp.recommendations(seed_genres=[seed_genres], limit=20, target_tempo=target_tempo)
        
        # Create a new playlist for the user
        user_id = sp.current_user()['id']
        playlist = sp.user_playlist_create(user_id, f"AI-Generated: {user_query}", public=True)
        
        # Extract track URIs from recommendations
        track_uris = [track['uri'] for track in recommendations['tracks']]
        
        # Add tracks to the newly created playlist
        sp.user_playlist_add_tracks(user_id, playlist['id'], track_uris)
        
        return f"Playlist created! Check your Spotify account for 'AI-Generated: {user_query}'."
    
    return render_template('playlist_request.html')