import socket, threading
from datetime import datetime

HEADER_LENGTH = 1
HOST = ''
PORT = 1032
FORMAT = 'utf-8'

f = open("output_server.txt", "w")
f.write("SYSTEM LOGS\n")


class Client:
    def __init__(self, conn, addr):
        self.conn = conn
        self.host, self.addr = addr
        self.objects = []


class Server:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.accept_connections()

    def accept_connections(self):
        while True:
            f.flush()
            client = Client(*self.server.accept())
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    def handle_client(self, client):
        print(f"[NEW CONNECTION] {client.addr} connected.")

        f.write(f"{datetime.now()} - AT SERVER - [NEW CONNECTION] {client.addr} connected.\n\n")
        f.flush()

        while True:
            try:
                msg_length = int.from_bytes(client.conn.recv(HEADER_LENGTH), byteorder='big')
                if msg_length:
                    msg = client.conn.recv(msg_length).decode(FORMAT)

                    f.write(f"{datetime.now()} - Client {client.addr} - {msg}\n")
                    f.flush()

                    comm = msg.split()[0]
                    if comm == "!read":
                        self.read(client)
                    if comm == "!write":
                        self.write(client)
                    if comm == "!get":
                        self.get(client)
                    if comm == "!who":
                        self.who(client)
                    if comm == "!disconnect":
                        self.disconnect(client)
                        return
                    if comm not in ["!read", "!write", "!get", "!who", "!disconnect"]:
                        self.send_response(client, "Invalid command\n")

                        f.write(f"{datetime.now()} - Server - Invalid command\n\n")
                        f.flush()

            except Exception as e:
                f.write(f"{datetime.now()} - ERROR AT SERVER- {e}\n\n")
                f.flush()
                break

    def read(self, client):
        input_object_name = client.conn.recv(int.from_bytes(client.conn.recv(HEADER_LENGTH), byteorder='big')).decode(FORMAT)

        f.write(f"{datetime.now()} - Client {client.addr} - {input_object_name}\n")
        f.flush()

        for object in client.objects:
            if object[1:len(object) - 1].split(", ")[0] == input_object_name:
                self.send_response(client, f"Object: {object}\n")
                f.write(f"{datetime.now()} - Server - Object: {object}\n\n")
                f.flush()
                return

        self.send_response(client, "Object not found\n")
        f.write(f"{datetime.now()} - Server - Object not found\n\n")
        f.flush()

    def write(self, client):
        input_object = client.conn.recv(int.from_bytes(client.conn.recv(HEADER_LENGTH), byteorder='big')).decode(FORMAT)

        f.write(f"{datetime.now()} - Client {client.addr} - {input_object}\n")
        f.flush()

        already_exists, already_exists_object = False, ""

        for object in client.objects:
            if object[1:len(object) - 1].split(", ")[0] == input_object[1:len(input_object) - 1].split(", ")[0]:
                already_exists = True
                already_exists_object = object
                client.objects.remove(object)
                break

        client.objects.append(input_object)

        if already_exists:
            self.send_response(client,
                               f"Object with the same name({already_exists_object}) already exists. Overwriting with {input_object}\n")
            f.write(
                f"{datetime.now()} - Server - Object with the same name({already_exists_object}) already exists. Overwriting with {input_object}\n\n")
            f.flush()
        else:
            self.send_response(client, f"Added object: {input_object}\n")
            f.write(f"{datetime.now()} - Server - Added object: {input_object}\n\n")
            f.flush()

    def get(self, client):
        if len(client.objects) == 0:
            self.send_response(client, "There are no objects in the container\n")
            f.write(f"{datetime.now()} - Server - There are no objects in the container\n\n")
            f.flush()
            return

        result = ""

        for object in client.objects:
            result += object[1:len(object) - 1].split(", ")[0] + " "

        self.send_response(client, "Objects' names are: " + result + "\n")
        f.write(f"{datetime.now()} - Server - Objects' names are: {result}\n\n")
        f.flush()

    def who(self, client):
        self.send_response(client, f"This is a Named Object Container\n")
        f.write(
            f"{datetime.now()} - Server - This is a Named Object Container\n\n")
        f.flush()

    def disconnect(self, client):
        print(f"[DISCONNECTED] Client {client.addr} disconnected.")

        f.write(f"{datetime.now()} - AT SERVER - [DISCONNECTED] Client {client.addr} disconnected.\n")
        f.flush()

        self.send_response(client, "Disconnecting...")
        f.write(f"{datetime.now()} - Server - Disconnecting...\n\n")
        f.flush()

    @staticmethod
    def send_response(client, response):
        client.conn.send(response.encode(FORMAT))


def run_server():
    print("[STARTING] Server has been started...")
    f.write(f"{datetime.now()} - AT SERVER - [STARTING] Server has been started...\n")

    server = Server()
    server.start()


if __name__ == '__main__':
    run_server()
