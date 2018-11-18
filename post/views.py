from flask import abort, render_template, request, redirect, session, flash
from . import post
from config import koneksi
import sys

db = koneksi.connections()

@post.route('/create/post', methods = ['POST', 'GET'])
def create_post():

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
			'id': row[0],
			'namadepan': row[1],
			'namabelakang': row[2],
			'email': row[3]
		}

	if request.method == 'POST':
		judul    = request.form['judul']
		kategori = request.form['kategori']
		isi      = request.form['isi']
		id_user = get_user['id']

		cur = db.cursor()
		cur.execute('INSERT INTO post(judul, kategori, isi, id_user) VALUES (%s, %s, %s, %s)', (judul, kategori, isi, id_user))
		db.commit()

		flash('Anda berhasil membuat postingan')
		return redirect('/list/post')

	else:

		return render_template('post/main.html', get_user=get_user)

@post.route('/list/post')
def list_post():

	# ambil data user yang sedang login
	cur_user = db.cursor()
	query_user = cur_user.execute('SELECT * FROM user WHERE email = %s', (session['user'],))
	result_user = cur_user.fetchall()

	for row in result_user:

		get_user = {
			'id': row[0],
			'namadepan': row[1],
			'namabelakang': row[2],
			'email': row[3]
		}

	# ambil data postingan berdasarkan siapa yang buat / login
	cur_post = db.cursor()
	query_post = cur_post.execute('SELECT * FROM post WHERE id_user = %s', (get_user['id'],))
	result_post = cur_post.fetchall()

	return render_template('post/list.html', postData = result_post, get_user = get_user)


@post.route('/view/post/<int:post_id>')
def view_post(post_id):
	# ambil data postingan berdasarkan id yang ada di url
	cur = db.cursor()
	query = cur.execute('SELECT * FROM post WHERE id = %s', (post_id,))
	result = cur.fetchall()

	for row in result:
		get_post = { 'id': row[0], 'judul': row[1], 'kategori': row[2], 'isi': row[3], 'tgl_post': row[5] }

	return render_template('post/view.html', getPost = get_post)

@post.route('/edit/post/<int:post_id>', methods = ['POST', 'GET'])
def edit_post(post_id):

	# ambil data user yang sedang login
	cur_user = db.cursor()
	query_user = cur_user.execute('SELECT * FROM user WHERE email = %s', (session['user'],))
	result_user = cur_user.fetchall()

	for row in result_user:

		get_user = {
			'id': row[0],
			'namadepan': row[1],
			'namabelakang': row[2],
			'email': row[3]
		}

	cur = db.cursor()
	query = cur.execute('SELECT * FROM post WHERE id = %s', (post_id,))
	result = cur.fetchall()

	for row in result:
		get_post = {
			'id': row[0],
			'judul': row[1],
			'kategori': row[2],
			'isi': row[3],
			'id_user': row[6],
		}

	if request.method == 'POST':

		judul = request.form['judul']
		kategori = request.form['kategori']
		isi = request.form['isi']

		query_edit = cur.execute('UPDATE post SET judul = %s, kategori = %s, isi = %s WHERE id = %s', (judul, kategori, isi, get_post['id']))
		db.commit()

		flash('Berhasil mengedit postingan !')

		return redirect('/list/post')

	else:
		return render_template('post/edit.html', get_post = get_post, get_user = get_user)

@post.route('/delete/post/<int:post_id>')
def delete_post(post_id):
	cur = db.cursor()
	query = cur.execute('DELETE FROM post WHERE id = %s', (post_id,))
	db.commit()

	flash('Berhasil menghapus postingan !')

	return redirect('/list/post')
