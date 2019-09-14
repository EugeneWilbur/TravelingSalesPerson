import math
import random
import time
import sys
import sqlite3

DBNAME = "TSPdb.db"
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
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()

    try:
        name = sys.argv[1]
        task = sys.argv[2]
    except IndexError:
        print("Error: Missing command line argument(s). Try again")
        exit()

    try:
        extra = sys.argv[3]
    except IndexError:
        if task != "FETCH":
            print("Error: Missing command line argument(s). Try again")
            exit()


    try:
        cursor.execute("select * from problem_sets;")
    except sqlite3.OperationalError:
        print("Error: Could not connect to database. Try again.")
        exit()

    if task == "ADD":
        nodes, size = nodeInput(extra)
        #insert into problem_sets table
        format_str = """INSERT INTO problem_sets(name, size) VALUES ("{curName}", "{curSize}");"""
        sql_command = format_str.format(curName=name, curSize=size)
        cursor.execute(sql_command)

        #insert into data table
        for i in nodes:
            format_str = """INSERT INTO data(x, y, problem_name) VALUES ("{x}", "{y}", "{curName}");"""
            sql_command = format_str.format(x=i.x, y=i.y, curName=name)
            cursor.execute(sql_command)
        connection.commit()
    elif task == "SOLVE":
        nodes = []
        format_str = "select x,y from data WHERE problem_name = \"{n}\""
        sql_command = format_str.format(n=name)
        cursor.execute(sql_command)
        result = cursor.fetchall()
        if result == []:
            print("Error: Tried to solve problem but no problem existed. Try again.")
            exit()
        for r in result:
            for i in range(len(r) - 1):
                nodes.append(Node(float(r[1]), float(r[i+1])))
        extra = int(extra)
        GOAT, dist = solve(nodes, extra)
        GOAT = str(GOAT)

        #check if we have already solved this, if we have, store the better solution.
        format_str = """select distance from solutions where problem_name = \"{n}\""""
        sql_command = format_str.format(n=name)
        cursor.execute(sql_command)
        result = cursor.fetchone()
        strResult = str(result)
        if strResult != "None":
            for i in result:
                result = i
            if result < dist:
                print("Previous solution was more efficient. Keeping previous solution")
                return
            else:
                print("New solution is more efficient, Replacing the previous solution.")
                format_str = """delete from solutions where problem_name = \"{n}\""""
                sql_command = format_str.format(n=name)
                cursor.execute(sql_command)

        format_str = """INSERT INTO solutions(shortest_order, distance, problem_name) VALUES ("{s}", "{d}", "{n}");"""
        sql_command = format_str.format(s=GOAT, d=dist, n=name)
        cursor.execute(sql_command)
        connection.commit()
    elif task == "FETCH":
        format_str = "select distance, shortest_order from solutions WHERE problem_name = \"{n}\""
        sql_command = format_str.format(n=name)
        cursor.execute(sql_command)
        result = cursor.fetchone()
        strResult = str(result)
        if strResult == "None":
            print("Error: Tried to fetch solution that does not exist. Try again.")
            exit()
        for i in range(len(result)):
            if i == 0:
                print("Distance: ")
                print(result[i])
            else:
                print("Order: ")
                print(result[i])

    connection.close()


def solve(nodes, timer):

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
    finalDist = calcDistance(nodes, GOAT.order)

    return GOAT.order, finalDist


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
    size = 0

    while(True):
        try:
            file = open(fileName)
            break
        except FileNotFoundError:
            print("Error: Failed to open file. Try again.")
            exit()


    while 'EOF' not in line:
        line = file.readline()
        if any(c.isalpha() for c in line):
            pass
        else:
            currentLine = line.split()
            nodes.append(Node(float(currentLine[1]), float(currentLine[2])))
            size += 1
    file.close()

    return nodes, size


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
