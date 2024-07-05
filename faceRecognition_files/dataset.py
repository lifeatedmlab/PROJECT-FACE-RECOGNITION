import cv2
import os
from database import mydb, mycursor

# Dapatkan jalur direktori saat ini
current_dir = os.path.dirname(os.path.abspath(__file__))

dataset_dir = os.path.join(current_dir, "faceRecognition_files", "dataset")
if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)

def generate_dataset(kodeAnggota):
    face_classifier = cv2.CascadeClassifier(os.path.join(current_dir, "faceRecognition_files", "resources", "haarcascade_frontalface_default.xml"))

    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            return None
        for (x, y, w, h) in faces:
            cropped_face = img[y:y + h, x:x + w]
        return cropped_face

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    mycursor.execute("SELECT IFNULL(MAX(img_id), 0) FROM img_dataset")
    row = mycursor.fetchone()
    lastid = row[0]

    img_id = lastid
    max_imgid = img_id + 100
    count_img = 0

    while True:
        ret, img = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        cropped_face = face_cropped(img)
        if cropped_face is not None:
            count_img += 1
            img_id += 1
            face = cv2.resize(cropped_face, (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            file_name_path = os.path.join(dataset_dir, f"{kodeAnggota}.{img_id}.jpg")
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(count_img), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            mycursor.execute("""INSERT INTO img_dataset (img_id, kodeAnggota) VALUES (%s, %s)""", (img_id, kodeAnggota))
            mydb.commit()

            frame = cv2.imencode('.jpg', face)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            print(f"Saved image {file_name_path}")

            if cv2.waitKey(1) == 13 or int(img_id) == int(max_imgid):
                break
        else:
            print("No face detected, skipping frame")
    cap.release()
    cv2.destroyAllWindows()
