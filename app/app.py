import pymysql
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template

conn = mysql.connector.connect(
    host = 'localhost',
    database = 'cms_request',
    user = 'root',
    password = 'qwerty')
cursor = conn.cursor()

def example():
    cursor.execute("select * from m_user")
    data = cursor.fetchall() #data from database

    #return render_template("example.html", value=data)
