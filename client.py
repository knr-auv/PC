import pickle
import socket


class Client:
    def __init__(self, ip, port):  # konstruktor tworzy socket oraz łączy i testuje połączenie z serverem
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port

        try:
            self.client.connect((self.ip, self.port))
            msg1 = self.client.recv(4096)
            self.flag = True
        except Exception as e:
            msg1 = pickle.dumps('Connection error')
            self.flag = False
        finally:
            print("Connection test: ", pickle.loads(msg1))

    def receive_data(self):  # metoda, którą odpalimy w wątku i będzie odbierać napływające dane z severa
        data = self.client.recv(4096)
        try:
            data = pickle.loads(data)
        except Exception as e:
            print(e)
            # data = {'yaw': 0.0, 'pitch': 0.0, 'roll': 0.0}
            data = [0, 0, 0, 0, 0]
        finally:
            return data

    def send_data(self, data):
        self.client.send(pickle.dumps(data))
