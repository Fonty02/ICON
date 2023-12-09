import os
import re
import pandas as pd
from pyswip import Prolog
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pyswip
import json
import csv





username = "fontanaemanuele14"
client_id = '84fb509f9cd542b98121fc8f9f526b51'
client_secret = 'caf49f15a6304b2f85604400812e09d4'
redirect_uri = "http://localhost:8080/mammt"
scope='user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

def notAuthor():
    with open('Playlist.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Crea e apri un file CSV in modalità scrittura
    with open('playlist_tracks.csv', 'w', newline='', encoding='utf-8') as csv_file:
        #Inserisci il nome dell autore della canzone
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


def withAuthor():
    with open('Playlist.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Crea e apri un file CSV in modalità scrittura
    with open('playlist_tracks2.csv', 'w', newline='', encoding='utf-8') as csv_file:
        # Inserisci il nome dell autore della canzone
        fieldnames = ['playlistName', 'danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness',
                      'instrumentalness', 'liveness', 'valence', 'tempo', 'author','name']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Itera attraverso ogni playlist nel JSON
        for playlist in data.get('playlists', []):
            playlist_name = playlist.get('name', '')

            # Verifica se la descrizione è diversa da quella dell'esempio
            if playlist_name != "My recommendation playlist":
                items = playlist.get('items', [])
                for item in items:
                    track = item.get('track', {})
                    if track:
                        track_uri = track.get('trackUri', '')
                        features = sp.audio_features(track_uri)
                        tackInfo = sp.track(track_uri)
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
                            author = tackInfo['artists'][0]['name']
                            name = tackInfo['name']
                            writer.writerow(
                                {'playlistName': playlist_name, 'danceability': danceability, 'energy': energy,
                                 'key': key, 'loudness': loudness, 'speechiness': speechiness,
                                 'acousticness': acousticness, 'instrumentalness': instrumentalness,
                                 'liveness': liveness, 'valence': valence, 'tempo': tempo, 'author': author, 'name': name})

def write_fact_to_file(fact, file):
    file.write(f"{fact}.\n")


def write_rule_to_file():
    fileName = os.path.join(os.path.dirname(__file__), "playlist_tracks2.csv")
    dataSet = pd.read_csv(fileName, low_memory=False)
    for index, row in dataSet.iterrows():
        danceability = "{:f}".format(row['danceability'])
        energy =  "{:f}".format(row['energy'])
        key = row['key']
        loudness = "{:f}".format(row['loudness'])
        speechiness = "{:f}".format(row['speechiness'])
        acousticness = "{:f}".format(row['acousticness'])
        instrumentalness = "{:f}".format(row['instrumentalness'])
        liveness = "{:f}".format(row['liveness'])
        valence = "{:f}".format(row['valence'])
        tempo = "{:f}".format(row['tempo'])
        author = row['author']
        name = row['name']
        name = re.sub(r'\W+', '_', name)
        author = re.sub(r'\W+', '_', author)
        prolog_clause = f"song({danceability},{energy},{key},{loudness},{speechiness},{acousticness},{instrumentalness},{liveness},{valence},{tempo},'{author}', '{name}')"
        prolog.assertz(prolog_clause)
        with open("kb.pl", "a") as file:
            write_fact_to_file(prolog_clause, file)



prolog = Prolog()
prolog.consult("kb.pl")
result = list(prolog.query("titoli_danzabili_di_artista('Ricchi_E_Poveri', X)"))
for l in result:
    print(l["X"])



