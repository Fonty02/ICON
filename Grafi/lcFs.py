from display import Displayable, visualize
from Path import Path
from SearchProblem import Search_Problem
from FrontierPQ import FrontieraPriorita
class lcfs(Displayable):


    def __init__(self,problem:Search_Problem):
        self.problem=problem
        self.initialize_frontier()
        self.num_expanded=0
        self.add_to_frontier(Path(problem.start_node()))
        super().__init__()

    def initialize_frontier(self):
        self.frontier=FrontieraPriorita()

    def empty_frontier(self):
        return len(self.frontier)==0

    def add_to_frontier(self,path):
        self.frontier.add(path,path.cost)

    @visualize
    def search(self):
        """ALGORITMO DI RICERCA GENERICO"""
        while not self.empty_frontier():
            path=self.frontier.pop()
            self.display(2,"Expanding",path,"(cost:",path.cost,")")
            self.num_expanded+=1
            if (self.problem.is_goal(path.end())):
                self.display(1,self.num_expanded,"percorso trovato con costo",path.cost,len(self.frontier),"percorsi rimasti in frontiera")
                self.solution=path
                return path
            else:
                neighs=self.problem.neighbors(path.end())
                self.display(3,"I vicini sono", neighs)
                for arc in neighs:
                    self.add_to_frontier(Path(path,arc))
                self.display(3,"Frontier",self.frontier)
        self.display(1,"Non ci sono soluzioni. Percorsi visitati:", self.num_expanded)



