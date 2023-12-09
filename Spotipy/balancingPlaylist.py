import matplotlib.pyplot as plt

from stampe import prGreenMoreString, prRedMoreString, prYellow

from imblearn.over_sampling import SMOTE
import pandas as pd


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

    prYellow("\nValue after Oversampling:")
    prGreenMoreString('Positive mood: ', dataSet_resampled[differentialColumn].value_counts()[0],
                      '(% {:.2f})'.format(dataSet_resampled[differentialColumn].value_counts()[0] / dataSet_resampled[
                          differentialColumn].count() * 100))
    prRedMoreString('Negative mood: ', dataSet_resampled[differentialColumn].value_counts()[1],
                    '(% {:.2f})'.format(dataSet_resampled[differentialColumn].value_counts()[1] / dataSet_resampled[
                        differentialColumn].count() * 100))

    return dataSet_resampled


def visualizeAspectRatioChart(dataSet, differentialColumn):
    #crea e mostra un grafo a torta con una legenda che mostri il mood Negative se dataset[differentialColumn] == 1 altrimenti Positive
    labels = 'Positive', 'Negative'
    sizes = [dataSet[differentialColumn].value_counts()[0],
             dataSet[differentialColumn].value_counts()[1]]
    explode = (0, 0.1)  # explode 1st slice
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels,
            autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend()
    plt.show()


