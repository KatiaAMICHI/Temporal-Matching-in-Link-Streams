import random
import sys

n = int(sys.argv[1])
T = int(sys.argv[2])
d = int(sys.argv[3])

position = [0] * n

for t in range(T):
    print(t, position)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(position[i] - position[j]) <= d:
                print(t, i, j)
    for i in range(n):
        if random.randint(0, 9) < 1 and position[i] > 0:
            position[i] -= 1
        else:
            position[i] += random.randint(0, 4)
