import math
import random

SIZE = 5
MAX = 100
testSize = 100000

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def main():
    totalD = 0  # haha
    nodes = []
    order = [i for i in range(52)]
    fileName = "berlin52.tsp"
    line = ""

    while True:
        # fileName = input("File name: ")
        try:
            file = open(fileName)
            break
        except FileNotFoundError:
            print("Error: Failed to open file. Try again.")

    while 'EOF' not in line:
        line = file.readline()
        if any(c.isalpha() for c in line):
            pass
        else:
            currentLine = line.split()
            nodes.append(Node(float(currentLine[1]), float(currentLine[2])))

    best = 10000000000
    for i in range(testSize):
        order = shuffle(order)
        print(order)
        current = calcDistance(nodes, order)
        if current < best:
            best = current
        print(current)
        i += 1

    print(best)

def shuffle(order):
    random.shuffle(order)
    return order

def calcDistance(nodes, order):
    total = 0
    for i in range(len(order) - 1):
        currentDistance = math.sqrt((nodes[order[i]].x - nodes[order[i+1]].x) ** 2 + (nodes[order[i]].y - nodes[order[i+1]].y) ** 2)
        total += currentDistance
    return total



if __name__ == "__main__":
    main()
