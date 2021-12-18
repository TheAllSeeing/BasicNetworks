import socket
from constants import PROGRAM_PORT, LAPTOP_SERVER_IP

CLIENT_IP = LAPTOP_SERVER_IP

if __name__ == '__main__':
    client_socket = socket.socket()

    valid = False
    port = PROGRAM_PORT
    while not valid:
        try:
            client_socket.connect((CLIENT_IP, port))
            print(f'Connected at port {port}')
            valid = True
        except OSError:
            port += 1



