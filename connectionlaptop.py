from padsteering import *
from client import *


#IP_ADDRESS = '192.168.137.68' #adres odroida
# wersja laptop = server
# class Connection(Thread):
#     def __init__(self, ip):
#         Thread.__init__(self)
#         self.server = Server(ip)
#         self.pad = PadSteering()
#
#     def run(self):
#         self.pad.start()
#         while True:
#             # odbiera ramki i zapisuje je w zmiennej
#             self.dataFrame = self.server.receiveData()
#
#     def getDataFrame(self):
#         return self.dataFrame


# IP_ADDRESS = '192.168.137.68' #adres odroida
# wersja laptop = client


class Connection(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.client = Client(ip, port)
        self.flag = self.client.flag
        self.data_frame = []
        self.pad = PadSteering()
        self.trigger_thread = TriggerThread(self.pad)


    def run(self):
        self.pad.start()
        self.trigger_thread.start()
        while True:
            # wysyła ramki danych z pada
            self.client.sendData(self.pad.get_output())
            print(self.pad.get_output())


    def set_data_frame(self, data_frame):
        self.data_frame = data_frame

    def get_data_frame(self):
        return self.data_frame
