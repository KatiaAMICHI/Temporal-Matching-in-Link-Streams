import random, numpy, pprint
from functools import reduce


def dpstatic(n, d, xInput):
    x = xInput.copy()
    argsort = list(numpy.argsort(x)) + [n]
    print("argsort : ", argsort)
    M = [0] * (n + 1)
    firstSeen = [True] * n
    # print(">> Proceeding DP for maximum matching:")
    edges = []
    for i in range(1, n):
        if abs(x[argsort[i]] - x[argsort[i - 1]]) <= d:
            M[argsort[i]] = M[argsort[i - 2]] + 1
            if firstSeen[argsort[i]] and firstSeen[argsort[i - 1]]:
                # print("  ...found vertices:", argsort[i], argsort[i - 1], "; x-positions:", x[argsort[i]],
                #    x[argsort[i - 1]])
                edges.append((argsort[i], argsort[i - 1]))
                firstSeen[argsort[i]] = False
                firstSeen[argsort[i - 1]] = False
        else:
            M[argsort[i]] = M[argsort[i - 1]]
    max_matching = reduce(max, M)
    # print("--> Maximum matching size:", reduce(max, M))
    return [max_matching, edges]


def main():
    xMax = 10
    d = 1
    n = 10

    x = list(map(lambda x: random.randint(0, xMax - 1), [0] * n))
    print("x : ", x)

    print(dpstatic(n, d, x))


main()

print("\n********************************\n")
arr = numpy.random.randint(7, size=(3, 3))
print("arr")
print(arr)
print()
argsort = numpy.argsort(arr)
print("argsort")
print(argsort)

print("arr[argsort[0]] : ", argsort[0][0])