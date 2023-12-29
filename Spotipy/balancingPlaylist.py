import matplotlib.pyplot as plt
import pandas as pd
from imblearn.over_sampling import SMOTE

#Funzione che effettua l'oversampling del dataset
def overSampling(dataSet, differentialColumn):
    dataSet = dataSet.dropna(subset=[differentialColumn])
    X = dataSet.drop(columns=[differentialColumn])
    y = dataSet[differentialColumn]
    smote = SMOTE(random_state=42) #random_state=42 per avere sempre lo stesso risultato
    # Applicazione di SMOTE al dataset
    X_resampled, y_resampled = smote.fit_resample(X, y)
    dataSet_resampled = pd.DataFrame(X_resampled, columns=X.columns)
    dataSet_resampled[differentialColumn] = y_resampled
    print('\033[93m' + "OVERSAMPLING EFFETTUATO CON SUCCESSO" + '\033[0m')
    return dataSet_resampled

#Funzione che visualizza il grafico a torta per la distribuzione dei valori di differentialColumn
def visualizeAspectRatioChart(dataSet, differentialColumn, title):
    # Conta le occorrenze per ciascun valore unico di differentialColumn
    counts = dataSet[differentialColumn].value_counts()

    # Etichette e colori per il grafico
    labels = counts.index.tolist()
    colors = ['lightcoral', 'lightskyblue', 'lightgreen', 'gold', 'mediumorchid', 'lightsteelblue', 'lightpink','lightgrey','lightcyan','lightyellow','lightseagreen','lightsalmon','lightblue','lightgreen','lightcoral','lightpink','lightgrey','lightcyan','lightyellow','lightseagreen','lightsalmon','lightblue','lightgreen','lightcoral','lightpink','lightgrey','lightcyan','lightyellow','lightseagreen','lightsalmon','lightblue','lightgreen','lightcoral','lightpink','lightgrey','lightcyan','lightyellow','lightseagreen','lightsalmon','lightblue','lightgreen','lightcoral','lightpink','lightgrey','lightcyan','lightyellow','lightseagreen','lightsalmon','lightblue','lightgreen','lightcoral','lightpink','lightgrey','lightcyan','lightyellow','lightseagreen','lightsalmon','lightblue','lightgreen','lightcoral','lightpink','lightgrey','lightcyan','lightyellow','lightseagreen','lightsalmon','lightblue','lightgreen','lightcoral','lightpink','lightgrey','lightcyan','lightyellow','lightseagreen','lightsalmon','lightblue']
    #lunga lista di colori per evitare ripetizioni in caso di molti valori unici
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.legend(labels, loc='lower left', fontsize='small')
    plt.title(title)
    plt.show()

