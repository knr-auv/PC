import socket
import cv2
import pickle
import struct
import logging


class StreamServer:
    """Klasa Tworzy serwer do odbierania ramek zdjec"""
    def __init__(self, port=8485, host=''):
        """Inicjalizacja socekta """
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.debug("Socket created port:{}".format(port))
        self.socket.bind((host, port))
        logging.debug("Socket bind complete port:{}".format(port))
        self.socket.listen(10)
        logging.debug("Socket now listening port:{}".format(port))
        self.conn, self.addr = self.socket.accept()
        self.data = b""
        self.payload_size = struct.calcsize(">L")

    """Metdoa zwraca klatke OpenCV uzyskana z socketa """
    def recive_frame(self):
        while len(self.data) < self.payload_size:
            logging.debug(str("Recv: {} port:{}".format(len(self.data), self.port)))
            self.data += self.conn.recv(4096)
        logging.debug(str("Done Recv: {}".format(len(self.data))))
        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        logging.debug("msg_size: {}".format(msg_size))
        while len(self.data) < msg_size:
            self.data += self.conn.recv(4096)
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]

        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        return cv2.imdecode(frame, cv2.IMREAD_COLOR)









