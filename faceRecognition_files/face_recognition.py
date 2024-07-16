import cv2
import numpy as np
from flask import Response
from database import mycursor
import os
import boto3
import logging
import base64

s3 = boto3.client('s3',
                  endpoint_url='https://a1c30d551c1d5963fc6afe44c3a6777c.r2.cloudflarestorage.com',
                  region_name='apac',
                  aws_access_key_id='d1862c406a16ad26eba46f3bcaa30f62',
                  aws_secret_access_key='2546d0a0d348fe0460924bedda9fa1213a5c7e26fc312cd82ed0a6eeb65c41bc')

current_dir = os.path.dirname(os.path.abspath(__file__))
classifier_dir = os.path.join(current_dir, "faceRecognition_files")

bucket_name = 'imgdataset'
classifier_prefix = 'classifiers/'




def download_from_s3(bucket_name, s3_key, file_path):
    try:
        s3.download_file(bucket_name, s3_key, file_path)
        print(f"Downloaded {s3_key} from S3 bucket {bucket_name} to {file_path}")
    except Exception as e:
        print(f"Failed to download {s3_key} from S3: {e}")

def list_classifiers_in_cloudflare():
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=classifier_prefix)
        if 'Contents' in response:
            cloudflare_files = [os.path.basename(item['Key']) for item in response['Contents']]
            return cloudflare_files
        else:
            return []
    except Exception as e:
        print(f"Failed to list classifiers in Cloudflare: {e}")
        return []

def delete_local_classifiers_not_in_cloudflare():
    cloudflare_files = list_classifiers_in_cloudflare()
    local_files = [f for f in os.listdir(classifier_dir) if f.startswith("classifier_") and f.endswith(".xml")]

    for local_file in local_files:
        if local_file not in cloudflare_files:
            try:
                os.remove(os.path.join(classifier_dir, local_file))
                print(f"Deleted local classifier {local_file} as it is not present in Cloudflare.")
            except Exception as e:
                print(f"Failed to delete local classifier {local_file}: {e}")

def load_classifiers():
    delete_local_classifiers_not_in_cloudflare()
    
    classifiers = []
    cloudflare_files = list_classifiers_in_cloudflare()

    for file in os.listdir(classifier_dir):
        if file.startswith("classifier_") and file.endswith(".xml"):
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read(os.path.join(classifier_dir, file))
            classifiers.append(clf)

    for classifier_file in cloudflare_files:
        local_path = os.path.join(classifier_dir, classifier_file)
        if not os.path.exists(local_path):
            download_from_s3(bucket_name, f"classifiers/{classifier_file}", local_path)
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read(local_path)
            classifiers.append(clf)

    return classifiers

def get_person_numbers_from_db():
    mycursor.execute("SELECT DISTINCT kodeAnggota FROM img_dataset")
    rows = mycursor.fetchall()
    return [row[0] for row in rows]

faceCascade = cv2.CascadeClassifier(os.path.join("faceRecognition_files", "resources", "haarcascade_frontalface_default.xml"))
classifiers = load_classifiers()


def process_camera_stream(socketio, stop_event):
    global cap
    cap = cv2.VideoCapture(0) 
    if not cap.isOpened():
        logging.error("Error: Could not open video stream.")
        return

    while not stop_event.is_set() and cap.isOpened():
        ret, img = cap.read()
        if not ret:
            logging.error("Failed to read frame from camera")
            break

        ret, buffer = cv2.imencode('.jpg', img)
        frame = base64.b64encode(buffer).decode('utf-8')

        socketio.emit('video_frame', frame, namespace='/video')
        socketio.sleep(0.1)

        coords = detect_faces(img, faceCascade, 1.1, 10, classifiers)
        if coords:
            for coord in coords:
                if coord['confidence'] > 80:
                    logging.debug(f'Emitting: {coord}')
                    socketio.emit('summary', coord, namespace='/video')

    cap.release()
    cv2.destroyAllWindows()

def detect_faces(img, classifier, scaleFactor, minNeighbors, clfs):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

    coords = []

    for (x, y, w, h) in features:
        region = gray_image[y:y + h, x:x + w]
        if region.size == 0:
            continue

        best_confidence = 0
        best_id = None
        for clf in clfs:
            id, pred = clf.predict(region)
            confidence = int(100 * (1 - pred / 300))
            if confidence > best_confidence:
                best_confidence = confidence
                best_id = id

        mycursor.execute("SELECT b.kodeAnggota, b.nama, b.nim, b.gen "
                         "FROM img_dataset a "
                         "LEFT JOIN usermstr b ON a.kodeAnggota = b.kodeAnggota "
                         "WHERE a.img_id = %s", (best_id,))
        s = mycursor.fetchone()

        result = {
            'kodeAnggota': s[0] if s else "UNKNOWN",
            'nama': s[1] if s else "UNKNOWN",
            'nim': s[2] if s else "UNKNOWN",
            'gen': s[3] if s else "UNKNOWN",
            'confidence': best_confidence
        }

        coords.append(result)

    return coords

 


 

