from database import mydb, mycursor

def add_attendance(eventId, kodeAnggota,  waktu):
    sql = "INSERT INTO absensi (eventId, kodeAnggota, waktu) VALUES (%s, %s, %s)"
    val = (eventId, kodeAnggota,  waktu)
    mycursor.execute(sql, val)
    mydb.commit()

def check_if_already_absent(eventId, kodeAnggota):
    sql = "SELECT COUNT(*) FROM absensi WHERE eventId = %s AND kodeAnggota = %s"
    val = (eventId, kodeAnggota)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    return result[0] > 0