from database import mydb, mycursor


def add_attendance(eventId, kodeAnggota,  waktu):
    sql = "INSERT INTO absensi (eventId, kodeAnggota, waktu) VALUES (%s, %s, %s)"
    val = (eventId, kodeAnggota,  waktu)
    mycursor.execute(sql, val)
    mydb.commit()
