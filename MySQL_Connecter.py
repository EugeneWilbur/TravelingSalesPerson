from solver import *
import mysql.connector
from mysql.connector import Error
from datetime import date



#DBNAME = 's5130828db'
DBNAME = '1810ICTdb'


def main(arg1, arg2, arg3):
    GOAT = ""
    nodes = []
    dist = 0

    try:
        connection = mysql.connector.connect(host='mysql.ict.griffith.edu.au',
                                         user='s5130828',
                                         password='aSPYbvce',
                                            database=DBNAME)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor = connection.cursor(buffered=True)
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
                cursor.execute("select * from Problem;")
            except Error:
                print("Error: Could not connect to database. Try again.")
                exit()

            if task == "ADD":
                nodes, size = nodeInput(extra)
                #insert into problem_sets table
                format_str = """INSERT INTO Problem(name, size, comment) VALUES ("{curName}", "{curSize}", " ");"""
                sql_command = format_str.format(curName=name, curSize=size)
                cursor.execute(sql_command)

                #insert into data table
                icounter = 0
                for i in nodes:
                    format_str = """INSERT INTO Cities(Name, ID, x, y) VALUES ( "{curName}", "{ID}", "{x}", "{y}");"""
                    sql_command = format_str.format(x=i.x, y=i.y, curName=name, ID=icounter)
                    cursor.execute(sql_command)
                    icounter += 1
                connection.commit()
            elif task == "LoadForSolve":
                format_str = "select x,y from Cities WHERE name = \"{n}\""
                sql_command = format_str.format(n=name)
                cursor.execute(sql_command)
                result = cursor.fetchall()
                if result == []:
                    print("Error: Tried to solve problem but no problem existed. Try again.")
                    exit()
                for r in result:
                    for i in range(len(r) - 1):
                        nodes.append(Node(float(r[1]), float(r[i+1])))
                return nodes
            elif task == "SaveNewSolve":
                cursor.execute(extra)
                connection.commit()
            elif task == "FETCH":
                format_str = "SELECT Tour FROM Solution WHERE ProblemName = \"{n}\" AND Author = \"{a}\""
                sql_command = format_str.format(n=name, a="5130828")
                cursor.execute(sql_command)
                result = cursor.fetchone()
                strResult = str(result)
                if strResult == "None":
                    print("Error: Tried to fetch solution that does not exist. Try again.")
                    exit()
                curTour = []
                for i in result:
                    curTour.append(i)
                return curTour
            elif task == "SHOW":
                format_str = "select x,y from Cities WHERE Name = \"{n}\""
                sql_command = format_str.format(n=name)
                cursor.execute(sql_command)
                result = cursor.fetchall()
                if result == []:
                    print("Error: Tried to solve problem but no problem existed. Try again.")
                    exit()
                return result

            connection.close()

    except Error as e:
        print("Error: Failed to connect to MySQL ", e)


    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")

if __name__ == "__main__":
    main()
