from FrontierPQ import FrontieraPriorita
from SearchProblem import Search_Problem
from Path import Path
class AStar():

    def __init__(self,problem: Search_Problem):
        self.problem=problem
        self.initializeFrontier()
        self.add_to_frontier(Path(problem.start_node()))

    def initializeFrontier(self):
        self.frontier=FrontieraPriorita()

    def add_to_frontier(self,path):
        self.frontier.add(path,path.cost+self.problem.heuristic(path.end()))

    def empty_frontier(self):
        return self.frontier.empty()

    def search(self):
        while not self.empty_frontier():
            path=self.frontier.pop()
            if (self.problem.is_goal(path.end())):
                self.solution=path
                print(f"COSTO = {path.cost}",end="\n")
                return path
            else:
                neighs=self.problem.neighbors(path.end())
                for arc in neighs:
                    self.add_to_frontier(Path(path,arc))














