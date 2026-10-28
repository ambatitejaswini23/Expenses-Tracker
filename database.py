import mysql.connector

def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@123",
        database="expenses_tracker"
    )
    return conn