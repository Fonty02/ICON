import matplotlib.pyplot as plt
import pandas as pd
from sklearn.utils import resample

from stampe import prGreenMoreString, prRedMoreString, prYellow


def resampleDataset(dataSet, differentialColumn):
    # Trova il numero massimo di canzoni in una playlist
    maxSongsPerPlaylist = dataSet[differentialColumn].value_counts().max()

    # Lista delle playlist
    playlistNames = dataSet[differentialColumn].unique()

    # Oversample ogni playlist
    oversampled_data = []
    for playlist in playlistNames:
        # Seleziona le canzoni della playlist corrente
        playlist_data = dataSet[dataSet[differentialColumn] == playlist]

        # Calcola il numero di campioni da generare per raggiungere la dimensione target
        n_samples = maxSongsPerPlaylist - len(playlist_data)

        # Esegui l'oversampling solo se il numero di campioni è positivo
        if n_samples > 0:
            playlist_oversampled = resample(playlist_data, replace=True, n_samples=n_samples, random_state=42)
            oversampled_data.append(playlist_oversampled)

    # Unisci i dati oversampled
    dataSet = pd.concat([dataSet] + oversampled_data)

    prYellow("\nValue after Oversampling:")
    print(dataSet[differentialColumn].value_counts())  # Stampa il conteggio delle canzoni per ogni playlist dopo l'oversampling

    return dataSet






def visualizeAspectRatioChart(dataSet, differentialColumn, labels):
    ax = dataSet[differentialColumn].value_counts().plot(
        kind='pie', figsize=(5, 5), labels=None)
    ax.axes.get_yaxis().set_visible(False)
    plt.title("Grafico delle canzoni per playlist")
    plt.legend(labels=labels, loc="best")
    plt.show()
    plt.clf()

