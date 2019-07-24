import pymysql

cnx = mysql.connector.connect(user='root', password='qwerty',
 host='127.0.0.1',
 database='test')

cnx.close()
