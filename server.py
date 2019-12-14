import pickle
import socket


class Server:
    def __init__(self, ip):  # Constructing socket, connecting and testing connection with server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 8080
        address = (ip, port)
        self.server.bind(address)
        self.server.listen(2)
        self.statusFlag = False
        self.client, addr = self.server.accept()
        msg = 'Connection succesful'
        self.client.send(pickle.dumps(msg))

    def receive_data(self):  # Method that we run in a thread to capture incoming data from Jetson
        data = self.client.recv(4096)
        return pickle.loads(data)

    def send_data(self, data):
        self.client.send(pickle.dumps(data))
