#from installPackages import installPackages
#installPackages ()

import os

import pandas as pd

from balancingPlaylist import resampleDataset, visualizeAspectRatioChart
# from bayesianNetwork import bayesianNetwork
from removeOutliers import softClusteringEMOutliersRemoval
from training import trainModelKFold

# DATASET CLEANING
fileName = os.path.join(os.path.dirname(__file__), "playlist_tracks.csv")
dataSet = pd.read_csv(fileName, low_memory=False)
differentialColumn = "playlistName"


print("\nInfo dataset:\n", dataSet.describe())


# Specifica la colonna differenziale (differentialColumn)
differentialColumn = 'playlistName'




#PREPROCESSING
dataSet[differentialColumn] = dataSet[differentialColumn].apply(
   lambda x: 1 if x == "Mhe" else 0)


dataSet=dataSet.drop(columns=['name','author'])

# Richiama la funzione di clustering non supervisionato
dataSet = softClusteringEMOutliersRemoval(dataSet)

# Visualizza il rapporto di aspetto del dataset prima del bilanciamento
visualizeAspectRatioChart(dataSet, differentialColumn)

# TRAINING
model= trainModelKFold(dataSet, differentialColumn)

# Esegui il resampling del dataset per bilanciare le classi
dataSet = resampleDataset(dataSet, differentialColumn)
# Visualizza il rapporto di aspetto del dataset dopo il bilanciamento
visualizeAspectRatioChart(dataSet, differentialColumn)

# TRAINING
model= trainModelKFold(dataSet, differentialColumn)


'''
# BAYESIAN NETWORK
bayesianNetwork(dataSet, differentialColumn)
'''

