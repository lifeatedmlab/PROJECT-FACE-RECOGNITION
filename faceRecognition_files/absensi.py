from database import mydb, mycursor

def add_attendance(kodeAnggota, waktu):
    sql = "INSERT INTO absensi (kodeAnggota, waktu) VALUES (%s, %s)"
    val = (kodeAnggota, waktu)
    mycursor.execute(sql, val)
    mydb.commit()