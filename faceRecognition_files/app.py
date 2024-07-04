from flask import Flask, render_template, request, redirect, url_for, flash, Response
from database import mydb, mycursor
from dataset import generate_dataset
from face_recognition import face_recognition
from login import login_user
from addperson import get_next_person_number, add_person
from train_classifier import train_classifier
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    mycursor.execute("select prs_nbr, prs_name, prs_skill, prs_active, prs_added from prs_mstr")
    data = mycursor.fetchall()

    return render_template('index.html', data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_user(request, render_template, flash, redirect, url_for)

@app.route('/data_anggota', methods = ['GET', 'POST'])
def data_anggota():
        return render_template('data_anggota.html')


@app.route('/addprsn')
def addprsn():
    nbr = get_next_person_number()
    return render_template('addprsn.html', newnbr=int(nbr))

@app.route('/addprsn_submit', methods=['POST'])
def addprsn_submit():
    prsnbr = request.form.get('txtnbr')
    prsname = request.form.get('txtname')
    prsskill = request.form.get('optskill')
    add_person(prsnbr, prsname, prsskill)
    return redirect(url_for('vfdataset_page', prs=prsnbr))

@app.route('/vfdataset_page/<prs>')
def vfdataset_page(prs):
    return render_template('gendataset.html', prs=prs)

@app.route('/vidfeed_dataset/<nbr>')
def vidfeed_dataset(nbr):
    return Response(generate_dataset(nbr), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed():
    return Response(face_recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/fr_page')
def fr_page():
    return render_template('fr_page.html')

@app.route('/train_classifier/<nbr>')
def train_classifier_route(nbr):
    return train_classifier(nbr)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
