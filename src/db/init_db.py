import psycopg2


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


def main():
    cursor, conn = connect()
    # query to create a database
    sql = ''' CREATE database bids ''';

    # executing above query
    cursor.execute(sql)
    print("Database has been created successfully !!");

    # Closing the connection
    conn.close()

if __name__ == '__main__':
    main()
