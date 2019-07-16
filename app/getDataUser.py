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

        latihan_id = input("Latihan_Id = ")
        latihan_deskripsi = input("Latihan_deskripsi = ")
        cursor = connection.cursor()
        cursor.execute('insert into latihan values (%s, %s)', (latihan_id, latihan_deskripsi))

        connection.commit()
        cursor.close()
   
except Error as e :
    print ("Error while connecting to MySQL", e)
finally:
    #closing database connection.
    if(connection .is_connected()):
        connection.close()
        print("MySQL connection is closed")
