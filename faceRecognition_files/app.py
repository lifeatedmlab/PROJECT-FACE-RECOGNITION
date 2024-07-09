from flask import Flask, render_template, request, redirect, url_for, flash, Response
from database import mydb, mycursor
from dataset import generate_dataset
from face_recognition import face_recognition
from login import login_user
from addperson import add_person, kodeAnggota_exists
from train_classifier import train_classifier
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def home():
    mycursor.execute("SELECT kodeAnggota, nama, nim, gen FROM usermstr")
    data = mycursor.fetchall()

    return render_template('index.html', data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_user(request, render_template, flash, redirect, url_for)

@app.route('/data_anggota', methods=['GET', 'POST'])
def data_anggota():
    return render_template('data_anggota.html')

@app.route('/addprsn')
def addprsn():
    return render_template('addprsn.html')

@app.route('/addprsn_submit', methods=['POST'])
def addprsn_submit():
    kodeAnggota = request.form.get('txtkdag').upper()
    nama = request.form.get('txtnama')
    nim = request.form.get('txtnim')
    gen = request.form.get('optgen')
    
    if not kodeAnggota:
        flash('Kode Anggota tidak boleh kosong', 'error')
        return redirect(url_for('addprsn'))
    
    if not nama:
        flash('Nama tidak boleh kosong', 'error')
        return redirect(url_for('addprsn'))
    
    if not nim:
        flash('NIM tidak boleh kosong', 'error')
        return redirect(url_for('addprsn'))
    
    if kodeAnggota_exists(kodeAnggota):
        flash(f'Kode Anggota {kodeAnggota} sudah ada. Silakan gunakan kode yang lain.', 'error')
        return redirect(url_for('addprsn'))

    add_person(kodeAnggota, nama, nim, gen)
    return redirect(url_for('vfdataset_page', kodeAnggota=kodeAnggota))

@app.route('/vfdataset_page/<kodeAnggota>')
def vfdataset_page(kodeAnggota):
    return render_template('gendataset.html', kodeAnggota=kodeAnggota)

@app.route('/vidfeed_dataset/<kodeAnggota>')
def vidfeed_dataset(kodeAnggota):
    return Response(generate_dataset(kodeAnggota), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed():
    return Response(face_recognition(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/fr_page')
def fr_page():
    return render_template('fr_page.html')

@app.route('/train_classifier/<kodeAnggota>')
def train_classifier_route(kodeAnggota):
    return train_classifier(kodeAnggota)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
