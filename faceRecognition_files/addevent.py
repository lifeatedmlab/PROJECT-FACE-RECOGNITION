from database import mydb, mycursor
import random
import string

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
