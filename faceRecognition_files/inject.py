from database import mydb, mycursor

# Membuat objek cursor
mycursor = mydb.cursor()

# Query SQL untuk menyuntikkan data
sql = "INSERT INTO adminmstr (kodeAdmin, username, password) VALUES (%s, %s, %s)"
val = [
  (1, 'admin1', 'password1'),
  (2, 'admin2', 'password2'),
  (3, 'admin3', 'password3')
]

try:
    mycursor.executemany(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "records inserted successfully.")

except Exception as e:
    mydb.rollback()
    print(f"Failed to insert records: {e}")

finally:
    mydb.close()
