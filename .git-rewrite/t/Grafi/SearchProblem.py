class Search_Problem(object):   #(object) significa che eredita dalla classe object

    #inferisce gli atteibuti

    #Clase astratta -> nota mancanza di __init__

    def start_node(self):  #self significa se stesso, il this in Java
        """restituisce il nodo di partenza"""
        raise NotImplementedError("start_node")   #MetodoAstratto

    def is_goal(self,node):
        """True se nodo è obiettivo, False altrimenti"""
        raise NotImplementedError("is_goal")

    def neighbors(self,node):
        """Restituisce lista degli archi uscenti da node"""
        raise NotImplementedError("neighbors")

    def heuristic(self,n):
        "Restituisce l'euristica di n, 0 se non sovrascrivo"
        return 0
