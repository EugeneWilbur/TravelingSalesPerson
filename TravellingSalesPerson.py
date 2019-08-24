import math
import random

SIZE = 5
MAX = 100
GENERATIONS = 25
POPSIZE = 250

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
    GOAT = 1000000

    for i in population:
        i.order = shuffle(i.order)
        i.fitness = 0

    population = setFitness(nodes, population)

    for i in range(GENERATIONS):
        print("Generation", i + 1)
        if getBest(nodes, population) < GOAT:
            GOAT = getBest(nodes, population)
        print("Best: ", GOAT)
        population = makeNextGen(population, nodes)

    print(GOAT)


def setFitness(nodes, population):
    for i in population:
        current = calcDistance(nodes, i.order)
        i.fitness = (1 / (current + 1)) * 1000
    population = fixFitness(population)
    return population


def fixFitness(population):
    fitSum = 0
    for i in population:
        fitSum += i.fitness
    for i in population:
        i.fitness = i.fitness / fitSum
    return population


def displayPop(population):
    for i in population:
        print(i.fitness)

def getBest(nodes, population):
    for i in range(POPSIZE):
        current = calcDistance(nodes, population[i].order)
        if i == 0:
            best = current
        if current < best:
            best = current
        population[i].fitness = 1/(current+1)
    return best


def pickSeed(population):
    index = 0
    r = random.random()

    while r > 0:
        r = r - population[index].fitness
        index += 1
        if index >= len(population):
            index = 1
    index -= 1
    return population[index]


def makeNextGen(population, nodes):
    nextGen = [Pop(0) for i in range(POPSIZE)]
    for i in range(POPSIZE):
        nextGen[i] = pickSeed(population)
        nextGen[i].order = swap(nextGen[i].order)
    nextGen = setFitness(nodes, nextGen)
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
