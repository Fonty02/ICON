from display import Displayable, visualize
from Path import Path
from SearchProblem import Search_Problem

class Searcher(Displayable):


    def __init__(self,problem:Search_Problem):
        self.problem=problem
        self.initialize_frontier()
        self.num_expanded=0
        self.add_to_frontier(Path(problem.start_node()))
        super().__init__()

    def initialize_frontier(self):
        self.frontier=[]

    def empty_frontier(self):
        return len(self.frontier)==0

    def add_to_frontier(self,path):
        self.frontier.append(path)

    @visualize
    def search(self):
        """ALGORITMO DI RICERCA GENERICO"""
        while not self.empty_frontier():
            path=self.frontier.pop()
            self.display(2,"Expanding",path,"(cost:",path.cost,")")
            self.num_expanded+=1
            if (self.problem.is_goal(path.end())):
                self.display(1,self.num_expanded,"percorso trovato",len(self.frontier),"percorsi rimasti in frontiera")
                self.solution=path
                return path
            else:
                neighs=self.problem.neighbors(path.end())
                self.display(3,"I vicini sono", neighs)
                for arc in neighs:
                    self.add_to_frontier(Path(path,arc))
                self.display(3,"Frontier",self.frontier)
        self.display(1,"Non ci sono soluzioni. Percorsi visitati:", self.num_expanded)

    def __dfs(self,path):
        if self.problem.is_goal(path.end()):
            self.solution=path
            return path
        self.num_expanded+=1
        neighs=self.problem.neighbors(path.end())
        if neighs is []: return None
        for arc in neighs:
            possibleSolution=self.__dfs(Path(path,arc))
            if possibleSolution is not None: return possibleSolution
        return None

    def dfs(self):
        self.solution=None
        path=self.frontier.pop()
        self.__dfs(path)
        if not self.solution: return "NON CI SONO SOLUZIONI"
        else: return self.solution



