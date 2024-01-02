from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

#Funzione che calcola il numero di cluster ottimale per il dataset mediante il metodo del gomito
def regolaGomito(dataSet):
    intertia = []
    #fisso un range di k da 1 a 10
    maxK=10
    for i in range(1, maxK):
        #eseguo il kmeans per ogni k, con 5 inizializzazioni diverse e con inizializzazione random. Prendo la migliore
        kmeans = KMeans(n_clusters=i,n_init=5,init='random')
        kmeans.fit(dataSet)
        intertia.append(kmeans.inertia_)
    #mediante la libreria kneed trovo il k ottimale
    from kneed import KneeLocator
    kl = KneeLocator(range(1, maxK), intertia, curve="convex", direction="decreasing")
    # Visualizza il grafico con la nota per il miglior k
    plt.plot(range(1, maxK), intertia, 'bx-')
    plt.scatter(kl.elbow, intertia[kl.elbow - 1], c='red', label=f'Miglior k: {kl.elbow}')
    plt.xlabel('Numero di Cluster (k)')
    plt.ylabel('Inertia')
    plt.title('Metodo del gomito per trovare il k ottimale')
    plt.legend()
    plt.show()
    return kl.elbow



#Funzione che esege il kmeans sul dataset e restituisce le etichette e i centroidi
def calcolaCluster(dataSet):
    k=regolaGomito(dataSet)
    km = KMeans(n_clusters=k,n_init=10,init='random')
    km = km.fit(dataSet)
    etichette = km.labels_
    centroidi = km.cluster_centers_
    return etichette, centroidi
