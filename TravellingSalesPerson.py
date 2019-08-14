import math

SIZE = 5
MAX = 100

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def main():
    totalD = 0  # haha
    nodes = []
    order = [i for i in range(280)]
    fileName = "a280.tsp"
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
            nodes.append(Node(int(currentLine[1]), int(currentLine[2])))

    for i in nodes:
        print(i.x, i.y)

    best = currentTotal(nodes)
    print(currentTotal(nodes))



def currentTotal(nodes):
    total = 0
    for i in range(len(nodes) - 1):
        currentDistance = calcDist(nodes[i], nodes[i+1])
        total += currentDistance
    return total


def calcDist(curNode, nextNode):
    return math.sqrt((curNode.x - nextNode.x) ** 2 + (curNode.y - nextNode.y) ** 2)


if __name__ == "__main__":
    main()
