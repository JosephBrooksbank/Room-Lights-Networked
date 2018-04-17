import socket
import threading
from Config import Config

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((Config.SERVER_HOST, Config.PORT))
except socket.error as e:
    print(str(e))

color = 'blue'
brightness = 255
commands = {'currentColor' : color, 'brightness' : str(brightness)}


s.listen(5)


def handler(conn, addr):
    global commands
    while True:
        try:
            data = conn.recv(2048)
        except:
            print("Connection closed")
            break
        data = data.decode('utf-8')
        conn.sendall(commands[data].encode())
        print("sent")

while True:
    conn, addr = s.accept()
    print("got connection")
    client_thread = threading.Thread(target=handler, args=(conn, addr))
    client_thread.daemon = True
    client_thread.start()
    #conn.close()



