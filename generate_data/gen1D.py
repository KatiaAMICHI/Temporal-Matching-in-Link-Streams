import random
import sys

n = int(sys.argv[1])
T = int(sys.argv[2])
d = int(sys.argv[3])

xposition = [0] * n

for t in range(T):
    print(t, xposition)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(xposition[i] - xposition[j]) <= d:
                print(t, i, j)
    for i in range(n):
        var_to_add = random.randint(1, 80) + i % n * random.randint(1, 33)
        var_to_sud = random.randint(1, 30) + i % n * random.randint(1, 5)

        if random.randint(0, 6) < 1 and xposition[i] > 10:
            xposition[i] -= var_to_sud
        else:
            xposition[i] += var_to_add
