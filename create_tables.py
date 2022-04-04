import psycopg2
from sql_queries import create_table_queries, drop_table_queries
from configuration import conf

def connect_to_database():
    # connect to sparkify database
    # conf variable can be found in configuration.py file, this contains the configuration details for the database
    conn = psycopg2.connect(
        host=conf["host"],
        database=conf["database"],
        user=conf["user"],
        password=conf["password"]
    )
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    cur, conn = connect_to_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()