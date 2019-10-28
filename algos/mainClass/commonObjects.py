class GammaMach:
    def __init__(self, t, u, v):
        self.t = t
        self.u = u
        self.v = v
        self.neighbours = set()
        self.nb_neighbours = 0

    def __repr__(self):
        return "GammaMach(t:" + str(self.t) + ", u:" + str(self.u) + ",v: " + str(self.v) + ", nb_neighbours :" + str(
            self.nb_neighbours) + ")"


class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v
        self.neighbours = []
        self.nb_neighbours = 0

    def __repr__(self):
        return "Edge(u:" + self.u + ", v:" + self.v + ", nb_neighbours:" + str(self.nb_neighbours) + ")"


def SommetsVivant(file):
    sommetsVivant = set()

    with open(file) as f:
        for line in f:
            line_split = line.split()
            t = int(line_split[0])
            u = line_split[1]
            v = line_split[2]

            sommetsVivant.add((t, u))
            sommetsVivant.add((t, v))

    return len(sommetsVivant)
