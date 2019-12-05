from connectionlaptop import Connection

IP_ADDRESS = '10.42.0.158'
PORT = 8181

if __name__ == "__main__":
    conn_flag = True  # flaga -> opuszczanie petli od razu polaczeniu
    while conn_flag :
        conn_thread = Connection(IP_ADDRESS, PORT)
        conn_flag = not conn_thread.flag

    conn_thread.start()
