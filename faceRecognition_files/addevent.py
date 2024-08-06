from database import mydb, mycursor
import random
import string

def namaEvent_exists(namaEvent):
    mycursor.execute("SELECT COUNT(*) FROM eventmstr WHERE namaEvent = %s", (namaEvent,))
    result = mycursor.fetchone()
    return result[0] > 0

def add_event(kodeAcara, namaEvent, waktuAcara, kodeAdmin):
    try:
        sql = "INSERT INTO eventmstr (kodeAcara, kodeAdmin, namaEvent, waktuAcara) VALUES (%s, %s, %s, %s)"
        val = (kodeAcara, kodeAdmin, namaEvent, waktuAcara)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Event added successfully")
    except Exception as e:
        print(f"Error adding event: {str(e)}")
        mydb.rollback()


def generate_event_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
