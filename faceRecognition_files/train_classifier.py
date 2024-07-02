import os
import numpy as np
from PIL import Image
import cv2
from flask import redirect

# Dapatkan jalur direktori saat ini
current_dir = os.path.dirname(os.path.abspath(__file__))

def train_classifier(nbr):
    dataset_dir = os.path.join(current_dir, "faceRecognition_files", "dataset")

    path = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir)]
    
    if len(path) == 0:
        return "No images found in dataset directory. Please add images and try again.", 400

    faces = []
    ids = []

    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split(".")[1])

        faces.append(imageNp)
        ids.append(id)
    
    if len(faces) == 0 or len(ids) == 0:
        return "Failed to load images or extract IDs. Please check the dataset directory and image format.", 400

    ids = np.array(ids)

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write(os.path.join(current_dir,"faceRecognition_files", "classifier.xml"))

    return redirect('/')
