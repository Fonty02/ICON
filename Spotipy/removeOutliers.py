import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture


def softClusteringEMOutliersRemoval(dataSet):
    # Carica il tuo file CSV
    df = dataSet

    # Seleziona solo le colonne contenenti le feature delle canzoni (escludi la colonna con i nomi delle playlist)
    song_features = df.drop('playlistName', axis=1)

    # Imposta il numero di componenti nel modello GMM (una per ogni playlist + 1 per gli outliers)
    n_components = len(df['playlistName'].unique()) + 1
    print(n_components)
    gmm = GaussianMixture(n_components=n_components)

    # Addestra il modello GMM
    gmm.fit(song_features)

    # Calcola la log-likelihood per ogni campione
    likelihoods = gmm.score_samples(song_features)

    # Imposta una soglia per identificare gli outliers
    outlier_threshold = np.mean(likelihoods) - 3 * np.std(likelihoods)

    # Identifica gli outliers
    outliers = np.where(likelihoods < outlier_threshold)[0]

    # Rimuovi gli outliers dal dataframe
    cleaned_df = df.drop(outliers)

    # Stampa informazioni sulla pulizia
    print('Removed ' +  str(len(outliers)) + ' outliers from the dataset. Cleaned dataset size: ' + str(cleaned_df.shape))

    # Salva il dataframe pulito in un nuovo file CSV
    cleaned_df.to_csv('cleaned_dataset.csv', index=False)

    return cleaned_df
