import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="GOODGOD97",
        database="emi_project"
    )
