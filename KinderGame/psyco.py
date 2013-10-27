import sys
import socket
import psycopg2

cursor = None
conn_string = ""

#function used to connect to the database
def Login(Username, Password):
	global cursor
	global conn_string
	#Define our connection string
	conn_string = "host='c3.east1.stormdb.us' dbname='k1382186238' user='"+Username+"' password='"+Password+"'"
 
	# print the connection string we will use to connect
	print "Connecting to database\n	->%s" % (conn_string)
 
	
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)
 
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	print "Connected!\n"

def Query(query):
	global cursor
	print "<"+query+">"
	cursor.execute(query)
	
	
user = raw_input("Username: ")
password = raw_input("Password: ")
Login(user,password)
query = raw_input("Enter your Query: ")
Query(query)
