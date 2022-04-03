from configuration import conf 
import psycopg2
import etl 
from sql_queries import create_table_queries, drop_table_queries 


def testSongplaysTable(conn):
    #first test
    return 1


def connectToDatabase():
    conn = psycopg2.connect(
        host=conf["host"],
        database=conf["database"],
        user=conf["user"],
        password=conf["password"]
    )
    cur = conn.cursor()
    return cur, conn
















if __name__ == "__main__":
    cur, conn = connectToDatabase()
    testSongplaysTable(conn)
