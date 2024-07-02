import mysql.connector

mydb = mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12717385",
    passwd="9YhkHLjLSS",
    database="sql12717385",
    port=3306
)

mycursor = mydb.cursor()
