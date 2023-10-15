class Arc(object):

    def __init__(self,from_node,to_node,cost=1,action=None):  #costruttore, costo=1 se non specificato, Azione nulla se non specificata
        self.from_node=from_node
        self.to_node=to_node
        self.cost=cost
        self.action=action
        assert cost>=0, (f"Il costo non puo' essere negativo: {self}, costo={cost}")
        """se il costo è negativo stampa a schermo il messagggio e al posto di self e cost mette i valori (come fosse un .toString())"""
        """la notazione con la f permette di usare le parentesi graffe"""

    def __repr__(self): #Sarebbe il toString
        if self.action:  #diverso da None/False
            return f"{self.from_node}--{self.action}-->{self.to_node}"
        else:
            return f"{self.from_node}-->{self.to_node}"


