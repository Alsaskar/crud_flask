import MySQLdb

def connections():

	db = MySQLdb.connect(host='localhost',
						 user='root',
						 passwd='',
						 db='flaskblog'
						 )

	return db