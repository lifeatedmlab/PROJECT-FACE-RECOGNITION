from database import mydb, mycursor

def kodeAnggota_exists(kodeAnggota):
    mycursor.execute("SELECT COUNT(*) FROM usermstr WHERE kodeAnggota = %s", (kodeAnggota,))
    result = mycursor.fetchone()
    return result[0] > 0

def add_person(kodeAnggota, nama,nim, gen):
    mycursor.execute("""INSERT INTO usermstr (kodeAnggota, nama, nim, gen) VALUES (%s, %s, %s, %s)""",
                     (kodeAnggota, nama, nim, gen))
    mydb.commit()
