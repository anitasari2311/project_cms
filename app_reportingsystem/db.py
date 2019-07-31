import mysql.connector
import pymysql
from flask import g
from mysql.connector import Error
from flask.cli import with_appcontext
from flask import current_app


def get_db_request():

    connection = mysql.connector.connect(
    host='localhost',
    database='cms_request',
    user='root',
    password='qwerty')
    if connection.is_connected():
        db_Info= connection.get_server_info()
    print("Connected to MySQL database...",db_Info)
    return connection







# def close_db(e=None):
#     """If this request connected to the database, close the
#     connection.
#     """
#     db = g.pop("db", None)
#
#     if db is not None:
#         db.close()
