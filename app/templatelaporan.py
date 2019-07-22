import datetime
import pymysql
import random
import mysql.connector
from requestlaporan import RequestLaporan
from mysql.connector import Error
from db import get_db_cms_request, get_db_cms_report
  
class TemplateLaporan:
    def __init__(self):
        self.kode_laporan = ''
        
    def viewReportID(self, kodeLaporan):
        try: 
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_template',
            user='root',
            password='qwerty')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()
        
            cursor.execute(''.join(['SELECT report_tampilan FROM m_report WHERE report_id = "'+kodeLaporan+'"']))

            connection.commit()

            record = cursor.fetchone()
            print ("Your connected...",record)

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")

                    
TemplateLaporan().viewReportID(kodeLaporan)
