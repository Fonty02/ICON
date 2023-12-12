#from installPackages import installPackages
#installPackages ()

import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from unsupervisonedLearning import calcolaCluster
from balancingPlaylist import visualizeAspectRatioChart, overSampling , underSampling
from bayesianNetwork import bNetCreation
from training import trainModelKFold

# DATASET CLEANING
fileName = os.path.join(os.path.dirname(__file__), "playlist_tracks.csv")
dataSet = pd.read_csv(fileName, low_memory=False)
differentialColumn = "playlistName"


# Specifica la colonna differenziale (differentialColumn)
differentialColumn = 'playlistName'

# Rimuovi le colonne non utili all'apprendimento
dataSet=dataSet.drop(columns=['name','author'])


# Visualizza il rapporto di aspetto del dataset prima del bilanciamento
visualizeAspectRatioChart(dataSet, differentialColumn,"Rapporto delle attuali playlist")



#Eseguo apprendimento non supervisionato per "riclassificare" le playlist
dataSet=dataSet.drop(columns=[differentialColumn])

numeric_columns = dataSet.select_dtypes(include=['float64', 'int64']).columns

etichette_cluster, centroidi = calcolaCluster(dataSet)

# Aggiungi la colonna con gli indici dei cluster al dataset originale
differentialColumn = 'clusterIndex'
dataSet[differentialColumn] = etichette_cluster


new_file_path = os.path.join(os.path.dirname(__file__), "newDataset.csv")
dataSet.to_csv(new_file_path, index=False)



'''

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


# Eseguo undersamping del dataset per bilanciare le classi
undersampled_dataSet = underSampling(dataSet, differentialColumn)
# Visualizza il rapporto di aspetto del dataset dopo il bilanciamento
visualizeAspectRatioChart(undersampled_dataSet, differentialColumn,"POST UNDERSAMPLING")
# TRAINING
undersampled_model= trainModelKFold(undersampled_dataSet, differentialColumn)
'''
# BAYESIAN NETWORK
bayesianNetwork= bNetCreation(dataSet)
#bayesianNetwork.show_graph()





