import mysql.connector

mydb = mysql.connector.connect(
    # host="9xy.h.filess.io",
    # user="flaskdb_studyingus",
    # passwd="737fa2a12646587f03b4cdcb84c6c9530d654c99",
    # database="flas",
    # port=3307
    host="localhost",
    user="root",
    passwd="",
    database="flask_db",
    port = 3307
)

mycursor = mydb.cursor()
