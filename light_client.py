import socket
import time
from Config import Config
import threading

CLIENT_COMMANDS = {'red' : [255,0,0], 'green': [0,255,0], 'blue' : [0,0,255], 'white' : [255,255,255]}
class client:

    def __init__(self):
        self.color = CLIENT_COMMANDS['white']
        self.isPolling = True
        self.color_lock = threading.Lock()
        self.brightness = 255


    def testing(self):
        print("did a thing")
        time.sleep(3)
    def main(self):
        # Setting up Polling thread to get lighting from server
        pollingThread = threading.Thread(target=self.get_command)
        pollingThread.daemon = True
        pollingThread.start()

        while True:
            pass



    def get_command(self):
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            c.connect((Config.SERVER_IP, Config.PORT))
        except:
            print("Didn't connect")

        while self.isPolling:
            command = 'currentColor'
            c.send(command.encode())
            #with self.color_lock:
            data = c.recv(2048)
            data = data.decode('utf-8')
            self.color = CLIENT_COMMANDS[data]
            print(self.color)
            time.sleep(1)
            if not data:
                break





if __name__ == '__main__':
    client().main()