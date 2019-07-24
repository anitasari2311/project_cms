import mysql.connector
from mysql.connector import Error
try: 
    connection = mysql.connector.connect(
        host='localhost',
        database='cms_request',
        user='root',
        password='qwerty')
    if connection.is_connected():
        db_Info= connection.get_server_info()
        print("Connected to MySQL database...",db_Info)

        cursor = connection.cursor()
        cursor.execute("show tables")
        for i in cursor.fetchall():
            print (i[0])

        cursor.execute("select * from m_kategori")
        for i in cursor.fetchall():
            print (i)
            
        #record = cursor.fetchone()
        #print ("Your connected...",record)

except Error as e :
    print("Error while connecting anita file MySQL", e)
finally:
    #Closing DB Connection.
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


