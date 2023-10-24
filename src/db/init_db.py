import psycopg2
from psycopg2 import errors

def connect():
    # connection establishment
    conn = psycopg2.connect(
        database="postgres",
        user='postgres',
        password='password',
        host='localhost',
        port='5432'
    )

    conn.autocommit = True

    # Creating a cursor object
    cursor = conn.cursor()
    return cursor, conn

def create_database(cursor, database_name):
    try:
        # Query to create a database if it doesn't exist
        sql = f"CREATE DATABASE {database_name}"
        cursor.execute(sql)
        print(f"Database '{database_name}' has been created successfully!")
    except errors.DuplicateDatabase:
        print(f"Database '{database_name}' already exists. No action taken.")
    except Exception as e:
        print(f"Error creating database: {e}")

def main():
    cursor, conn = connect()
    database_name = "bids"

    # Call the create_database function
    create_database(cursor, database_name)

    # Closing the connection
    conn.close()

if __name__ == '__main__':
    main()
