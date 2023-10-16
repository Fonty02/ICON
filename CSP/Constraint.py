from variable import Variable
class Constraint(object):
 def __init__(self, scope, condition, string=None, position=None):
    self.scope = scope
    self.condition = condition
    if string is None:
        self.string = f"{self.condition.__name__}({self.scope})"
    else:
        self.string = string
    self.position = position

    def __repr__(self):
        return self.string

    def can_evaluate(self, assignment):
        return all(v in assignment for v in self.scope)

    def holds(self, assignment):
        return self.condition(*tuple(assignment[v] for v in self.scope))