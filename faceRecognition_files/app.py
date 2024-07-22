from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from database import mydb, mycursor
from dataset import generate_dataset, delete_dataset
from face_recognition import process_camera_stream
from addperson import add_person, kodeAnggota_exists
from train_classifier import train_classifier
from addevent import add_event, generate_event_id
import os
import logging
from enum import Enum
from flask_socketio import SocketIO, emit
from threading import Event
from datetime import datetime
from absensi import add_attendance
import pytz

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)
stop_event = Event()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Generation(Enum):
    GEN4 = '4'
    GEN5 = '5'
    GEN6 = '6'

class User(UserMixin):
    def __init__(self, id, is_admin):
        self.id = id
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    mycursor.execute("SELECT * FROM adminmstr WHERE KodeAdmin = %s", (user_id,))
    user = mycursor.fetchone()
    if user:
        return User(user_id, user[2])
    return None

@app.route('/')
def home():
    return render_template('index.html', current_url=request.path)

@app.route('/data_anggota')
def dataanggota():
    mycursor.execute("SELECT kodeAnggota, nama, nim, gen FROM usermstr")
    data = mycursor.fetchall()
    return render_template('data_anggota.html', data=data, current_url=request.path)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        mycursor.execute("SELECT * FROM adminmstr WHERE username = %s AND password = %s", (username, password))
        account = mycursor.fetchone()
        if account:
            user = User(account[0], account[2])  # Assuming the 'is_admin' flag is at index 2
            login_user(user)
            session['kode_admin'] = account[0]  # Simpan kode admin ke dalam session
            return redirect(url_for('dataanggota'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)

@app.route('/logout', methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect('/')

@app.route('/addprsn')
def addprsn():
    return render_template('addprsn.html', generations=Generation, current_url=request.path)

@app.route('/addprsn_submit', methods=['POST'])
def addprsn_submit():
    kodeAnggota = request.form.get('txtkdag').upper()
    nama = request.form.get('txtnama').title()
    nim = request.form.get('txtnim')
    gen = request.form.get('optgen')

    if not kodeAnggota:
        flash('Kode Anggota tidak boleh kosong', 'error')
        return redirect(url_for('addprsn'))

    if len(kodeAnggota) != 4:
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
    return render_template('gendataset.html', kodeAnggota=kodeAnggota, nama=nama, nim=nim, gen=gen, current_url='/addprsn')

@app.route('/retry_dataset/<kodeAnggota>')
def retry_dataset(kodeAnggota):
    delete_dataset(kodeAnggota)
    mycursor.execute("SELECT nama, nim, gen FROM usermstr WHERE kodeAnggota = %s", (kodeAnggota,))
    user_data = mycursor.fetchone()
    
    if user_data:
        nama, nim, gen = user_data
    else:
        nama, nim, gen = '', '', ''
    return redirect(url_for('vfdataset_page', kodeAnggota=kodeAnggota, nama=nama, nim=nim, gen=gen))


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

@app.route('/train_classifier/<kodeAnggota>')
def train_classifier_route(kodeAnggota):
    return train_classifier(kodeAnggota)

@app.route('/event')
@login_required
def event():
    mycursor.execute("SELECT kodeAcara, namaEvent, waktuAcara FROM eventmstr")
    events = mycursor.fetchall()
    return render_template('event.html', events=events, current_url=request.path)

@app.route('/data_event')
@login_required
def data_event():
    return render_template('event_register.html', current_url='/event')

@app.route('/event_register', methods=['POST'])
@login_required
def event_register():
    kodeAcara = request.form.get('kode-event')
    namaEvent = request.form.get('nama-event')
    waktuAcara = request.form.get('tanggal')
    kodeAdmin = session.get('kode_admin')

    if not kodeAcara or not namaEvent or not waktuAcara:
        return redirect(url_for('data_event'))

    add_event(kodeAcara, namaEvent, waktuAcara, kodeAdmin)
    return redirect(url_for('event'))

@app.route('/absensi')
def absensi():
    return render_template('absensi.html', current_url=request.path)

@app.route('/select_event')
def select_event():
    mycursor.execute("SELECT kodeAcara, namaEvent, eventId  FROM eventmstr")
    select_event = mycursor.fetchall()
    return render_template('select_event.html', events=select_event, current_url=request.path)

@app.route('/check_passkey', methods=['POST'])
def check_passkey():
    kode_acara = request.form['kode_acara']
    passkey = request.form['passkey']
    mycursor.execute("SELECT kodeAcara, eventId FROM eventmstr WHERE kodeAcara = %s", (kode_acara,))
    result = mycursor.fetchone()
    if result and result[0] == passkey:
        return jsonify({'status': 'success', 'message': 'Passkey is correct', 'eventId': result[1]})
    else:
        return jsonify({'status': 'fail', 'message': 'Incorrect passkey'})
    
@app.route('/absensi_event')
def absensi_event():
    mycursor.execute("SELECT eventId, namaEvent FROM eventmstr")
    events = mycursor.fetchall()
    return render_template('absensi_event.html', events=events, current_url=request.path)


@app.route('/submit_absensi', methods=['POST'])
# @login_required
def submit_absensi():
    data = request.json
    waktu_sekarang_utc = datetime.now(pytz.utc)
    
    jakarta_tz = pytz.timezone('Asia/Jakarta')
    waktu_sekarang_wib = waktu_sekarang_utc.astimezone(jakarta_tz).strftime('%Y-%m-%d %H:%M:%S')
    
    kodeAnggota = data['kodeAnggota']
    eventId = data['eventId']

    add_attendance(eventId, kodeAnggota,  waktu_sekarang_wib)
    
    return jsonify({'message': 'Data saved successfully',  'waktu': waktu_sekarang_wib}), 200

@app.route('/get_absensi', methods=['GET'])
@login_required
def get_absensi():
    event_id = request.args.get('eventId')
    if not event_id:
        return jsonify({'status': 'fail', 'message': 'eventId is required'}), 400

    query = """
        SELECT 
            u.kodeAnggota, u.nama, u.nim, u.gen, a.waktu 
        FROM 
            absensi a
        JOIN 
            usermstr u ON a.kodeAnggota = u.kodeAnggota
        JOIN 
            eventmstr e ON a.eventId = e.eventId
        WHERE 
            e.eventId = %s
    """
    mycursor.execute(query, (event_id,))
    results = mycursor.fetchall()
    absensi_data = []
    for row in results:
        absensi_data.append({
            'kodeAnggota': row[0],
            'nama': row[1],
            'nim': row[2],
            'gen': row[3],
            'waktu': row[4].strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify({'status': 'success', 'data': absensi_data}), 200

@app.route('/index/<kodeAnggota>', methods=['DELETE'])
def delete_data(kodeAnggota):
    try:
        mycursor.execute("DELETE FROM absensi WHERE kodeAnggota = %s", (kodeAnggota,))
        
        mycursor.execute("DELETE FROM img_dataset WHERE kodeAnggota = %s", (kodeAnggota,))
        mycursor.execute("DELETE FROM usermstr WHERE kodeAnggota = %s", (kodeAnggota,))
        mydb.commit()
        
        return jsonify({'success': True, 'message': f"Data for kodeAnggota {kodeAnggota} deleted successfully."})
    except Exception as e:
        mydb.rollback()
        return jsonify({'success': False, 'message': f"Failed to delete: {e}"})

    
@app.route('/event/<eventID>', methods=['DELETE'])
def delete_data_event(eventID):
    try:
        logging.debug(f"Attempting to delete event with ID: {eventID}")
        mycursor.execute("DELETE FROM eventmstr WHERE eventID = %s", (eventID,))
        mydb.commit()
        
        return jsonify({'success': True, 'message': f"Data for {eventID} deleted successfully."})
    except Exception as e:
        logging.error(f"Error deleting event with ID: {eventID} - {e}")
        mydb.rollback()
        return jsonify({'success': False, 'message': str(e)})


# @app.route('/editEvent/<eventID>')
# def editEvent(eventID):
#     delete_dataset(eventID)
#     mycursor.execute("SELECT eventID, kodeAcara, kodeAdmin, namaEvent, waktuAcara FROM eventmstr WHERE eventID = %s", (eventID,))
#     event_data = mycursor.fetchone()
    
#     if event_data:
#         eventID, kodeAcara, kodeAdmin, namaEvent, waktuAcara = event_data
#     else:
#         eventID, kodeAcara, kodeAdmin, namaEvent, waktuAcara = '', '', '', '', ''
#     return redirect(url_for('data_event', eventID=eventID, kodeAdmin=kodeAdmin, namaEvent=namaEvent, waktuAcara=waktuAcara))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
