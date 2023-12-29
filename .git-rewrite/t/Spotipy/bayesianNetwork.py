import pickle


import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
from pgmpy.models import BayesianNetwork

def visualizeBayesianNetwork(bayesianNetwork: BayesianNetwork):
    G = nx.MultiDiGraph(bayesianNetwork.edges())
    pos = nx.spring_layout(G, iterations=100, k=2,
                           threshold=5, pos=nx.spiral_layout(G))
    nx.draw_networkx_nodes(G, pos, node_size=150, node_color="#ff574c")
    nx.draw_networkx_labels(
        G,
        pos,
        font_size=10,
        font_weight="bold",
        clip_on=True,
        horizontalalignment="center",
        verticalalignment="bottom",
    )
    nx.draw_networkx_edges(
        G,
        pos,
        arrows=True,
        arrowsize=7,
        arrowstyle="->",
        edge_color="purple",
        connectionstyle="angle3,angleA=90,angleB=0",
        min_source_margin=1.2,
        min_target_margin=1.5,
        edge_vmin=2,
        edge_vmax=2,
    )

    plt.title("BAYESIAN NETWORK GRAPH")
    plt.show()
    plt.clf()

def bNetCreation(dataSet):
    # Crea archi in modo tale che ogni feature dipenda da clusterIndex
    edges = []
    for column in dataSet.columns:
        if column != 'clusterIndex':
            edges.append(('clusterIndex', column))
    '''hc_k2=HillClimbSearch(dataSet)
    k2_model=hc_k2.estimate(max_iter=4)'''
    edges.append(('tempo','danceability'))
    edges.append(('energy','danceability'))
    edges.append(('loudness','energy'))
    edges.append(('tempo','energy'))
    edges.append(('loudness','speechiness'))
    edges.append(('liveness','acousticness'))
    edges.append(('speechiness','liveness'))
    edges.append(('loudness','liveness'))
    edges.append(('danceability','valence'))

    model = BayesianNetwork(edges)
    model.fit(dataSet,estimator=MaximumLikelihoodEstimator,n_jobs=-1)
    with open('modello.pkl', 'wb') as output:
        pickle.dump(model, output)
    visualizeBayesianNetwork(model)
    return model



def readBayesianNetwork():
    with open('modello.pkl', 'rb') as input:
        model = pickle.load(input)
    visualizeBayesianNetwork(model)
    return model

def prediciCluster(bayesianNetwork: BayesianNetwork, example, differentialColumn):
    inference = VariableElimination(bayesianNetwork)
    result = inference.query(variables=[differentialColumn], evidence=example)
    print(result)


def generateRandomExample(bayesianNetwork: BayesianNetwork):
    return bayesianNetwork.simulate(n_samples=1).drop(columns=['clusterIndex'])


