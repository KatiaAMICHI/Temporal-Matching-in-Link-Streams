import numpy
import os
import subprocess
import shlex
from functools import reduce

"""
Methos to generate data 
"""


def generateXD(script, dir):
    nb_tests = 1500
    subprocess.call(shlex.split('./gen_shell.sh ' + str(nb_tests) + ' ' + script + ' ' + dir))


def dpstatic(n, d, t, xInput):
    x = xInput.copy()
    argsort = list(numpy.argsort(x)) + [n]
    M = [0] * (n + 1)
    firstSeen = [True] * n
    edges = []

    for i in range(1, n):
        if abs(x[argsort[i]] - x[argsort[i - 1]]) <= d:
            M[argsort[i]] = M[argsort[i - 2]] + 1
            if firstSeen[argsort[i]] and firstSeen[argsort[i - 1]]:
                edges.append((t, argsort[i], argsort[i - 1]))
                firstSeen[argsort[i]] = False
                firstSeen[argsort[i - 1]] = False
        else:
            M[argsort[i]] = M[argsort[i - 1]]

    max_matching = reduce(max, M)

    return max_matching, edges


def genGammaEdges(path):
    result = []
    for folder in os.listdir(path):
        for file in os.listdir(path + folder):
            path_file = path + folder + "/"
            file_output = path_file + file.replace(".position", ".nb_matching")
            if file.endswith('.position'):
                with open(path_file + file) as f:
                    n, t_max, d = list(map(int, f.readline().split()))
                    x = [[]] * t_max
                    with open(file_output, "+w") as f_outPut:
                        f_outPut.write(str(n) + " " + str(t_max) + " " + str(d) + "\n")
                        for line in f:
                            t, pos = line.split("[")
                            t = int(t)
                            x[t] = list(map(int, pos.replace("]", "").replace(",", " ").split()))
                            max_matching, edges = dpstatic(n, d, t, x[t])
                            result.append((max_matching, edges))  # ajout du tuple (nb_matching, [les matching])
                            f_outPut.write(str(max_matching) + " " + str(edges) + "\n")

    return result


def main():
    path = r"../res/gen_B2/"
    script = 'gen2D.py'
    dir = 'gen_B2'

    generateXD(script, dir)
    # genGammaEdges(path)


main()
