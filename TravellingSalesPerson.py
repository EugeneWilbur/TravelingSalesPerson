import math
import random

SIZE = 5
MAX = 100
testSize = 100
POPSIZE = 300

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Pop:
    def __init__(self, fitness):
        self.order = [i for i in range(52)]
        self.fitness = fitness


def main():
    # Population of random orders created
    population = [Pop(0) for i in range(POPSIZE)]

    # file i/o handled.
    fileName = "berlin52.tsp"
    nodes = nodeInput(fileName)

    for i in population:
        i.order = shuffle(i.order)
        i.fitness = 0

    getBest(nodes, population)

    #population = fixFitness(population)

    for i in range(testSize):
        fittestOrder = Pop(0)
        for i in population:
            if i.fitness > fittestOrder.fitness:
                fittestOrder = i
        population = makeNextGen(fittestOrder, nodes)

    for i in population:
        print(i.fitness)

    print(getBest(nodes, population))


def pickSeed(popultaion):
    index = 0
    r = random.randint(0, 1)

    while(r > 0):
        r = r - popultaion[index].fitness
        index += 1
    index -= 1
    return popultaion[index]


def fixFitness(population):
    sum = 0
    for i in range(len(population)):
        sum += population[i].fitness

    for i in range(len(population)):
        population[i].fitness = population[i].fitness / sum
    return population


def getBest(nodes, population):
    for i in range(POPSIZE):
        current = calcDistance(nodes, population[i].order)
        if i == 0:
            best = current
        if current < best:
            best = current
        population[i].fitness = 1/(current+1)
    return best


def makeNextGen(fittestLast, nodes):
    nextGen = [Pop(0) for i in range(POPSIZE)]
    for i in range(POPSIZE):
        nextGen[i].order = fittestLast.order
        fittestLast.setFitness(fittestLast.order, nodes)
        nextGen[i].fitness = fittestLast.fitness
        fittestLast.order = swap(fittestLast.order)
    return nextGen

def swap(order):
    a = random.randint(0, (len(order) - 2))
    b = a+1
    temp = order[a]
    order[a] = order[b]
    order[b] = temp
    return order


def nodeInput(fileName):
    nodes = []
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
    return nodes


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
