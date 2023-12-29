import csv
import json

import spotipy
from pyswip import Prolog
from spotipy.oauth2 import SpotifyOAuth

username = "fontanaemanuele14"
client_id = '84fb509f9cd542b98121fc8f9f526b51'
client_secret = 'caf49f15a6304b2f85604400812e09d4'
redirect_uri = "http://localhost:8080/mammt"
scope = 'user-library-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))




def createCSVDataset():
    with open('Playlist.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Crea e apri un file CSV in modalità scrittura
    with open('playlist_tracks.csv', 'w', newline='', encoding='utf-8') as csv_file:
        # Inserisci il nome dell autore della canzone
        fieldnames = ['playlistName', 'danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness',
                      'instrumentalness', 'liveness', 'valence', 'tempo', 'author', 'name']
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
                                 'liveness': liveness, 'valence': valence, 'tempo': tempo, 'author': author,
                                 'name': name})


def write_fact_to_file(fact, file_path):
    # Verifica se il fatto è già presente
    with open(file_path, 'r', encoding='utf-8') as file:
        existing_content = file.read()

    if fact not in existing_content:
        # Riapri il file in modalità append e scrivi il fatto
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(f"{fact}.\n")



def writeSongsInfo(dataSet):
    file_path = "kb.pl"
    with open(file_path, "w", encoding="utf-8") as file:  # Sovrascrivi il file (svuotalo)
        write_fact_to_file(":- encoding(utf8)", file_path)
        for index, row in dataSet.iterrows():
            danceability = "{:f}".format(row['danceability'])
            energy = "{:f}".format(row['energy'])
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
            #remove the ' from the name and the author
            name=name.replace("'", "")
            author=author.replace("'", "")
            prolog_clause = f"song({danceability},{energy},{key},{loudness},{speechiness},{acousticness},{instrumentalness},{liveness},{valence},{tempo},'{author}', '{name}')"
            write_fact_to_file(prolog_clause, file_path)


def writeClusterInfo(dataSet):
    file_path = "kb.pl"
    #oepn file in append mode
    with open(file_path, "a", encoding="utf-8") as file:  # Sovrascrivi il file (svuotalo)
        for index, row in dataSet.iterrows():
            danceability = "{:f}".format(row['danceability'])
            energy = "{:f}".format(row['energy'])
            key = row['key']
            loudness = "{:f}".format(row['loudness'])
            speechiness = "{:f}".format(row['speechiness'])
            acousticness = "{:f}".format(row['acousticness'])
            instrumentalness = "{:f}".format(row['instrumentalness'])
            liveness = "{:f}".format(row['liveness'])
            valence = "{:f}".format(row['valence'])
            tempo = "{:f}".format(row['tempo'])
            clusterIndex = row['clusterIndex']
            prolog_clause = f"clustered_song({danceability},{energy},{key},{loudness},{speechiness},{acousticness},{instrumentalness},{liveness},{valence},{tempo},{clusterIndex})"
            write_fact_to_file(prolog_clause, file_path)



def writeRules():
    with open("kb.pl", "a", encoding="utf-8") as file:
        rule="canzoni_info(NomeCanzone, Autore, Cluster) :- ( song(A1, B1, C1, D1, E1, F1, G1, H1, I1, L1, Autore, NomeCanzone), clustered_song(A2, B2, C2, D2, E2, F2, G2, H2, I2, L2, Cluster) ), A1= A2, B1 = B2, C1 = C2, D1 = D2, E1 = E2, F1 = F2, G1 = G2, H1 = H2, I1 = I2, L1 = L2"
        write_fact_to_file(rule, "kb.pl")
    prolog = Prolog()
    prolog.consult("kb.pl")
    clustersIndex=set()
    with open("newDataset.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            clustersIndex.add(row['clusterIndex'])
    clustersIndex = [float(i) for i in clustersIndex]
    for i in clustersIndex:
        print("Cluster: ", i)
        result = list(prolog.query("canzoni_info(Nome, Autore, "+str(i)+")"))
        for l in result:
            print(l["Nome"], l["Autore"])
        print("\n\n")







def estraiFeature(track_uri):
    #return a dictionary with the features of the track. Feature is the key, value is the value of the feature
    fieldnames = ['danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness',
                  'instrumentalness', 'liveness', 'valence', 'tempo', 'author', 'name']
    features = sp.audio_features(track_uri)
    tackInfo = sp.track(track_uri)
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
    return {'danceability': danceability, 'energy': energy,
                'key': key, 'loudness': loudness, 'speechiness': speechiness,
                'acousticness': acousticness, 'instrumentalness': instrumentalness,
                'liveness': liveness, 'valence': valence, 'tempo': tempo, 'author': author,
                'name': name}

