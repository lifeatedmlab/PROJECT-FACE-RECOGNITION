import os
import numpy as np
from PIL import Image
import cv2
from flask import redirect, flash, url_for
import boto3

s3 = boto3.client('s3',
                  endpoint_url='https://a1c30d551c1d5963fc6afe44c3a6777c.r2.cloudflarestorage.com',
                  region_name='apac',
                  aws_access_key_id='d1862c406a16ad26eba46f3bcaa30f62',
                  aws_secret_access_key='2546d0a0d348fe0460924bedda9fa1213a5c7e26fc312cd82ed0a6eeb65c41bc')

current_dir = os.path.dirname(os.path.abspath(__file__))

def upload_to_s3(file_path, bucket_name, s3_key):
    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"Uploaded {file_path} to S3 bucket {bucket_name} as {s3_key}")
    except Exception as e:
        print(f"Failed to upload {file_path} to S3: {e}")

def train_classifier(kodeAnggota):
    dataset_dir = os.path.join(current_dir, "faceRecognition_files", "dataset")

    path = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if f.startswith(f"{kodeAnggota}.")]
    
    if len(path) == 0:
        flash("No images found in dataset directory for this ID. Please add images and try again.", "error")
        return redirect(url_for('home'))

    faces = []
    ids = []

    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split(".")[1])

        faces.append(imageNp)
        ids.append(id)
    
    if len(faces) == 0 or len(ids) == 0:
        flash("Failed to load images or extract IDs. Please check the dataset directory and image format.", "error")
        return redirect(url_for('home'))

    ids = np.array(ids)

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    classifier_file = os.path.join(current_dir, "faceRecognition_files", f"classifier_{kodeAnggota}.xml")
    clf.write(classifier_file)

    upload_to_s3(classifier_file, 'imgdataset', f"classifiers/classifier_{kodeAnggota}.xml")

    for file in os.listdir(dataset_dir):
        os.remove(os.path.join(dataset_dir, file))

    flash("Registration successful and classifier uploaded!", "success")
    return redirect(url_for('home'))