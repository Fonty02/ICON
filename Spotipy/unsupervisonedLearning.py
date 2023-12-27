from matplotlib import pyplot as plt
from sklearn.cluster import KMeans



def regolaGomito(dataSet):
    intertia = []
    maxK=10
    for i in range(1, maxK):
        kmeans = KMeans(n_clusters=i,n_init=5,init='random')
        kmeans.fit(dataSet)
        intertia.append(kmeans.inertia_)
    from kneed import KneeLocator
    kl = KneeLocator(range(1, maxK), intertia, curve="convex", direction="decreasing")

    # Visualizza il grafico con la nota per il miglior k
    plt.plot(range(1, maxK), intertia, 'bx-')
    plt.scatter(kl.elbow, intertia[kl.elbow - 1], c='red', label=f'Miglior k: {kl.elbow}')
    plt.xlabel('Numero di Cluster (k)')
    plt.ylabel('Intertia')
    plt.title('Metodo del gomito per trovare il k ottimale')
    plt.legend()
    plt.show()
    return kl.elbow



#restituisci per ogni elemento del dataset il cluster di appartenenza e le labels dei centroidi
def calcolaCluster(dataSet):
    k=regolaGomito(dataSet)
    km = KMeans(n_clusters=k,n_init=10,init='random')
    km = km.fit(dataSet)
    etichette = km.labels_
    centroidi = km.cluster_centers_
    return etichette, centroidi
