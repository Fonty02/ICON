from installLibreries import installPackages
#installPackages()
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from Spotipy.SpotifyAPI import estraiFeature, createCSVDataset, writeSongsInfo,writeClusterInfo,writeRules
from unsupervisonedLearning import calcolaCluster
from balancingPlaylist import visualizeAspectRatioChart, overSampling
from bayesianNetwork import bNetCreation, prediciCluster, generateRandomExample, readBayesianNetwork
from training import trainModelKFold

scaler=MinMaxScaler()
createCSVDataset()

# DATASET CLEANING
fileName = os.path.join(os.path.dirname(__file__), "playlist_tracks.csv")
dataSet = pd.read_csv(fileName)
differentialColumn = "playlistName"


copyDataSet = dataSet.copy()
copyDataSet = copyDataSet.drop(columns=['playlistName'])
# Conserva le colonne 'name' e 'author' prima di rimuoverle
name_author_columns = copyDataSet[['name', 'author']]

# Estrai le colonne che vuoi normalizzare
columns_to_normalize = copyDataSet.columns.difference(['name', 'author'])


# Normalizza le colonne selezionate
copyDataSet[columns_to_normalize] = scaler.fit_transform(copyDataSet[columns_to_normalize])

# Reinserisci le colonne 'name' e 'author'
copyDataSet[['name', 'author']] = name_author_columns

writeSongsInfo(copyDataSet)



# Rimuovi le colonne non utili all'apprendimento
dataSet = dataSet.drop(columns=['name', 'author'])

# Visualizza il rapporto di aspetto del dataset prima del bilanciamento
visualizeAspectRatioChart(dataSet, differentialColumn, "Rapporto delle attuali playlist")

# Eseguo apprendimento non supervisionato per "riclassificare" le playlist
dataSet = dataSet.drop(columns=[differentialColumn])

numeric_columns = dataSet.select_dtypes(include=['float64', 'int64']).columns



# Applica la funzione a ogni elemento del dataset
dataSet[:] = scaler.fit_transform(dataSet)


etichette_cluster, centroidi = calcolaCluster(dataSet)

# Aggiungi la colonna con gli indici dei cluster al dataset originale
differentialColumn = 'clusterIndex'
dataSet[differentialColumn] = etichette_cluster

new_file_path = os.path.join(os.path.dirname(__file__), "newDataset.csv")
dataSet.to_csv(new_file_path, index=False)

writeClusterInfo(dataSet)
writeRules()

# Visualizza il rapporto di aspetto del dataset dopo il non supervisionato
visualizeAspectRatioChart(dataSet, differentialColumn,"Rapporto delle nuove playlist dato il clustering")

# TRAINING
model= trainModelKFold(dataSet, differentialColumn)
# Eseguo oversamping del dataset per bilanciare le classi
oversampled_dataSet = overSampling(dataSet, differentialColumn)
# Visualizza il rapporto di aspetto del dataset dopo il bilanciamento
visualizeAspectRatioChart(oversampled_dataSet, differentialColumn,"POST OVERSAMPLING")
# TRAINING
oversampled_dataSet= trainModelKFold(oversampled_dataSet, differentialColumn)


# BAYESIAN NETWORK
#bayesianNetwork = bNetCreation(dataSet)
bayesianNetwork=readBayesianNetwork()


# PREDICTION
#ESEMPIO CHE GENERA ERRORE
#esempio = estraiFeature("https://open.spotify.com/track/45bE4HXI0AwGZXfZtMp8JR?si=667b1cdc1f9140d8")

#ESEMPIO CHE FUNZIONA
esempio = estraiFeature("https://open.spotify.com/track/3CRDbSIZ4r5MsZ0YwxuEkn?si=daf548cffbc44fa3")
# esempio è un dizionario con le features della canzone.
titolo = esempio['name']
autore = esempio['author']
# remove from the dictionary the name and the author
del esempio['name']
del esempio['author']
# use custom scalr to scale the features of the example
esempio = pd.DataFrame(esempio, index=[0])
esempio[:] = scaler.transform(esempio)
# now turn esempio into a dictionary again
esempio = esempio.to_dict('records')[0]
print("PREDIZIONE DELLA CANZONE: " + titolo + " DI " + autore)
prediciCluster(bayesianNetwork, esempio, "clusterIndex")


esempioRandom = generateRandomExample(bayesianNetwork)
inverseScaled = scaler.inverse_transform(esempioRandom)

# Stampa il nuovo dizionario a schermo
print("ESEMPIO RANDOMICO GENERATO --->  ",inverseScaled)

print("PREDIZIONE DEL SAMPLE RANDOM")
prediciCluster(bayesianNetwork, esempioRandom.to_dict('records')[0], "clusterIndex")
index=numeric_columns.get_loc('energy')
del(esempioRandom['energy'])
#remove indexth-element from inverseScaled
inverseScaled=np.delete(inverseScaled,index)

# Stampa il nuovo dizionario a schermo
print("ESEMPIO RANDOMICO SENZA ENERGY ----> ",inverseScaled)

print("PREDIZIONE DEL SAMPLE RANDOM SENZA ENERGY")
prediciCluster(bayesianNetwork, esempioRandom.to_dict('records')[0], "clusterIndex")