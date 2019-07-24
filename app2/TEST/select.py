import mysql.connector
from mysql.connector import Error
try:
   mySQLconnection = mysql.connector.connect(host='localhost',
                             database='cms_request',
                             user='root',
                             password='qwerty')
   sql_select_Query = "select * from t_request"
   cursor = mySQLconnection .cursor()
   cursor.execute(sql_select_Query)
   records = cursor.fetchall()
   print("Total number of rows in python_developers is - ", cursor.rowcount)
   print ("Printing each row's column values i.e.  developer record")
   for row in records:
       print("req_id = ", row[0], )
       #print("prog_id = ", row[1])
       #print("user_id  = ", row[2])
       #print("org_id  = ", row[3],)
       #print("ktgri_id = ", row[4],)
       #print("req_kodeLaporan = ", row[5])
       print("req_judul = ", row[6])
       #print("req_deskripsi = ", row[7])
       #print("req_tujuan = ", row[8])
       #print("req_tampilan = ", row[9])
       #print("req_periode = ", row[10])
       print("req_deadline = ", row[11])
       print("req_file = ", row[12])
       print("req_date = ", row[13])
       #print("req_dateAccept = ", row[14])
       #print("req_endDate = ", row[15])
       print("req_status = ", row[16])
       print("req_pic = ", row[17], "\n")
       #print("req_penerima = ", row[18])
       #print("req_prioritas = ", row[19], "\n")
   cursor.close()
   
except Error as e :
    print ("Error while connecting to MySQL", e)
finally:
    #closing database connection.
    if(mySQLconnection .is_connected()):
        mySQLconnection.close()
        print("MySQL connection is closed")
