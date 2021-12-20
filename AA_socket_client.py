#!/bin/python3

import socket
import constants
from AC_protocol import Message
from utils import colortext, Color, connect_client, CouldNotFindPortError

SERVER_IP = constants.LAPTOP_SERVER_IP

if __name__ == '__main__':

    try:
        with socket.socket() as client_socket:
            connect_client(client_socket, SERVER_IP)
            running = True
            count = 1
            while running:
                request = Message(input(colortext(f'In [{count}]: ', Color.GREEN)))
                request.send(client_socket)
                response = Message.receive(client_socket)
                if response is not None:
                    print(colortext(f'Out [{count}]: ', Color.RED) + response + '\n')
                    if response == 'QUIT':
                        running = False
                    count += 1
    except CouldNotFindPortError:
        pass
