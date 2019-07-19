import mysql.connector
from mysql.connector import Error
try:
   connection = mysql.connector.connect(host='localhost',
                             database='cms_request',
                             user='root',
                             password='qwerty')
   if connection.is_connected():
        db_Info= connection.get_server_info()
        print("Connected to MySQL database...",db_Info)

        cursor = connection.cursor()
        cursor.execute('select * from t_request')
            
        record = cursor.fetchall()

        print("Total number of rows in python_developers is - ", cursor.rowcount)
        print ("Printing each row's column values i.e.  developer record")
        for row in record:
           print (row[0], row[1], row[2], row[3], row[4], row[5])
        
        cursor.close()
   
except Error as e :
    print ("Error while connecting to MySQL", e)
finally:
    #closing database connection.
    if(connection .is_connected()):
        connection.close()
        print("MySQL connection is closed")
