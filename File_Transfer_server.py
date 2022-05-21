import socket
import tqdm
import os




PORT = 2210
SERVER_ADDRESS = '127.0.0.1'

buffer_size = 4096 # Receive 4096 bytes each time
SEPARATOR = '<SEP>'

# Start server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_ADDRESS, PORT))

# Listen for connection
# Five is the number of unaccepted connection system will allow before refusing other connections
server_socket.listen(5) 
print('[SERVER] listening on {}'.format(server_socket.getsockname()))


# Accept connection if there is any
client_socket, client_address = server_socket.accept()
print('Connected')

received = client_socket.recv(buffer_size).decode('utf-8')
filename, filesize = received.split(SEPARATOR)

# Remove absolute path if there is one
filename = os.path.basename(filename)

# Convert to integer
filesize = int(filesize)

# Start receiving the file from the socket 
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), 'Receiving {}'.format(filename), unit='B', unit_scale=True, unit_divisor=1024)
with open(filename, 'wb') as f:
	while True:
		# read 1024 bytes from the socket(receive)
		bytes_read = client_socket.recv(buffer_size)
		if not bytes_read:
			# Nothing is received
			# File transmitting is over
			break

		# Write the file to the bytes we just received
		f.write(bytes_read)

		# Updates the progress bar
		progress.update(len(bytes_read))




client_socket.close()
print('Disconnected')

server_socket.close()

