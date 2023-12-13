import matplotlib.pyplot as plt
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler


def underSampling(dataSet, differentialColumn):
    # Filtra il dataset per includere solo le righe con valori validi nella colonna specificata
    dataSet = dataSet.dropna(subset=[differentialColumn])

    X = dataSet.drop(columns=[differentialColumn])
    y = dataSet[differentialColumn]

    # Creazione di un oggetto RandomUnderSampler
    under_sampler = RandomUnderSampler(random_state=42)

    # Applicazione di RandomUnderSampler al dataset
    X_resampled, y_resampled = under_sampler.fit_resample(X, y)

    # Creazione di un nuovo DataFrame con i dati resampled
    dataSet_resampled = pd.DataFrame(X_resampled, columns=X.columns)
    dataSet_resampled[differentialColumn] = y_resampled

    # Stampa in giallo la scritta "UNDERSAMPLING EFFETTUATO CON SUCCESSO"
    print('\033[93m' + "UNDERSAMPLING EFFETTUATO CON SUCCESSO" + '\033[0m')

    return dataSet_resampled


def overSampling(dataSet, differentialColumn):
    # Filtra il dataset per includere solo le righe con valori validi nella colonna specificata
    dataSet = dataSet.dropna(subset=[differentialColumn])

    X = dataSet.drop(columns=[differentialColumn])
    y = dataSet[differentialColumn]

    # Creazione di un oggetto SMOTE
    smote = SMOTE(random_state=42)

    # Applicazione di SMOTE al dataset
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Creazione di un nuovo DataFrame con i dati resampled
    dataSet_resampled = pd.DataFrame(X_resampled, columns=X.columns)
    dataSet_resampled[differentialColumn] = y_resampled

    # Stampa in giallo la scritta "OVERSAMPLING EFFETTUATO CON SUCCESSO"
    print('\033[93m' + "OVERSAMPLING EFFETTUATO CON SUCCESSO" + '\033[0m')

    return dataSet_resampled

def visualizeAspectRatioChart(dataSet, differentialColumn, title):
    # Conta le occorrenze per ciascun valore unico di differentialColumn
    counts = dataSet[differentialColumn].value_counts()

    # Etichette e colori per il grafico
    labels = counts.index.tolist()
    colors = ['lightcoral', 'lightskyblue', 'lightgreen', 'gold', 'mediumorchid', 'lightsteelblue']  # Aggiungi altri colori se necessario

    # Crea il grafico a torta
    fig, ax = plt.subplots(figsize=(8, 8))  # Imposta una dimensione più grande per il grafico
    wedges, texts, autotexts = ax.pie(counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

    # Aggiungi la legenda nell'angolo in basso a sinistra con dimensione più piccola
    ax.legend(labels, loc='lower left', fontsize='small')

    # Titolo del grafico
    plt.title(title)

    # Mostra il grafico
    plt.show()

