import json
import socket
import pigpio

from Config import Config

class client:
    def __init__(self):
        self.r = 255
        self.g = 255
        self.b = 255
        self.pi = pigpio.pi()


    def main(self):
        self.get_color()




    def get_color(self):
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            c.connect((Config.SERVER_IP, Config.PORT))
        except socket.error as e:
            print(str(e))

        while True:
            data = c.recv(1024).decode('utf-8')
            if not data:
                break
            data = json.loads(data)
            self.r, self.b, self.g = data
            self.pi.set_PWM_dutycycle(Config.RED_PIN, self.r)
            self.pi.set_PWM_dutycycle(Config.GREEN_PIN, self.g)
            self.pi.set_PWM_dutycycle(Config.BLUE_PIN, self.b)



if __name__ == '__main__':
    client().main()