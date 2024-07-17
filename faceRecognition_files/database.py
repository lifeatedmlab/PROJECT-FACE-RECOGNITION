import mysql.connector

mydb = mysql.connector.connect(
  host="sql12.freesqldatabase.com",
  user="sql12720243",
  password="YGj5yeupCX",
  database="sql12720243",
  port=3306
)

mycursor = mydb.cursor()
