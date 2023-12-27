# from installPackages import installPackages
# installPackages ()
import math
import os

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from unsupervisonedLearning import calcolaCluster
from balancingPlaylist import visualizeAspectRatioChart, overSampling, underSampling
from bayesianNetwork import bNetCreation, prediciCluster, generateRandomExample, readBayesianNetwork
from training import trainModelKFold
from SpotifyAPI import estraiFeature

# DATASET CLEANING
fileName = os.path.join(os.path.dirname(__file__), "playlist_tracks.csv")
dataSet = pd.read_csv(fileName)
differentialColumn = "playlistName"

# Specifica la colonna differenziale (differentialColumn)
differentialColumn = 'playlistName'

# Rimuovi le colonne non utili all'apprendimento
dataSet = dataSet.drop(columns=['name', 'author'])

# Visualizza il rapporto di aspetto del dataset prima del bilanciamento
visualizeAspectRatioChart(dataSet, differentialColumn, "Rapporto delle attuali playlist")

# Eseguo apprendimento non supervisionato per "riclassificare" le playlist
dataSet = dataSet.drop(columns=[differentialColumn])

numeric_columns = dataSet.select_dtypes(include=['float64', 'int64']).columns

scaler=MinMaxScaler()

def custom_scaling(value):
    return int((math.cos(value) + 1) / 2 * 100)


# Applica la funzione a ogni elemento del dataset
dataSet[:] = scaler.fit_transform(dataSet)

etichette_cluster, centroidi = calcolaCluster(dataSet)

# Aggiungi la colonna con gli indici dei cluster al dataset originale
differentialColumn = 'clusterIndex'
dataSet[differentialColumn] = etichette_cluster

new_file_path = os.path.join(os.path.dirname(__file__), "newDataset.csv")
dataSet.to_csv(new_file_path, index=False)


# Visualizza il rapporto di aspetto del dataset dopo il non supervisionato
visualizeAspectRatioChart(dataSet, differentialColumn,"Rapporto delle nuove playlist dato il clustering")

# TRAINING
model= trainModelKFold(dataSet, differentialColumn)

'''
# Eseguo oversamping del dataset per bilanciare le classi
oversampled_dataSet = overSampling(dataSet, differentialColumn)
# Visualizza il rapporto di aspetto del dataset dopo il bilanciamento
visualizeAspectRatioChart(oversampled_dataSet, differentialColumn,"POST OVERSAMPLING")
# TRAINING
oversampled_dataSet= trainModelKFold(oversampled_dataSet, differentialColumn)


# Eseguo undersamping del dataset per bilanciare le classi
undersampled_dataSet = underSampling(dataSet, differentialColumn)
# Visualizza il rapporto di aspetto del dataset dopo il bilanciamento
visualizeAspectRatioChart(undersampled_dataSet, differentialColumn,"POST UNDERSAMPLING")
# TRAINING
undersampled_model= trainModelKFold(undersampled_dataSet, differentialColumn)


# BAYESIAN NETWORK
#bayesianNetwork = bNetCreation(dataSet)
bayesianNetwork=readBayesianNetwork()
# PREDICTION
esempio = estraiFeature("https://open.spotify.com/track/0qMip0B2D4ePEjBJvAtYre?si=bd2b9ffdf8ed4219")
# esempio è un dizionario con le features della canzone.
titolo = esempio['name']
autore = esempio['author']
# remove from the dictionary the name and the author
del esempio['name']
del esempio['author']
# use custom scalr to scale the features of the example
esempio = pd.DataFrame(esempio, index=[0])
esempio = scaler.transform(esempio)
# now turn esempio into a dictionary in esempioDict
esempioDict = {}
for i in range(len(esempio[0])):
    esempioDict[numeric_columns[i]] = esempio[0][i]
esempio = esempioDict
print("PREDIZIONE DELLA CANZONE: " + titolo + " DI " + autore)
prediciCluster(bayesianNetwork, esempio, "clusterIndex")


def inverse_custom_scaling(scaled_value):
    # Riporta il valore scalato nell'intervallo [0, 1]
    scaled_value /= 100.0
    angle = math.acos(float(scaled_value.iloc[0]))

    return angle


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
'''