import spotipy
from spotipy.oauth2 import SpotifyOAuth
#import pyswip
import json
import csv
import removeOutliers

#prolog = pyswip.Prolog()
#prolog.consult("prolog2.pl")


username = "fontanaemanuele14"
client_id = '84fb509f9cd542b98121fc8f9f526b51'
client_secret = 'caf49f15a6304b2f85604400812e09d4'
redirect_uri = "http://localhost:8080/mammt"
scope='user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

removeOutliers.softClusteringEMOutliersRemoval('playlist_tracks.csv')
exit()



with open('Playlist.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Crea e apri un file CSV in modalità scrittura
with open('playlist_tracks.csv', 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['playlistName','danceability','energy','key','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Itera attraverso ogni playlist nel JSON
    for playlist in data.get('playlists', []):
        playlist_name = playlist.get('name', '')

        # Verifica se la descrizione è diversa da quella dell'esempio
        if  playlist_name!= "My recommendation playlist":
            items = playlist.get('items', [])
            for item in items:
                track = item.get('track', {})
                if track:
                    track_uri = track.get('trackUri', '')
                    features = sp.audio_features(track_uri)
                    if features:
                        danceability = features[0].get('danceability', '')
                        energy = features[0].get('energy', '')
                        key = features[0].get('key', '')
                        loudness = features[0].get('loudness', '')
                        speechiness = features[0].get('speechiness', '')
                        acousticness = features[0].get('acousticness', '')
                        instrumentalness = features[0].get('instrumentalness', '')
                        liveness = features[0].get('liveness', '')
                        valence = features[0].get('valence', '')
                        tempo = features[0].get('tempo', '')
                        writer.writerow({'playlistName': playlist_name, 'danceability': danceability, 'energy': energy, 'key': key, 'loudness': loudness, 'speechiness': speechiness, 'acousticness': acousticness, 'instrumentalness': instrumentalness, 'liveness': liveness, 'valence': valence, 'tempo': tempo})

