import pickle

import matplotlib.pyplot as plt
import networkx as nx
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork


def bNetCreation(dataSet):
    # Crea archi in modo tale che ogni feature dipenda da clusterIndex
    edges = []
    for column in dataSet.columns:
        if column != 'clusterIndex':
            edges.append(('clusterIndex', column))
    model = BayesianNetwork(edges)
    model.fit(dataSet,estimator=MaximumLikelihoodEstimator)

    # Restituisci il modello adattato
    return model


def prediciCluster(bayesianNetwork, example, differentialColumn):
    inference = VariableElimination(bayesianNetwork)
    # Prevedi la probabilità per ogni valore di differentialColumn dato l'esempio
    result = inference.query(variables=[differentialColumn], evidence=example)
    print(result)


def generateRandomExample(bayesianNetwork: BayesianNetwork):
    return bayesianNetwork.simulate(n_samples=1).drop(columns=['clusterIndex'])



