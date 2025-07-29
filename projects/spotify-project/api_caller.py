"""
Spotify API Data Collection Module

This module collects Brazilian Hip Hop playlist data from Spotify API, including
track information and audio features for data analysis purposes.

The script fetches playlists from the Hip Hop category in Brazil, extracts track
metadata, and enriches it with audio features like tempo, loudness, and energy.
All data is saved as both JSON and CSV formats with comprehensive logging.

Dependencies:
    - spotipy: Spotify Web API wrapper
    - pandas: Data manipulation and analysis
    - tqdm: Progress bars
    - dotenv: Environment variable management

Environment Variables Required:
    - SPOTIPY_CLIENT_ID: Spotify API client ID
    - SPOTIPY_CLIENT_SECRET: Spotify API client secret

Example:
    python api_caller.py
"""

from datetime import datetime, date
import json
import logging
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('spotify_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

COUNTRY_ID = 'BR'
HIPHOP_CATEGORY_ID = 'hiphop'
LOCALE = 'pt_BR'

logger.info("Initializing Spotify client...")
try:
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    logger.info("Spotify client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Spotify client: {e}")
    raise

def save_dict_as_json(filename, data):
    logger.info(f"Saving data to {filename}.json with {len(data)} items")
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(f'{filename}.json', 'w') as fp:
            json.dump(data, fp)
        logger.info(f"Successfully saved data to {filename}.json")
    except Exception as e:
        logger.error(f"Failed to save data to {filename}.json: {e}")
        raise

def collect_category_playlists(category_id, num_lim=5):
    logger.info(f"Collecting {num_lim} playlists from category '{category_id}' in country '{COUNTRY_ID}'")
    try:
        results = spotify.search(q=category_id, type='playlist', market=COUNTRY_ID, limit=num_lim)
        # results = spotify.category_playlists(category_id, country=COUNTRY_ID, limit=num_lim)
        logger.debug(f"Results: {results}")
        playlist_count = len(results['playlists']['items'])
        logger.info(f"Successfully collected {playlist_count} playlists from category '{category_id}'")
        return results
    except Exception as e:
        logger.error(f"Failed to collect playlists from category '{category_id}': {e}")
        raise

def get_playlists_ids(data):
    playlists = data['playlists']
    items = playlists['items']
    ids = []

    logger.info(f"Getting items = {items}")
    for item in items:
        if item is None:
            logger.warning(f"Item has no ID: {item}")
            continue
        ids.append(item['id'])
    return ids

def get_playlists_names(data):
    playlists = data['playlists']
    items = playlists['items']
    names = []
    for item in items:
        if item is None:
            logger.warning(f"Item has no name: {item}")
            continue
        names.append(item['name'])
    return names

def get_playlists_descriptions(data):
    playlists = data['playlists']
    items = playlists['items']
    descriptions = []
    for item in items:
        if item is None:
            logger.warning(f"Item has no description: {item}")
            continue
        descriptions.append(item['description'])
    return descriptions

def get_playlist_info(playlist):
    logger.debug(f"Getting info for playlist: {playlist}")
    try:
        return spotify.playlist(playlist)
    except Exception as e:
        logger.error(f"Failed to get info for playlist {playlist}: {e}")
        raise

def get_playlist_tracks(playlist):
    logger.debug(f"Getting tracks for playlist: {playlist}")
    try:
        tracks = get_playlist_info(playlist)['tracks']['items']
        logger.debug(f"Found {len(tracks)} tracks in playlist {playlist}")
        return tracks
    except Exception as e:
        logger.error(f"Failed to get tracks for playlist {playlist}: {e}")
        raise

def get_track_info(track):
    track_unwrapped = track['track']
    return {
        'added_at': track['added_at'],
        'album_name': track_unwrapped['album']['name'],
        'track_number': track_unwrapped['track_number'],
        'artists': [(artist['name'], artist['id'])  for artist in track_unwrapped['artists']],
        'name': track_unwrapped['name'],
        'popularity': track_unwrapped['popularity'],
        'track_id': track_unwrapped['id']
    }

def aggregate_track_info_with_audio_features(track_info):
    track_id = track_info['track_id']
    logger.debug(f"Getting audio features for track: {track_id}")
    try:
        audio_features = spotify.audio_features(track_id)
        if audio_features and audio_features[0]:
            track_info.update(audio_features[0])
            logger.debug(f"Successfully added audio features for track: {track_id}")
        else:
            logger.warning(f"No audio features found for track: {track_id}")
    except Exception as e:
        logger.error(f"Failed to get audio features for track {track_id}: {e}")
        raise
    
def load_json(json_file_path):
    logger.info(f"Loading JSON data from {json_file_path}.json")
    try:
        with open(f'{json_file_path}.json', 'r') as fp:
            data = json.load(fp)
        logger.info(f"Successfully loaded {len(data)} items from {json_file_path}.json")
        return data
    except Exception as e:
        logger.error(f"Failed to load JSON from {json_file_path}.json: {e}")
        raise

def dict_to_dataframe(dic):
    logger.info(f"Converting {len(dic)} items to DataFrame")
    try:
        df = pd.DataFrame(dic)
        logger.info(f"Successfully created DataFrame with shape {df.shape}")
        return df
    except Exception as e:
        logger.error(f"Failed to create DataFrame: {e}")
        raise

def main():
    '''
    Collects track information.
    
    We first collect the playlists related to Hip Hop on BR.
    Then, collect track info for every track on this respective playlist.
    We aggregate track info such as tempo, loudness, liveness and etc.
    
    API reference: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features
    '''
    logger.info("Starting Spotify data collection process")
    
    data_folder = 'data'
    
    logger.info("Phase 1: Collecting Hip Hop playlists")
    hip_hop_playlists = collect_category_playlists(HIPHOP_CATEGORY_ID, num_lim=20)
    playlist_ids = get_playlists_ids(hip_hop_playlists)
    playlist_names = get_playlists_names(hip_hop_playlists)
    playlist_descriptions = get_playlists_descriptions(hip_hop_playlists)
    
    logger.info(f"Collected {len(playlist_ids)} playlists: {playlist_names}")

    today_with_hours_and_minutes = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    logger.info(f"Session timestamp: {today_with_hours_and_minutes}")

    tracks = list()
    total_playlists = len(playlist_ids)
    
    logger.info("Phase 2: Processing tracks from playlists")
    
    for idx, (pl_id, pl_name, pl_description) in enumerate(tqdm(zip(playlist_ids, playlist_names, playlist_descriptions), desc="Processing playlists"), 1):
        logger.info(f"Processing playlist {idx}/{total_playlists}: '{pl_name}' (ID: {pl_id})")
        
        try:
            playlist_track = get_playlist_tracks(pl_id)
            playlist_track_count = len(playlist_track)
            logger.info(f"Found {playlist_track_count} tracks in playlist '{pl_name}'")
            
            for track_idx, track in enumerate(playlist_track, 1):
                try:
                    track_info = get_track_info(track)
                    # aggregate_track_info_with_audio_features(track_info)
                    track_info.update({'playlist_name': pl_name, 'playlist_description': pl_description})
                    tracks.append(track_info)
                    
                    if track_idx % 10 == 0:
                        logger.info(f"Processed {track_idx}/{playlist_track_count} tracks from playlist '{pl_name}'")
                        
                except Exception as e:
                    logger.error(f"Failed to process track {track_idx} from playlist '{pl_name}': {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to process playlist '{pl_name}' (ID: {pl_id}): {e}")
            continue

    total_tracks = len(tracks)
    logger.info(f"Phase 3: Saving {total_tracks} tracks to files")

    filename = f'{data_folder}/json/{today_with_hours_and_minutes}/track_list_with_features'
    save_dict_as_json(filename, tracks)
    
    logger.info("Converting to DataFrame and saving as CSV")
    try:
        csv_filename = f'{data_folder}/csv/{today_with_hours_and_minutes}/df.csv'
        os.makedirs(os.path.dirname(csv_filename), exist_ok=True)
        dict_to_dataframe(load_json(filename)).to_csv(csv_filename, index=False)
        logger.info(f"Successfully saved CSV to {csv_filename}")
    except Exception as e:
        logger.error(f"Failed to save CSV: {e}")
        raise
    
    logger.info(f"Data collection completed successfully! Processed {total_playlists} playlists and {total_tracks} tracks")

    
if __name__ == '__main__':
    main()