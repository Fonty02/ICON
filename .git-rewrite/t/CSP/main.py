from CSPProblem import CSP
from variable import Variable
from Constraint import Constraint
from operator import lt,ne,eq,gt

def ne_(val):
    def nev(x):
        return val != x
    nev.__name__ = f"{val} != " # name of the function
    return nev

def is_(val):
    def isv(x):
        return val == x
    isv.__name__ = f"{val} == "
    return isv




A = Variable('A', {1,2,3,4}, position=(0.2,0.9))
B = Variable('B', {1,2,3,4}, position=(0.8,0.9))
C = Variable('C', {1,2,3,4}, position=(1,0.4))
C0 = Constraint([A,B], lt, "A < B", position=(0.4,0.3))
C1 = Constraint([B], ne_(2), "B != 2", position=(1,0.9))
C2 = Constraint([B,C], lt, "B < C", position=(0.6,0.1))
csp1 = CSP("csp1", {A, B, C},[C0, C1, C2])
csp1s = CSP("csp1s", {A, B, C},[C0, C2])

def adjacent(x,y):
    return abs(x-y) == 1
