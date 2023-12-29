import heapq

class FrontieraPriorita(object):
    """
    * costo (or costo+euristica)
    * indice unico per ogni elemento
    * percorso
    """

    def __init__(self):
        self.frontier_index=0
        self.frontierpq=[]

    def empty(self):
        return self.frontierpq==[]

    def add(self,path,value):
        self.frontier_index+=1
        heapq.heappush(self.frontierpq,(value, -self.frontier_index,path))

    def pop(self):
        (_,_,path)=heapq.heappop(self.frontierpq)
        return path

    def count(self,val):
        """ritorna numero elementi con valore=val"""
        return sum(1 for e in self.frontierpq if e[0]==val)

    def __repr__(self):
        return str([(n,c,str(p)) for (n,c,p) in self.frontierpq])

    def __len__(self):
        return len(self.frontierpq)

    def __iter__(self):
        for(_,_,path) in self.frontierpq:
            yield path
            