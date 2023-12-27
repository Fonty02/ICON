import pickle

import matplotlib.pyplot as plt
#import networkx as nx
from pgmpy.estimators import MaximumLikelihoodEstimator, HillClimbSearch
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork


def bNetCreation(dataSet):
    # Crea archi in modo tale che ogni feature dipenda da clusterIndex
    edges = []
    for column in dataSet.columns:
        if column != 'clusterIndex':
            edges.append(('clusterIndex', column))
    '''hc_k2=HillClimbSearch(dataSet)
    k2_model=hc_k2.estimate(max_iter=4,fixed_edges=edges)'''
    edges.append(('tempo','danceability'))
    edges.append(('energy','danceability'))
    edges.append(('energy','loudness'))
    edges.append(('instrumentalness','speechiness'))
    edges.append(('liveness','acousticness'))
    edges.append(('danceability','valence'))
    model = BayesianNetwork(edges)
    print("MODELLO CREATO")
    model.fit(dataSet,estimator=MaximumLikelihoodEstimator)
    print("MODELLO ADATTATO")
    # Restituisci il modello adattato
    return model

def readBayesianNetwork():
    with open('modello.pkl', 'rb') as input:
        model = pickle.load(input)
    return model

def prediciCluster(bayesianNetwork, example, differentialColumn):
    inference = VariableElimination(bayesianNetwork)
    # Prevedi la probabilità per ogni valore di differentialColumn dato l'esempio
    result = inference.query(variables=[differentialColumn], evidence=example)
    print(result)


def generateRandomExample(bayesianNetwork: BayesianNetwork):
    return bayesianNetwork.simulate(n_samples=1).drop(columns=['clusterIndex'])



