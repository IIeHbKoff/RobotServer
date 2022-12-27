import socket

from common_files.protocol import Protocol


class Connection:
    def __init__(self):
        self.sock = None

    def connect(self, host, port):
        self.sock = socket.socket()
        self.sock.connect((host, port))

    def send(self, message: str):
        self.sock.send(message.encode())

    def receive_from_socket(self):
        received_bytes = list()
        packet_started = False
        while True:
            symbol = self.sock.recv(1)
            if symbol == Protocol.start_symbol.encode():
                packet_started = True
                continue
            elif symbol == Protocol.end_symbol.encode():
                break
            if packet_started:
                received_bytes.append(symbol.decode())
        # self.conn.close()
        # self.conn = None
        return "".join(received_bytes)

    def send_and_receive(self, message):
        self.send(message)
        return self.receive_from_socket()

    def close(self):
        self.sock.close()
