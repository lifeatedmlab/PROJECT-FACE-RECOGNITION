import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="flask_db",
    port = 3306
)

mycursor = mydb.cursor()
