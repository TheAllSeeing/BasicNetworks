#!/bin/python3
import datetime
import random
import socket

import constants
import utils
from utils import confirm

REQUESTS_IP = constants.SELF_SERVER_IP


def time() -> str:
    return datetime.datetime.now().strftime('HH:mm')


def whoru() -> str:
    return socket.gethostname()


def rand() -> str:
    return str(random.randint(1, 10))


def exit() -> str:
    return 'QUIT'


COMMANDS = {
    'TIME': time,
    'WHORU': whoru,
    'RAND': rand,
    'EXIT': exit
}


def respond(command: str) -> str:
    try:
        return COMMANDS[command]()
    except KeyError:
        commands = list(COMMANDS.keys())
        commands.sort()
        return f'{command}: Command not found. Available command are {", ".join(commands)}'


if __name__ == '__main__':
    server_socket = socket.socket()

    utils.connect_server(server_socket, REQUESTS_IP)

    (client_socket, client_ip) = server_socket.accept()
    confirm('Client connected')

    command = client_socket.recv(1024).decode()
    print('Command received: ' + command)

    client_socket.send(respond(command).encode())
