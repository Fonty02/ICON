#from installPackages import installPackages
#installPackages ()

import os

import pandas as pd

from balancingPlaylist import resampleDataset, visualizeAspectRatioChart
#from bayesianNetwork import bayesianNetwork
from removeOutliers import softClusteringEMOutliersRemoval
#from training import trainModelKFold, visualizeMetricsGraphs
#from verificationFeaturesImportance import (createXfeatureAndyTarget,visualizeFeaturesImportances)


# DATASET CLEANING
fileName = os.path.join(os.path.dirname(__file__), "playlist_tracks.csv")
dataSet = pd.read_csv(fileName)
differentialColumn = "playlistName"


print("\nInfo dataset:\n", dataSet.describe())

# Richiama la funzione di clustering non supervisionato
dataSet = softClusteringEMOutliersRemoval(dataSet)

# Specifica la colonna differenziale (differentialColumn)
differentialColumn = 'playlistName'

# Estrai i nomi delle playlist uniche
playlistNames = dataSet[differentialColumn].unique()

# Visualizza il rapporto di aspetto del dataset prima del bilanciamento
visualizeAspectRatioChart(dataSet, differentialColumn, playlistNames)

# Esegui il resampling del dataset per bilanciare le classi
dataSet = resampleDataset(dataSet, differentialColumn)

# Visualizza il rapporto di aspetto del dataset dopo il bilanciamento
visualizeAspectRatioChart(dataSet, differentialColumn, playlistNames)


"""
# TRAINING
model, X_test, y_test, knn, dtc, rfc, svc, bnb, gnb = trainModelKFold(
    dataSet, differentialColumn)
visualizeMetricsGraphs(model, X_test, y_test, knn, dtc, rfc, svc, bnb, gnb)


# VERIFICATION OF THE IMPORTANCE OF FEATURES
rfc_model, X = createXfeatureAndyTarget(dataSet, differentialColumn)

visualizeFeaturesImportances(rfc_model, X)


# BAYESIAN NETWORK
bayesianNetwork(dataSet, differentialColumn)
"""