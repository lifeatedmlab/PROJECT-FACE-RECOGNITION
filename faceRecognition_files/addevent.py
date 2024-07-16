from database import mydb, mycursor

def add_event(kodeAcara, namaEvent, waktuAcara):
    mycursor.execute("""INSERT INTO `eventmstr` (kodeAcara, namaEvent, waktuAcara) VALUES
                    (%s, %s, %s)""", (kodeAcara, namaEvent, waktuAcara))
    mydb.commit()