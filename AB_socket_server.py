#!/bin/python3
import datetime
import random
import socket

import constants
import utils
from AC_protocol import Message
from utils import confirm

REQUESTS_IP = constants.SELF_SERVER_IP


def time() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


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


def respond(command: str) -> Message:
    try:
        if command is None:
            return None
        return Message(COMMANDS[command]())
    except KeyError:
        commands = list(COMMANDS.keys())
        commands.sort()
        not_found_message = f': Command not found. Available command are {", ".join(commands)}'
        available_command_space = Message.MAX_MESSAGE_LENGTH - len(not_found_message)
        if len(command) > available_command_space:
            command = command[:available_command_space - 3] + '...'
        return Message(f'{command}: {not_found_message}')


if __name__ == '__main__':
    server_socket = socket.socket()

    utils.connect_server(server_socket, REQUESTS_IP)

    (client_socket, client_ip) = server_socket.accept()
    confirm('Client connected')

    running = True
    while running:
        command = Message.receive(client_socket)
        if command != '':
            print('Command received: ' + str(command))
            respond(command).send(client_socket)
        if command == 'EXIT':
            running = False
