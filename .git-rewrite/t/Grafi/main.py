from SearchProblemGrafoEsplicito import *
from Arc import Arc
from AStar import AStar
from lcFs import lcfs

problem1=SearchProblemGrafoEsplicito(
    {'A','B','C','D','G'},
    [Arc('A','B',3),Arc('A','C',1),Arc('B','D',1),
     Arc('B','G',3),Arc('C','B',1),Arc('C','D',3),
     Arc('D','G',1)],start='A',goals={'G'},positions={'A':(0,2),'B':(1,1),'C':(0,1),'D':(1,0),'G':(2,0)})

ricerca=AStar(problem1)
print(ricerca.search())

