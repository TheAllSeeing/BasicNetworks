from socket import socket
from typing import Optional

import utils


class Message:
    VALIDATION = '@@@'
    VALIDATION_LENGTH  = len(VALIDATION)
    LENGTH_LENGTH = 2
    MAX_MESSAGE_LENGTH = int('9' * LENGTH_LENGTH)
    GARBAGE_TOLERANCE = 1000

    def __init__(self, message: str):
        self.message = message
        self.length = len(message)

        if self.length > Message.MAX_MESSAGE_LENGTH:
            self.length = Message.MAX_MESSAGE_LENGTH
            self.message = self.message[:Message.MAX_MESSAGE_LENGTH + 1]
            utils.warning(f'Warning: cutting message at max length {Message.MAX_MESSAGE_LENGTH}: {self.message}')

    def __len__(self):
        return self.length

    def __str__(self):
        return f'{Message.VALIDATION}{str(self.length).zfill(Message.LENGTH_LENGTH)}{self.message}'

    def send(self, connection: socket):
        connection.send(str(self).encode())

    @classmethod
    def receive(cls, connection: socket) -> str:
        validation = ''
        read_count = 0

        while validation != Message.VALIDATION:
            validation = connection.recv(Message.VALIDATION_LENGTH).decode()
            read_count += Message.VALIDATION_LENGTH
            if read_count > Message.GARBAGE_TOLERANCE:
                utils.warning(f'Gave up after {Message.GARBAGE_TOLERANCE} bytes of garbage')
                return ''

        if read_count > Message.VALIDATION_LENGTH:
            utils.warning(f'Warning: Invalid protocol; skipped {read_count - 3} bytes of garbage')

        length_message = connection.recv(Message.LENGTH_LENGTH).decode()

        try:
            message_length = int(length_message)
            return connection.recv(message_length).decode()
        except ValueError:
            utils.warning(f'Invalid protocol; garbage length {length_message}')
            return ''
