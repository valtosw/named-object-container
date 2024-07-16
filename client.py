import socket
from datetime import datetime

HEADER_LENGTH = 1
HOST = '' #your IP here
PORT = 1032
FORMAT = 'utf-8'

lines = ["SYSTEM LOGS\n"]


class Client:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.client.connect((self.host, self.port))
        self.client.setblocking(False)
        self.handle_connection()

    def handle_connection(self):
        while True:
            command = input("Enter command: ")
            self.client.send((" " + command).encode(FORMAT))

            lines.append(f"{datetime.now()} - Client - {command}\n")

            self.who(command)

            if command == "!disconnect":
                self.receive()

                self.client.close()
                break

            self.read(command)

            self.write(command)

            self.get(command)

            self.wrong_command(command)

    def receive(self):
        while True:
            try:
                response = self.client.recv(1024).decode(FORMAT)
                print(response)
                lines.append(f"{datetime.now()} - Server - {response}\n")
                break
            except BlockingIOError:
                continue

    def read(self, command):
        if command == "!read":
            object_name = input("Enter object name: ")
            self.client.send((" " + object_name).encode(FORMAT))

            lines.append(f"{datetime.now()} - Client - {object_name}\n")

            self.receive()

    def who(self, command):
        if command == "!who":
            self.receive()

    def write(self, command):
        if command == "!write":
            object = input("Enter object(<Name, Type, Value>): ")
            self.client.send((" " + object).encode(FORMAT))
            lines.append(f"{datetime.now()} - Client - {object}\n")
            self.receive()

    def get(self, command):
        if command == "!get":
            self.receive()

    def wrong_command(self, command):
        if command not in ["!read", "!write", "!get", "!who", "!disconnect"]:
            self.receive()


def run_client():
    client = Client()
    client.start()


if __name__ == '__main__':
    run_client()

    with open("output_client.txt", "w") as f:
        f.writelines(lines)
        f.flush()
