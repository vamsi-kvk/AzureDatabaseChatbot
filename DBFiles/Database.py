import sys
import os
import pandas as pd
import pyodbc
from Model.AzureOpenAi import CorrectSqlQuery, get_completion_from_messages
from utils.Converter import ResponseToQuerry
from utils.Exception import CustomException
import warnings 
from prompts import prompt3

warnings.filterwarnings('ignore')

from utils.Logger import logging


def get_schema_representation():
    """ Get the database schema Using dict """
    try:
        
        conn = create_connection()
        cursor = conn.cursor()
        
        # Query to get all table names
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE';")
        tables = cursor.fetchall()
        logging.info("Fetched all tables from Database")
        
        db_schema = {}
        
        for table in tables:
            table_name = table[0]
            
            # Query to get column details for each table
            cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'")
            columns = cursor.fetchall()
            
            column_details = {}
            for column in columns:
                ColumnName,column_type,CLength = column
                column_details[ColumnName] = column_type
            
            db_schema[table_name] = column_details
        
        conn.close()
        logging.info("Returning Schema of the Database which has schema {}".format(db_schema))
        return db_schema
    except Exception as e:
        raise CustomException(e,sys)



def query_database(query, c=0):
    """ Run SQL query and return results in a dataframe """
    conn = create_connection()
    try:
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print("Entering into the Model To create correct response.")
        corrected_query = CorrectSqlQuery(query, e)
        c += 1
        if c <= 3:  # Limit the number of correction attempts to avoid infinite recursion
            return query_database(corrected_query, c)
        else: 
            return "Please Check the question and try again later"

        


def create_connection():
    server = os.getenv("server")
    db = os.getenv("db")
    user = os.getenv("user")
    password = os.getenv("password")
    
    """ Create or connect to  MySql Server """
    pyconstring = "Driver={ODBC Driver 18 for SQL Server};Server="+server+",1433;Database="+db+";Uid="+user+";Pwd="+password+";Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

    try:
        conn = pyodbc.connect(pyconstring)
        logging.info("COnnection Sucessfull")
    except Exception as e:
        print(f"Error: {str(e)}")
        return e
    return conn
    





if __name__ == "__main__":

    # Getting the schema representation
    print(get_schema_representation())