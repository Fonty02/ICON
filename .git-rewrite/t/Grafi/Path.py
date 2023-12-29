class Path(object):
    """il percorso è singolo nodo oppure nodo -> arco"""

    def __init__(self, initial, arc=None):
        self.initial = initial
        self.arc = arc
        if arc == None:
            self.cost = 0
        else:
            self.cost = arc.cost + initial.cost

    # costruzione "ricorsiva", initial è a sua volta un altro Path

    def end(self):
        if self.arc == None:
            return self.initial
        else:
            return self.arc.to_node

    def nodes(self):
        current = self
        while current.arc is not None:
            yield current.arc.to_node  # mantieni il nodo destinazione
            current = current.initial  # torna al nodo partenza
        yield current.initial  # mantiene partenza
        # alla fine restituisce il percorso "inverso"

    def initial_nodes(self):
        if self.arc is not None:  # se ho almeno 2 nodi
            yield from self.initial.nodes()
        # restituisce il percorso "dritto", tranne il nodo finale

    def __repr__(self):
        if self.arc is None:
            return str(self.initial)  # ritorna il __repr__ del nodo Iniziale
        elif self.arc.action:
            return f"{self.initial}--{self.arc.action}-->{self.arc.to_node}"  # chiamata ricorsiva
        else:
            return f"{self.initial}-->{self.arc.to_node}"  # chiamata ricorsiva
