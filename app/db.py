import pymysql
import mysql.connector
from mysql.connector import Error
from flask import g


def close_db(e=None):
        db = g.pop("db", None)
        if db is not None:
            db.close

def get_db_cms_request():
        try: 
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_request',
            user='root',
            password='qwerty')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print ("===========================")    
            print("Connected to MySQL database...")
            print ("===========================",db_Info)

            cursor = connection.cursor()
     

        except Error as e :
            print("Error while connecting file MySQL", e)
        #finally:
                #Closing DB Connection.
         #           if(connection.is_connected()):
          #              cursor.close()
           #             connection.close()
            #        print("MySQL connection is closed")



def get_db_cms_template():
        try: 
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_template',
            user='root',
            password='qwerty')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print ("===========================")    
            print("Connected to MySQL database...")
            print ("===========================",db_Info)

            cursor = connection.cursor()
     

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")
get_db_cms_request()		
