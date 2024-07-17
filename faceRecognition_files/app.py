from flask import Flask, render_template, request, redirect, url_for, flash,  jsonify, Response
from database import mydb, mycursor
from dataset import generate_dataset
from face_recognition import process_camera_stream
from login import login_user
from addperson import add_person, kodeAnggota_exists
from train_classifier import train_classifier
from addevent import eventExists, add_event, generate_event_id
import os
import logging
from enum import Enum
from flask_socketio import SocketIO, emit
from threading import Event
from datetime import datetime
from absensi import  add_attendance


app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)
stop_event = Event()

class Generation(Enum):
    GEN4 = '4'
    GEN5 = '5'
    GEN6 = '6'

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
    return render_template('addprsn.html', generations=Generation)

@app.route('/addprsn_submit', methods=['POST'])
def addprsn_submit():
    kodeAnggota = request.form.get('txtkdag').upper()
    nama = request.form.get('txtnama').title()
    nim = request.form.get('txtnim')
    gen = request.form.get('optgen')
    
    if not kodeAnggota:
        flash('Kode Anggota tidak boleh kosong', 'error')
        return redirect(url_for('addprsn'))
    
    if len(kodeAnggota) != 4 :
        flash('Kode Anggota tidak valid', 'error')
        return redirect(url_for('addprsn'))
    
    if not nama:
        flash('Nama tidak boleh kosong', 'error')
        return redirect(url_for('addprsn'))
    
    if not nim:
        flash('NIM tidak boleh kosong', 'error')
        return redirect(url_for('addprsn'))
    
    try:
        nim = int(nim)
    except ValueError:
        flash('NIM harus berupa angka', 'error')
        return redirect(url_for('addprsn'))

    
    if kodeAnggota_exists(kodeAnggota):
        flash(f'Kode Anggota {kodeAnggota} sudah ada. Silakan gunakan kode yang lain.', 'error')
        return redirect(url_for('addprsn'))

    add_person(kodeAnggota, nama, nim, gen)
    return redirect(url_for('vfdataset_page', kodeAnggota=kodeAnggota, nama=nama, nim=nim, gen=gen))

@app.route('/vfdataset_page/<kodeAnggota>')
def vfdataset_page(kodeAnggota):
    nama = request.args.get('nama')
    nim = request.args.get('nim')
    gen = request.args.get('gen')
    return render_template('gendataset.html', kodeAnggota=kodeAnggota, nama=nama, nim=nim, gen=gen)

@app.route('/vidfeed_dataset/<kodeAnggota>')
def vidfeed_dataset(kodeAnggota):
    return Response(generate_dataset(kodeAnggota), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect', namespace='/video')
def handle_connect():
    global stop_event
    logging.debug('Client connected')
    stop_event.clear()
    socketio.start_background_task(target=process_camera_stream, socketio=socketio, stop_event=stop_event)

@socketio.on('disconnect', namespace='/video')
def handle_disconnect():
    global stop_event
    logging.debug('Client disconnected')
    stop_event.set()

# @app.route('/fr_page')
# def fr_page():
#     return render_template('fr_page.html')

@app.route('/train_classifier/<kodeAnggota>')
def train_classifier_route(kodeAnggota):
    return train_classifier(kodeAnggota)

@app.route('/event')
def event():
    mycursor.execute("SELECT * FROM eventmstr")
    events = mycursor.fetchall()

    return render_template('event.html', events=events)

@app.route('/data_event')
def data_event():
    return render_template('event_register.html')

@app.route('/event_register', methods=['POST'])
def event_register():
    kodeAcara = request.form.get('kode-event')
    namaEvent = request.form.get('nama-event')
    waktuAcara = request.form.get('tanggal')
    
    if not kodeAcara:
        flash('Kode Acara tidak boleh kosong', 'error')
        return redirect(url_for('data_event'))
    
    if not namaEvent:
        flash('Nama Event tidak boleh kosong', 'error')
        return redirect(url_for('data_event'))
    
    if not waktuAcara:
        flash('Waktu Acara tidak boleh kosong', 'error')
        return redirect(url_for('data_event'))
    
    if eventExists(kodeAcara):
        flash(f'Kode Acara {kodeAcara} sudah ada. Silakan gunakan kode yang lain.', 'error')
        return redirect(url_for('data_event'))
    
    add_event(kodeAcara, namaEvent, waktuAcara)
    return redirect(url_for('data_event', kodeAcara=kodeAcara, namaEvent=namaEvent, waktuAcara=waktuAcara))



@app.route('/absensi')
def absensi():
    return render_template('absensi.html')

@app.route('/absensi_event')
def absensi_event():
    return render_template('absensi_event.html')

@app.route('/submit_absensi', methods=['POST'])
def submit_absensi():
    data = request.json
    event_id = generate_event_id()
    waktu_sekarang = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    kode_anggota = data['kodeAnggota']

    add_attendance(kode_anggota, waktu_sekarang)
    
    return jsonify({'message': 'Data saved successfully',  'waktu': waktu_sekarang}), 200

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
