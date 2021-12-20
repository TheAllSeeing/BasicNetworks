import socket
from enum import Enum

from termcolor import colored

import constants


class Color(Enum):
    GREEN = 'green'
    RED = 'red'
    YELLOW = 'yellow'


class CouldNotFindPortError(Exception):
    pass


def colortext(text: str, color: Color, marker=False):
    if marker:
        return colored(text, on_color=color.value)
    return colored(text, color.value)


def confirm(text: str):
    print(colortext(text, Color.GREEN))


def error(text: str):
    print(colortext(text, Color.RED))


def warning(text: str):
    print(colortext(text, Color.YELLOW))


def connect_client(connection_socket: socket.socket, server_ip: int):
    valid = False
    port = constants.PROGRAM_PORT
    while not valid and port < 8830:
        try:
            connection_socket.connect((server_ip, port))
            confirm(f'Connected at port {port}')
            valid = True
        except OSError:
            port += 1
    if not valid:
        raise CouldNotFindPortError(error('Error: Could not find a free and connected port'))


def connect_server(connection_socket: socket.socket, request_ip: int):
    valid = False
    port = constants.PROGRAM_PORT
    while not valid:
        try:
            connection_socket.bind((request_ip, port))
            confirm(f'Connected at port {port}')
            valid = True
        except OSError:
            port += 1

    connection_socket.listen()
    confirm(f'Server is up and running at port {port}')
