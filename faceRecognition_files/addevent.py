from database import mydb, mycursor

def eventExists(kodeAcara):
    mycursor.execute("SELECT COUNT(*) FROM eventmstr WHERE kodeAcara = %s", (kodeAcara,))
    events = mycursor.fetchone()
    return events[0] > 0

def add_event(kodeAcara, namaEvent, waktuAcara):
    mycursor.execute("""INSERT INTO eventmstr (kodeAcara, namaEvent, waktuAcara) VALUES
                    (%s, %s, %s)""", (kodeAcara, namaEvent, waktuAcara))
    mydb.commit()