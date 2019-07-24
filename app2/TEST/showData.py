import pymysql
from flask import Flask, render_template
connection = mysql.connector.connect(
            host='localhost',
            database='cms_request',
            user='root',
            password='qwerty')
cursor = connection.cursor()
def example():
    cursor.execute("select * from t_request")
    data = cursor.fetchall() #data from database
    return render_template("example.html", value=data)
