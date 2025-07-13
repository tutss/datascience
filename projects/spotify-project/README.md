# Spotify Brazilian Rap data analysis a.k.a. Pique

Brazilian rap data analysis with Spotify data, collected via API.

Qual a cena do rap?

## Data collection
### api_caller.py

`api_caller.py` calls Spotify API.

It needs:
- export client ID on local terminal: SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET
    - collected via [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)
    - Spotipy docs: [link](https://spotipy.readthedocs.io/en/2.9.0/)
    
- needs to aggregate musics outside major playlists as well
    
## Preprocessing
### preprocessing.ipynb

Dataset date is fixed by the last data collection time.

Columns description can be found here as well as in [Spotify docs](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features).

It:
- removes duplicates by song name (remain only one, even if they are on different playlists)
- maps the artists name into a readable list without artist id
- removes unnecessary columns
- maps datetime column
- saves dataset with only BR related songs

## Data analysis
### analysis.ipynb
WIP

## Inference
### inference.ipynb
WIP