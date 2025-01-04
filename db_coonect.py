import psycopg2
import numpy

def ps_connect1():
    try:
        with psycopg2.connect(host=host,
        database=database,
        user=user,
        password=password,
        port=port) as db_connection:
         print('Database connection successfull')
         return db_connection

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)



def create_table(db_connection,create_table_query ):

    """
    Create a table if it does not exist in the PostGres database
    """

    try:
        cursor = db_connection.cursor()
        cursor.execute(create_table_query)
        db_connection.commit()
        print("Table created successfully")

    except Exception as e:
        print(f"❌ [CREATING TABLE ERROR]: '{e}'")

def truncate_table(db_connection,truncate_table_query):
    """
    Truncate the table before inserting data into the table
    """
    try:
        cursor = db_connection.cursor()
        cursor.execute(truncate_table_query)
        db_connection.commit()
        print("Table truncated successfully")

    except Exception as e:
        print(f"❌ [TRUCATE TABLE ERROR]: '{e}'")


    
def insert_table(db_connection,insert_table_query,df):

    """
    Insert data into target table
    """
    try:
        cursor = db_connection.cursor()
        data_values_as_tuples = [tuple(x) for x in df.to_numpy()]
        cursor.executemany(insert_table_query,data_values_as_tuples)
        db_connection.commit()
        print("Data inserted successfully")
        
    except Exception as e:
        print(f"❌ [INSERT TABLE ERROR]: '{e}'")



if __name__ == '__main__':
    db_connection = ps_connect()
    #create_table(db_connection,create_table_query)
