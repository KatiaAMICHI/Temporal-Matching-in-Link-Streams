
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