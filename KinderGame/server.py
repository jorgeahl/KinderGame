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

host = ''
port = 50000
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(5)
print "SERVER RUNNING"
while 1:
    client, address = s.accept()
    data = client.recv(size)
    if data:
		print "RECIEVED: "+data
		datalist = data.split("@")
		if datalist[0] == "LOGIN":
			Login(datalist[1],datalist[2])
		if datalist[0] == "QUERY":
			Query(datalist[1])
		client.send("DATA RECIEVED")
    client.close() 
