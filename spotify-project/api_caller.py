from datetime import datetime, date
import json

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm
import pandas as pd

COUNTRY_ID = 'BR'
hiphop_category_id = 'hiphop'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def save_dict(filename, data):
    with open(f'{filename}.json', 'w') as fp:
        json.dump(data, fp)

def collect_category_playlists(category_id, num_lim=5):
    results = spotify.category_playlists(category_id, country=COUNTRY_ID, limit=num_lim)
    return results

def get_playlists_ids(data):
    playlists = data['playlists']
    items = playlists['items']
    ids = []
    for item in items:
        ids.append(item['id'])
    return ids

def get_playlists_names(data):
    playlists = data['playlists']
    items = playlists['items']
    names = []
    for item in items:
        names.append(item['name'])
    return names

def get_playlists_descriptions(data):
    playlists = data['playlists']
    items = playlists['items']
    descriptions = []
    for item in items:
        descriptions.append(item['description'])
    return descriptions

def get_playlist_info(playlist):
    return spotify.playlist(playlist)

def get_playlist_tracks(playlist):
    return get_playlist_info(playlist)['tracks']['items']

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
    audio_features = spotify.audio_features(track_info['track_id'])
    track_info.update(audio_features[0])
    
def load_json(json_file_path):
    with open(f'{json_file_path}.json', 'r') as fp:
        data = json.load(fp)
    return data

def dict_to_dataframe(dic):
    df = pd.DataFrame(dic)
    return df

def main():
    '''
    Collects track information.
    
    We first collect the playlists related to Hip Hop on BR.
    Then, collect track info for every track on this respective playlist.
    We aggregate track info such as tempo, loudness, liveness and etc.
    
    API reference: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features
    '''
    now = str(date.today())
    folder = 'track_list_json'
    
    hip_hop_playlists = collect_category_playlists(hiphop_category_id, num_lim=20)
    playlist_ids = get_playlists_ids(hip_hop_playlists)
    playlist_names = get_playlists_names(hip_hop_playlists)
    playlist_descriptions = get_playlists_descriptions(hip_hop_playlists)

    tracks = list()
    tracks_audio_features = list()
    
    for pl_id, pl_name, pl_description in tqdm(zip(playlist_ids, playlist_names, playlist_descriptions)):
        playlist_track = get_playlist_tracks(pl_id)
        for track in playlist_track:
            track_info = get_track_info(track)
            aggregate_track_info_with_audio_features(track_info)
            track_info.update({'playlist_name': pl_name, 'playlist_description': pl_description})
            tracks.append(track_info)

    filename = f'{folder}/track_list_with_features_{now}'
    save_dict(filename, tracks)
    dict_to_dataframe(load_json(filename)).to_csv(f'data/df_{now}.csv', index=False)

    
main()