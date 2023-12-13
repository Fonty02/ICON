import csv
import json
import os

import pandas as pd
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



def write_rule_to_file():
    file_path = "kb.pl"
    with open(file_path, "w", encoding="utf-8") as file:  # Sovrascrivi il file (svuotalo)
        write_fact_to_file(":- encoding(utf8)", file_path)
        fileName = os.path.join(os.path.dirname(__file__), "playlist_tracks.csv")
        dataSet = pd.read_csv(fileName, low_memory=False)
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
            name = name.replace("'", "\\'")  # Escape dell'apostrofo
            author = author.replace("'", "\\'")  # Escape dell'apostrofo
            prolog_clause = f"song({danceability},{energy},{key},{loudness},{speechiness},{acousticness},{instrumentalness},{liveness},{valence},{tempo},'{author}', '{name}')"
            write_fact_to_file(prolog_clause, file_path)
        write_fact_to_file(
                "% Tutte le canzoni di un artista\ncanzoni_di_un_artista(Artist,Title):- song(_, _, _, _, _, _, _, _, _, _, Artist, Title)",
                file_path)
        write_fact_to_file(
                "% Tracce con Elevato Grado di Danzabilità\ntitoli_alta_danzabilita(Titolo) :- song(Danceability, _, _, _, _, _, _, _, _, _, _, Titolo), Danceability >= 0.8",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce con Livello di Energia Elevato\ntitoli_alta_energia(Titolo) :- song(_, Energy, _, _, _, _, _, _, _, _, _, Titolo), Energy >= 0.8",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce Molto Strumentali\ntitoli_molto_strumentale(Titolo) :- song(_, _, _, _, _, _, Instrumentalness, _, _, _, _, Titolo), Instrumentalness >= 0.7",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce in Chiave Maggiore\ntitoli_chiave_maggiore(Titolo) :- song(_, _, Key, _, _, _, _, _, _, _, _, Titolo), Key >= 7",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce con Alta Probabilità di Registrazione Live\ntitoli_registrazione_live(Titolo) :- song(_, _, _, _, _, _, _, Liveness, _, _, _, Titolo), Liveness >= 0.7",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce con Loudness Elevato\ntitoli_loudness_alto(Titolo) :- song(_, _, _, Loudness, _, _, _, _, _, _, _, Titolo), Loudness >= -5.0",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce con Elevata Presenza di Parole Parlate\ntitoli_molto_parlante(Titolo) :- song(_, _, _, _, Speechiness, _, _, _, _, _, _, Titolo), Speechiness >= 0.7",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce con Tempo Vivace (BPM > 120)\ntitoli_tempo_vivace(Titolo) :- song(_, _, _, _, _, _, _, _, _, Tempo, _, Titolo), Tempo >= 120",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce con Valenza Positiva\ntitoli_valenza_positiva(Titolo) :- song(_, _, _, _, _, _, _, _, Valence, _, _, Titolo), Valence >= 0.7",
                file_path)
        write_fact_to_file(
                "% titoli delle tracce con alta probabilità di essere acustiche\ntitoli_alta_acusticità(Titolo) :- song(_, _, _, _, _, Acousticness, _, _, _, _, _, Titolo), Acousticness >= 0.7",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce con bassa danzabilità\ntitoli_bassa_danzabilita(Titolo) :- song(Danceability, _, _, _, _, _, _, _, _, _, _, Titolo), Danceability < 0.8",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce con basso livello di energia\ntitoli_bassa_energia(Titolo) :- song(_, Energy, _, _, _, _, _, _, _, _, _, Titolo), Energy < 0.8",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce Poco Strumentali\ntitoli_poco_strumentale(Titolo) :- song(_, _, _, _, _, _, Instrumentalness, _, _, _, _, Titolo), Instrumentalness < 0.7",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce in Chiave Minore\ntitoli_chiave_minore(Titolo) :- song(_, _, Key, _, _, _, _, _, _, _, _, Titolo), Key < 7",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce con Bassa Probabilità di Registrazione Live\ntitoli_registrazione_non_live(Titolo) :- song(_, _, _, _, _, _, _, Liveness, _, _, _, Titolo), Liveness < 0.7",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce con Loudness Basso\ntitoli_loudness_basso(Titolo) :- song(_, _, _, Loudness, _, _, _, _, _, _, _, Titolo), Loudness < -5.0",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce con Bassa Presenza di Parole Parlate\ntitoli_molto_poco_parlante(Titolo) :- song(_, _, _, _, Speechiness, _, _, _, _, _, _, Titolo), Speechiness < 0.7",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce con Tempo Lento (BPM <= 120)\ntitoli_tempo_lento(Titolo) :- song(_, _, _, _, _, _, _, _, _, Tempo, _, Titolo), Tempo < 120",
                file_path)
        write_fact_to_file(
                "% Titoli delle tracce con Valenza Negativa\ntitoli_valenza_negativa(Titolo) :- song(_, _, _, _, _, _, _, _ , Valence, _, _, Titolo), Valence < 0.7",
                file_path)
        write_fact_to_file(
                "% titoli delle tracce con bassa probabilità di essere acustiche\ntitoli_bassa_acusticità(Titolo) :- song(_, _, _, _, _, Acousticness, _, _, _, _, _, Titolo), Acousticness < 0.7",
                file_path)

        write_fact_to_file(
                "% Ritrova il valore di Danceability dato il titolo\ndanceability_di_titolo(Titolo, Danceability) :- song(Danceability, _, _, _, _, _, _, _, _, _, _, Titolo)",
                file_path)
        write_fact_to_file(
                "% Ritrova il valore di Energy dato il titolo\nenergy_di_titolo(Titolo, Energy) :- song(_, Energy, _, _, _, _, _, _, _, _, _, Titolo)",
                file_path)
        write_fact_to_file(
                "% Ritrova il valore di Key dato il titolo\nkey_di_titolo(Titolo, Key) :- song(_, _, Key, _, _, _, _, _, _, _, _, Titolo)",
                file_path)
        write_fact_to_file(
                "% Ritrova il valore di Loudness dato il titolo\nloudness_di_titolo(Titolo, Loudness) :- song(_, _, _, Loudness, _, _, _, _, _, _, _, Titolo)",
                file_path)
        write_fact_to_file(
                "% Ritrova il valore di Speechiness dato il titolo\nspeechiness_di_titolo(Titolo, Speechiness) :- song(_, _, _, _, Speechiness, _, _, _, _, _, _, Titolo)",
                file_path)
        write_fact_to_file(
            "% Ritrova il valore di Acousticness dato il titolo\nacousticness_di_titolo(Titolo, Acousticness) :- song(_, _, _, _, _, Acousticness, _, _, _, _, _, Titolo)",
            file_path)
        write_fact_to_file(
            "% Ritrova il valore di Instrumentalness dato il titolo\ninstrumentalness_di_titolo(Titolo, Instrumentalness) :- song(_, _, _, _, _, _, Instrumentalness, _, _, _, _, Titolo)",
            file_path)
        write_fact_to_file(
            "% Ritrova il valore di Liveness dato il titolo\nliveness_di_titolo(Titolo, Liveness) :- song(_, _, _, _, _, _, _, Liveness, _, _, _, Titolo)",
            file_path)
        write_fact_to_file(
            "% Ritrova il valore di Valence dato il titolo\nvalence_di_titolo(Titolo, Valence) :- song(_, _, _, _, _, _, _, _, Valence, _, _, Titolo)",
            file_path)
        write_fact_to_file(
            "% Ritrova il valore di Tempo dato il titolo\ntempo_di_titolo(Titolo, Tempo) :- song(_, _, _, _, _, _, _, _,_, Tempo, _, Titolo)",
            file_path)
        write_fact_to_file(
            "% Titoli delle canzoni danzabili di un artista\ntitoli_danzabili_di_artista(Artista, Titolo) :- canzoni_di_un_artista(Artista, Titolo), titoli_alta_danzabilita(Titolo)",
            file_path)
        write_fact_to_file(
            "% Titoli delle canzoni danzabili con molte parole\ntitoli_danzabili_con_molte_parole(Titolo) :- titoli_alta_danzabilita(Titolo), titoli_molto_parlante(Titolo)",
            file_path)
        write_fact_to_file(
            "% Titoli delle canzoni danzabili veloci\ntitoli_danzabili_veloci(Titolo) :- titoli_alta_danzabilita(Titolo), titoli_tempo_vivace(Titolo)",
            file_path)
        write_fact_to_file(
            "% Titoli delle canzoni danzabili lente\ntitoli_danzabili_lente(Titolo) :- titoli_alta_danzabilita(Titolo), titoli_tempo_lento(Titolo)",
            file_path)


"""createCSVDataset()
prolog = Prolog()
prolog.consult("kb.pl")
result = list(prolog.query("titoli_danzabili_di_artista('Ricchi E Poveri', X)"))
for l in result:
   print(l["X"])"""

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
