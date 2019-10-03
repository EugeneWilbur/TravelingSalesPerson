import sys
import sqlite3
from solver import *


DBNAME = "TSPdb.db"


def main(arg1, arg2, arg3):
    connection = sqlite3.connect(DBNAME)
    cursor = connection.cursor()

    try:
        name = arg1
        task = arg2
    except IndexError:
        print("Error: Missing command line argument(s). Try again")
        exit()

    try:
        extra = arg3
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
            returning = []
            if i == 0:
                pass
                #print("Distance: ")
                #print(result[i])
            else:
               # print("Order: ")
                #print(result[i])
                returning.append(result[i])
        return returning
    elif task == "SHOW":
        format_str = "select x,y from data WHERE problem_name = \"{n}\""
        sql_command = format_str.format(n=name)
        cursor.execute(sql_command)
        result = cursor.fetchall()
        if result == []:
            print("Error: Tried to solve problem but no problem existed. Try again.")
            exit()
        return result

    connection.close()


if __name__ == "__main__":
    main()
