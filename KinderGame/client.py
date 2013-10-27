import socket

class SocketConection:
	def __init__(self):
		self.host = '192.168.1.106'
		self.port = 50000
		self.size = 2048
		self.recieved = ""
		
	def Send(self,data):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((self.host,self.port))
		s.send(data)
		self.recieved = s.recv(self.size)
		s.close()
		
		

s = SocketConection()
while True:
	inputs = raw_input("type something here: ")
	s.Send(inputs)
	
	
	
'''
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	inputs = raw_input("type something here: ")
	s.send(inputs)
	data = s.recv(size)
	s.close()
	print 'Received:', data 
'''



		
	
		
	
		
		
