from installLibreries import installPackages
#installPackages()
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from Spotipy.SpotifyProlog import estraiFeature, createCSVDataset, writeSongsInfo,writeClusterInfo,writeRules
from unsupervisedLearning import calcolaCluster
from balancingPlaylist import visualizeAspectRatioChart, overSampling
from bayesianNetwork import bNetCreation, predici, generateRandomExample, readBayesianNetwork
from supervisedLearning import trainModelKFold

scaler=MinMaxScaler()

# DATASET CLEANING
createCSVDataset()
fileName = os.path.join(os.path.dirname(__file__), "playlist_tracks.csv")
dataSet = pd.read_csv(fileName)
differentialColumn = "playlistName"


#Inizio ragionamento logico


copyDataSet = dataSet.copy()
copyDataSet = copyDataSet.drop(columns=['playlistName'])
#Normalizzo tutte le colonne numeriche e reinserisco le colonne 'name' e 'author'
name_author_columns = copyDataSet[['name', 'author']]
columns_to_normalize = copyDataSet.columns.difference(['name', 'author'])
copyDataSet[columns_to_normalize] = scaler.fit_transform(copyDataSet[columns_to_normalize])
copyDataSet[['name', 'author']] = name_author_columns
writeSongsInfo(copyDataSet)


#APPRENDIMENTO NON SUPERVISIONATO


# Rimuovi le colonne non utili all'apprendimento, visualizza il rapporto di aspetto del dataset
dataSet = dataSet.drop(columns=['name', 'author'])
visualizeAspectRatioChart(dataSet, differentialColumn, "Rapporto delle attuali playlist")
#Normalizzo tutte le colonne numeriche e rimuovo la colonna 'playlistName'
dataSet = dataSet.drop(columns=[differentialColumn])
numeric_columns = dataSet.select_dtypes(include=['float64', 'int64']).columns
dataSet[:] = scaler.fit_transform(dataSet)
#Eseguo il KMeans
etichette_cluster, centroidi = calcolaCluster(dataSet)
#Creo il nuovo dataset con la colonna 'clusterIndex'
differentialColumn = 'clusterIndex'
dataSet[differentialColumn] = etichette_cluster
new_file_path = os.path.join(os.path.dirname(__file__), "newDataset.csv")
dataSet.to_csv(new_file_path, index=False)

#Termino la parte di ragionamento logico
writeClusterInfo(dataSet)
writeRules()

# Visualizza il rapporto di aspetto del dataset dopo il non supervisionato
visualizeAspectRatioChart(dataSet, differentialColumn,"Rapporto delle nuove playlist dato il clustering")


# APPRENDIMENTO SUPERVISIONATO

#Addestro e valuto i modelli
model= trainModelKFold(dataSet, differentialColumn)
# Eseguo oversamping del dataset per bilanciare le classi
oversampled_dataSet = overSampling(dataSet, differentialColumn)
visualizeAspectRatioChart(oversampled_dataSet, differentialColumn,"POST OVERSAMPLING")
#Addestro e valuto i modelli dopo l'oversampling
oversampled_dataSet= trainModelKFold(oversampled_dataSet, differentialColumn)


# RAGIONAMENTO PROBABILISTICO


#Leggo o creo la rete bayesiana a seconda delle necessità
bayesianNetwork = bNetCreation(dataSet)
#bayesianNetwork=readBayesianNetwork()

# TASK DI CLASSIFICAZIONE

#ESEMPIO CHE GENERA ERRORE
#esempio = estraiFeature("https://open.spotify.com/track/45bE4HXI0AwGZXfZtMp8JR?si=667b1cdc1f9140d8")

#ESEMPIO CHE FUNZIONA
esempio = estraiFeature("https://open.spotify.com/track/3CRDbSIZ4r5MsZ0YwxuEkn?si=daf548cffbc44fa3")
# esempio è un dizionario con le features della canzone.
titolo = esempio['name']
autore = esempio['author']
del esempio['name']
del esempio['author']
esempio = pd.DataFrame(esempio, index=[0])
esempio[:] = scaler.transform(esempio)
esempio = esempio.to_dict('records')[0]
print("PREDIZIONE DELLA CANZONE: " + titolo + " DI " + autore)
predici(bayesianNetwork, esempio, "clusterIndex")

#GENERAZIONE DI UN ESEMPIO RANDOMICO e PREDIZIONE DELLA SUA CLASSE
esempioRandom = generateRandomExample(bayesianNetwork)
inverseScaled = scaler.inverse_transform(esempioRandom)
print("ESEMPIO RANDOMICO GENERATO --->  ",inverseScaled)
print("PREDIZIONE DEL SAMPLE RANDOM")
predici(bayesianNetwork, esempioRandom.to_dict('records')[0], "clusterIndex")

#RIMOZIONE DI UNA FEATURE E PREDIZIONE DELLA SUA CLASSE
index=numeric_columns.get_loc('energy')
del(esempioRandom['energy'])
inverseScaled=np.delete(inverseScaled,index)
print("ESEMPIO RANDOMICO SENZA ENERGY ----> ",inverseScaled)
print("PREDIZIONE DEL SAMPLE RANDOM SENZA ENERGY")
predici(bayesianNetwork, esempioRandom.to_dict('records')[0], "clusterIndex")