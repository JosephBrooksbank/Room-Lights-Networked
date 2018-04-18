import socket
import json
import threading
from Config import Config

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((Config.SERVER_HOST, Config.PORT))
except socket.error as e:
    print(str(e))

color = 'blue'
brightness = 255
currentStatus = {'currentColor' : [0,0,255], 'brightness' : 255}


s.listen(5)


def handler(conn, addr):
    global currentStatus
    while True:
        try:
            data = conn.recv(2048)
        except:
            print("Connection closed")
            break
        data = data.decode('utf-8')
        if data == 'interface':
            interface_connection_handler(conn)
            break
        try:
            data_dump = json.dumps(currentStatus[data])
            conn.sendall(data_dump.encode())
            print("sent")
        except NameError:
            pass



def interface_connection_handler(conn):
    conn.sendall("waiting for input".encode())

    data = conn.recv(2048).decode('utf-8')
    if not data:
        print("This wasn't supposed to happen") # I've been working on this far too long
    data_load = json.loads(data)
    if (len(data_load) == 3):
        color = data_load
        print(color)
    conn.shutdown(socket.SHUT_WR)
    print("Closed connection")


while True:
    conn, addr = s.accept()
    print("got connection")
    client_thread = threading.Thread(target=handler, args=(conn, addr))
    client_thread.daemon = True
    client_thread.start()




