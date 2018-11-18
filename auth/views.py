from flask import abort, render_template, request, redirect, session, flash
from . import auth
from config import koneksi
import sys

db = koneksi.connections()

@auth.route('/', methods = ['POST', 'GET'])
def index():

	if 'user' in session: # jika user sudah berhasil login
		return redirect('/dashboard')

	if request.method == 'POST':
		email    = request.form['email']
		password = request.form['password']

		cur = db.cursor()
		resultValue = cur.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))

		if resultValue > 0: # apakah data user ada di database, jika sudah maka
			session['user'] = request.form['email']
			return redirect('/dashboard') # akan di redirect ke halaman dashboard
		else: # jika tidak, maka tidak bisa login
			message = 'Email atau Password salah'
			return render_template('main.html', message = message)
	else:
		return render_template('main.html')

@auth.route('/register', methods = ['POST', 'GET'])
def register():

	if 'user' in session: # jika user sudah berhasil login
		return redirect('/dashboard')

	if request.method == 'POST':
		firstname = request.form['namadepan']
		lastname  = request.form['namabelakang']
		email 	  = request.form['email']
		password  = request.form['password']

		cur = db.cursor()
		cur.execute("INSERT INTO user(namadepan, namabelakang, email, password) VALUES (%s, %s, %s, %s)", (firstname, lastname, email, password))
		db.commit()

		flash('Anda berhasil mendaftar. Silahkan login !')
		return redirect('/')

	return render_template('register.html')

@auth.route('/dashboard')
def dashboard():

	if 'user' in session: # cek apakah session sudah ada,
		# maka kita hanya kasih pass, atau membiarkan saja
		pass
	else: # jika user belum login, maka akan redirect ke halaman awal
		return redirect('/')

	# ambil data user yang sedang login
	cur = db.cursor()
	query = cur.execute('SELECT * FROM user WHERE email = %s', (session['user'],))
	result = cur.fetchall()

	for row in result:

		get_user = {
			'namadepan': row[1],
			'namabelakang': row[2],
			'email': row[3]
		}

	return render_template('dashboard.html', get_user = get_user)

@auth.route('/logout')
def logout():
	# hapus session jika ada session
	session.pop('user', None)
	flash('Anda berhasil keluar. Terima kasih sudah berkunjung ke web ini hahaha !')
	return redirect('/')