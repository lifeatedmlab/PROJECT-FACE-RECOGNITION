import cv2
import numpy as np
from flask import Response
from database import mycursor
import os

# Dapatkan jalur direktori saat ini
current_dir = os.path.dirname(os.path.abspath(__file__))

def face_recognition():
    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

        coords = []

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)

            id, pred = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))

            mycursor.execute("select b.prs_name "
                             "  from img_dataset a "
                             "  left join prs_mstr b on a.img_peson = b.prs_nbr "
                             " where img_id = %s", (id,))
            s = mycursor.fetchone()

            if s:
                s = ''.join(s)
            else:
                s = "UNKNOWN"

            if confidence > 70:
                cv2.putText(img, s, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
            else:
                cv2.putText(img, "UNKNOWN", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

            coords = [x, y, w, h]
        return coords

    def recognize(img, clf, faceCascade):
        coords = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 0), "Face", clf)
        return img

    faceCascade = cv2.CascadeClassifier(os.path.join(current_dir, "faceRecognition_files", "resources", "haarcascade_frontalface_default.xml"))
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read(os.path.join(current_dir,"faceRecognition_files", "classifier.xml"))

    wCam, hCam = 500, 400

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    while True:
        ret, img = cap.read()
        if not ret:
            continue
        img = recognize(img, clf, faceCascade)

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
