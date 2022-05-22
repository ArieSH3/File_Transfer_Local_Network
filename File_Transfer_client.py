import socket
import tkinter as tk
from tkinter import Tk
from tkinter.filedialog import askopenfilename	
import tqdm
import os




class Client_Connect:
	def __init__(self):
		self.PORT = 2210
		self.SERVER_ADDRESS = '127.0.0.1' # '192.168.0.18'

		self.SEPARATOR = '<SEP>'
		self.buffer_size = 4096 # send 4096 bytes each timestep

		# Adding socket(IPv4, TCP) to client_socket var
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Referencing a file needed to be transfered
		self.filename = askopenfilename() #'BPM.exe' #'data.txt'
		self.filesize = os.path.getsize(self.filename)


		try:
			print('[CLIENT] connecting to the server...')
			self.client_socket.connect((self.SERVER_ADDRESS, self.PORT))
			print('[CLIENT] connected to the server.')

		except ConnectionRefusedError:
			print('[CLIENT] failed to connect to the server.')

		# Sends the filename and filesize to server
		self.client_socket.send('{}{}{}'.format(self.filename, self.SEPARATOR, self.filesize).encode('utf-8'))

		# Setting up the progress bad values
		self.progress = tqdm.tqdm(range(self.filesize),'Sending {}'.format(self.filename), unit='B', unit_scale=True, unit_divisor=1024)

		# 'rb' is read binary mode
		with open(self.filename, 'rb') as f:

			while True:
				# Read the bytes from the file
				self.bytes_read = f.read(self.buffer_size)
				if not self.bytes_read:
					# file transmitting is done
					break

				# We use sendall to assure transmission in busy networks
				# 	No encoding cus its not text, but a file (I think)
				self.client_socket.sendall(self.bytes_read)

				# Update the progress bar
				self.progress.update(len(self.bytes_read))

		self.client_socket.close()


class Client_App(Client_Connect):
	pass





if  __name__== '__main__':
	Tk().withdraw()
	Client_Connect()