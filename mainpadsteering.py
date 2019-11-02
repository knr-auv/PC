from .connectionlaptop import Connection

IP_ADDRESS = ' 192.168.137.68'

conn_thread = Connection(IP_ADDRESS, 8080)
conn_thread.start()


