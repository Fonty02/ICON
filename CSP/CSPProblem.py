import matplotlib.pyplot as plt


class CSP(object):

    def __init__(self, title, variables, constraints):
        self.title = title
        self.variables = variables
        self.constraints = constraints
        self.var_to_const = {var: set() for var in self.variables}
        for con in constraints:
            for var in con.scope:
                self.var_to_const[var].add(con)

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return f"CSP({self.title}, {self.variables}, {([str(c) for c in self.constraints])})"

    def consistent(self, assignment):

        return all(con.holds(assignment)
                   for con in self.constraints
                   if con.can_evaluate(assignment))

    def show(self):

        plt.ion()  # interactive
        ax = plt.figure().gca()
        ax.set_axis_off()
        plt.title(self.title)
        var_bbox = dict(boxstyle="round4,pad=1.0,rounding_size=0.5")
        con_bbox = dict(boxstyle="square,pad=1.0", color="green")
        for var in self.variables:
            if var.position is None:
                var.position = (random.random(), random.random())
        for con in self.constraints:
            if con.position is None:
                con.position = tuple(sum(var.position[i] for var in
                                         con.scope) / len(con.scope)
                                     for i in range(2))


            bbox = dict(boxstyle="square,pad=1.0", color="green")
            for var in con.scope:
                ax.annotate(con.string, var.position, xytext=con.position,arrowprops={'arrowstyle': '-'}, bbox=con_bbox,ha='center')
        for var in self.variables:
            x, y = var.position
            plt.text(x, y, var.name, bbox=var_bbox, ha='center')
