#!/bin/python3

import socket
from enum import Enum

import constants
from termcolor import colored


SERVER_IP = constants.SELF_SERVER_IP


class Color(Enum):
    GREEN = 'green'
    RED = 'red'


def colortext(text: str, color: Color, marker=False):
    if marker:
        return colored(text, on_color=color.value)
    return colored(text, color.value)


def confirm(text: str):
    print(colortext(text, Color.GREEN))


if __name__ == '__main__':
    server_socket = socket.socket()

    valid = False
    port = constants.PROGRAM_PORT
    while not valid:
        try:
            server_socket.bind((SERVER_IP, port))
            valid = True
        except OSError:
            port += 1


    # server_socket.recv(1026).decode()
    server_socket.listen()
    confirm(f'Server is up and running at port {port}')

    (client_socket, client_ip) = server_socket.accept()
    confirm('Client connected')

    name = client_socket.recv(1024).decode()
    print('Client sent: ' + name)

    with client_socket:
        client_socket.send(f'Hello, {name}'.encode())
