from database import mydb, mycursor
import random
import string

def add_event(kodeAcara, namaEvent, waktuAcara):
    mycursor.execute("""INSERT INTO `eventmstr` (kodeAcara, namaEvent, waktuAcara) VALUES
                    (%s, %s, %s)""", (kodeAcara, namaEvent, waktuAcara))
    mydb.commit()

def generate_event_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))