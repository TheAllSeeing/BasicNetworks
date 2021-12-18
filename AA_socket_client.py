#!/bin/python3

import socket
import constants

CLIENT_IP = constants.LAPTOP_SERVER_IP

if __name__ == '__main__':
    client_socket = socket.socket()

    valid = False
    port = constants.PROGRAM_PORT
    while not valid:
        try:
            client_socket.connect((CLIENT_IP, port))
            print(f'Connected at port {port}')
            valid = True
        except OSError:
            port += 1

    client_socket.send(input('What is your name? ').encode())
    data = client_socket.recv(1025).decode()
    print(f'Server sent "{data}"')
