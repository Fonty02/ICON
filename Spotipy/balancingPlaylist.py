import matplotlib.pyplot as plt
import pandas as pd
from imblearn.over_sampling import SMOTE

from stampe import prGreenMoreString, prRedMoreString, prYellow


def resampleDataset(dataSet, differentialColumn):
    dataSet.drop(dataSet[(dataSet[differentialColumn] != 0) & (
            dataSet[differentialColumn] != 1)].index, inplace=True)

    X = dataSet.drop(columns=[differentialColumn])
    y = dataSet[differentialColumn]

    # Creazione di un oggetto SMOTE
    smote = SMOTE(random_state=42)

    # Applicazione di SMOTE al dataset
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Creazione di un nuovo DataFrame con i dati resampled
    dataSet_resampled = pd.DataFrame(X_resampled, columns=X.columns)
    dataSet_resampled[differentialColumn] = y_resampled

    prYellow("\nOVERSAMPLING EFFETTUATO CON SUCCESSO\n")

    return dataSet_resampled


def visualizeAspectRatioChart(dataSet, differentialColumn):
    # Filtra il dataset per StressRelief e DanceEnergy
    stress_relief_data = dataSet[dataSet[differentialColumn] == 1]
    dance_energy_data = dataSet[dataSet[differentialColumn] == 0]

    # Conta le occorrenze per ciascun mood
    stress_relief_count = len(stress_relief_data)
    dance_energy_count = len(dance_energy_data)

    # Etichette e colori per il grafico
    labels = ['StressRelief', 'DanceEnergy']
    colors = ['lightcoral', 'lightskyblue']

    # Crea il grafico a torta
    plt.pie([stress_relief_count, dance_energy_count], labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

    # Aggiungi la legenda
    plt.legend()

    # Titolo del grafico
    plt.title("Distribuzione di StressRelief e DanceEnergy")

    # Mostra il grafico
    plt.show()


