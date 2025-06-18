import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="insurance_interest"
    )
