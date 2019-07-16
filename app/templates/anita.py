import PyMySQL 
import mysql.connector
from mysql.connector import Error
try:
    connection =
mysql.connector.connect(host='localhost',
database='cms_request',
user='root',
password='qwerty')
    if connection.is_connected():
        db_Info= connection.get_server_info()
        print("Connected to MySQL database...",db_Info)

        cursor = connection.cursor()
        cursor


