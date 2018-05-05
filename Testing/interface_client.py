import json
import socket
from Testing.Config import Config
from Testing.light_client import client

class interface_client(client):
    def main(self):
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            c.connect((Config.SERVER_IP, Config.PORT))
        except:
            print("Didn't Connect!")
            exit(1)

        c.send('interface'.encode())
        data = c.recv(2048).decode('utf-8')
        # if data is not "waiting for input":
        #     exit(1)
        while True:
            stdin = input("color")
            stdin = {'1': stdin, '2': 'urmomgay', '3': 'sendnudes'}
            data_dump = json.dumps(stdin)
            print(type(data_dump))
            print(data_dump)
            print(stdin)
            c.send(data_dump.encode())






if __name__ == '__main__':
    interface_client().main()