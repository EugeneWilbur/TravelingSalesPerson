import math
import random
import time
import sys

#number of orders in each population
POPSIZE = 200

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Pop:
    def __init__(self, fitness, order):
        self.order = order
        self.fitness = fitness


def main():

    fileName = sys.argv[1]
    timer = int(sys.argv[2])
    outFile = sys.argv[3]
    nodes = nodeInput(fileName)

    # Population of random orders created
    order = [i for i in range(len(nodes))]
    population = [Pop(0, order) for i in range(POPSIZE)]

    GOAT = Pop(0, order)

    for i in population:
        i.order = shuffle(i.order)
        i.fitness = 0

    population = setFitness(nodes, population) ##starting population

    start = time.time()
    now = 0
    while now < timer:
        now = (time.time() - start)
        current = getBest(population)
        if current.fitness > GOAT.fitness:
            GOAT.order = current.order.copy()
            GOAT.fitness = current.fitness
        population = makeNextGen(population, nodes)

    output(outFile, GOAT, nodes)
    print(calcDistance(nodes, GOAT.order))


def getBest(population):
    index = 0
    for i in range(POPSIZE):
        current = population[i].fitness
        if i == 0:
            best = current
        if current > best:
            best = current
            index = i

    return population[index]


def makeNextGen(population, nodes):
    nextGen = [Pop(0, population[i].order) for i in range(POPSIZE)]
    for i in nextGen:
        i.order = swap(pickSeed(population).order).copy()
    nextGen = setFitness(nodes, nextGen)
    return nextGen


#the more fitness an object has, the more likely it will be picked in the following generation
def pickSeed(population):
    index = 0
    num = random.random()

    while num > 0:
        num = num - population[index].fitness
        index += 1
        if index >= len(population):
            index = 1
    index -= 1

    return population[index]


def setFitness(nodes, population):
    fitSum = 0

    for i in population:
        current = calcDistance(nodes, i.order)
        i.fitness = 1 / current #makes it so that a smaller distance means higher fitness
        fitSum += i.fitness

    #normalises the fitness across all the objects
    for i in population:
        i.fitness = i.fitness / fitSum

    return population


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
    file.close()

    return nodes


def shuffle(order):
    random.shuffle(order)
    return order


def calcDistance(nodes, order):
    total = 0

    for i in range(len(order)):
        j = i + 1
        if j >= len(order):
            j = 0
        currentDistance = math.hypot((nodes[order[i]].x - nodes[order[j]].x), (nodes[order[i]].y - nodes[order[j]].y))
        total += currentDistance

    return total


def output(outFile, GOAT, nodes):

    file = open(outFile, "w")
    ans = round(calcDistance(nodes, GOAT.order), 2)
    file.write("Shortest Length Found in time limit: ")
    file.write(str(ans))
    for i in GOAT.order:
        file.write("\n")
        file.write(str(i))

    file.close()


if __name__ == "__main__":
    main()
