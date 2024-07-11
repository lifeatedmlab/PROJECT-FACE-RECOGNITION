from database import mydb, mycursor

def get_event():
    mycursor.execute("SELECT * FROM eventmstr")
    events = mycursor.fetchone()
    return events[0]

def add_event(kodeAcara, namaEvent, waktuAcara):
    mycursor.execute("""INSERT INTO eventmstr (kodeAcara, namaEvent, waktuAcara) VALUES
                    (%s, %s, %s)""", (kodeAcara, namaEvent, waktuAcara))
    mydb.commit()