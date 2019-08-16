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
        var_to_add = random.randint(1, 20) + i % n * random.randint(1, 15)
        var_to_sud = random.randint(1, 20) + i % n * random.randint(1, 15)

        if random.randint(0, 4) < 1 and xposition[i] > 10:
            xposition[i] -= random.randint(1, 30)
        else:
            xposition[i] += random.randint(0, 80)

        # changement du 14/08 (après génération des tests dans gen_B1)
        if t % random.randint(1, t+1) == 0:
            xposition[i] = 0
