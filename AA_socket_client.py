#!/bin/python3

import socket
import constants
from utils import colortext, Color, connect_client

SERVER_IP = constants.LAPTOP_SERVER_IP

if __name__ == '__main__':
    with socket.socket() as client_socket:
        connect_client(client_socket, SERVER_IP)
        running = True
        while running:
            count = 1
            request = input(colortext(f'In [{count}]', Color.GREEN))
            client_socket.send(request.encode())
            response = client_socket.recv(1025).decode()
            print(colortext(f'Out [{count}] {response}', Color.RED))
            if response == 'QUIT':
                running = False
