"""Problema di ricerca di un grafo di cui ho
 - set o lista di nodi
 - set o lista di archi
 - nodo partenza
 - set o lista nodi obiettivo
 - (opzionale) mappa dei valori euristici"""

from SearchProblem import Search_Problem
class SearchProblemGrafoEsplicito(Search_Problem):

    def __init__(self,nodes,arcs,start=None,goals=set(),hmap={}, positions={}):
        self.neighs={}  #dizionario di node->lista archi
        self.nodes=nodes
        for n in self.nodes:
            self.neighs[n]=[]
        self.arcs=arcs
        for arc in arcs:
            self.neighs[arc.from_node].append(arc)
        self.start=start
        self.goals=goals
        self.hmap=hmap
        self.positions=positions

    def start_node(self):
        return self.start

    def is_goal(self,node):
        return node in self.goals  #Restituisce True se il nodo è nel set, False altrimenti

    def neighbors(self,node):
        return self.neighs[node]

    def heuristic(self,n):
        if n in self.hmap:
            return self.hmap[n]
        else:
            return 0

    def __repr__(self):
        res=""
        for arc in self.arcs:
            res+=f"{arc}. "
        return res
