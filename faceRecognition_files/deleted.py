from database import mydb, mycursor

def delete_data(kodeAnggota):
    try:
        mycursor.execute("DELETE FROM img_dataset WHERE kodeAnggota = %s", (kodeAnggota,))
        mycursor.execute("DELETE FROM usermstr WHERE kodeAnggota = %s", (kodeAnggota,))
        mydb.commit()
        
        print(f"Data for kodeAnggota {kodeAnggota} deleted successfully.")
    except Exception as e:
        mydb.rollback()
        print(f"Failed to delete data for kodeAnggota {kodeAnggota}: {e}")

# if __name__ == "__main__":
#     kodeAnggota = input("Enter the kodeAnggota to delete: ")
#     delete_data(kodeAnggota)
