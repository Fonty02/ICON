import matplotlib.pyplot as plt
import pandas as pd
from sklearn.utils import resample

from stampe import prGreenMoreString, prRedMoreString, prYellow


def resampleDataset(dataSet, differentialColumn):
    dataSet.drop(dataSet[(dataSet[differentialColumn] != 0) & (
        dataSet[differentialColumn] != 1)].index, inplace=True)
    df_majority = dataSet[dataSet[differentialColumn] == 0]
    df_minority = dataSet[dataSet[differentialColumn] == 1]

    df_minority_upsampled = resample(
        df_minority, replace=True, n_samples=len(df_majority), random_state=42)
    dataSet = pd.concat([df_minority_upsampled, df_majority])

    prYellow("\nValue after Oversampling:")
    prGreenMoreString('Positive mood: ', dataSet.playlistName.value_counts()[0],
                      '(% {:.2f})'.format(dataSet.playlistName.value_counts()[0] / dataSet.playlistName.count() * 100))
    prRedMoreString('Neegative mood: ', dataSet.playlistName.value_counts()[1],
                    '(% {:.2f})'.format(dataSet.playlistName.value_counts()[1] / dataSet.playlistName.count() * 100))

    return dataSet


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


