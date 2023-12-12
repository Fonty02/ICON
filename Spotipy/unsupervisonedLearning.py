from matplotlib import pyplot as plt
from sklearn.cluster import KMeans



def regolaGomito(dataSet):
    errori_predizione = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i,n_init=10)
        kmeans.fit(dataSet)
        errori_predizione.append(kmeans.inertia_)

    # Trova il gomito considerando la massima riduzione dell'errore tra k e k-1
    best_k = 0
    max_reduction = 0
    for i in range(1, len(errori_predizione) - 1):  # Modificato il range per evitare l'errore di chiave
        reduction = errori_predizione[i - 1] - errori_predizione[i]
        if reduction > max_reduction:
            max_reduction = reduction
            best_k = i + 1

    # Visualizza il grafico con la nota per il miglior k
    plt.plot(range(1, 11), errori_predizione, 'bx-')
    plt.scatter(best_k, errori_predizione[best_k - 1], c='red', label=f'Miglior k: {best_k}')
    plt.xlabel('Numero di Cluster (k)')
    plt.ylabel('Somma degli errori quadrati')
    plt.title('Método del gomito per trovare il k ottimale')
    plt.legend()
    plt.show()
    return best_k



#restituisci per ogni elemento del dataset il cluster di appartenenza e le labels dei centroidi
def calcolaCluster(dataSet):
    k=regolaGomito(dataSet)
    km = KMeans(n_clusters=k,n_init=10)
    km = km.fit(dataSet)
    etichette = km.labels_
    centroidi = km.cluster_centers_
    return etichette, centroidi
