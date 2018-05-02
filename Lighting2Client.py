#!/home/pi/.virtualenvs/remi/bin/python
import json
import socket
import pigpio

from Config import Config

class client:

    list_of_colors = []
    def __init__(self):
        self.r = 255
        self.g = 255
        self.b = 255
        self.pi = pigpio.pi()

        self.red = color([[250, 255],[70,130],[0,150]],[255,0,0])
        self.green = color([[235,245],[250,255],[74,194]], [0,255,0])
        self.blue = color([[97,116],[25,86],[253,255]], [0,0,255])
        self.purple = color([[125,169],[88,91],[253,255]],[255,0,255])
        self.pink = color([[170,255],[70,90],[214,255]], [255,20,147])
        self.orange = color([[253,255],[100,155],[18,45]], [255,69,0])

        self.list_of_colors = [self.purple, self.pink, self.orange, self.green,self.red, self.blue]

    def main(self):
        self.get_color()

    def get_color(self):
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            c.connect((Config.SERVER_IP, Config.PORT))
        except socket.error as e:
            print(str(e))

        print(c.recv(1044).decode('utf-8'))
        while True:
            data = c.recv(1024).decode('utf-8')
            if not data:
                break
            data = json.loads(data)
            print(data)

            for color in self.list_of_colors:
                if in_range(self, color.range, data):
                    print("changing to " + str(color))
                    self.r, self.g, self.b = color.color
                    break
                else:
                    self.r, self.g, self.b = data
            self.pi.set_PWM_dutycycle(Config.RED_PIN, self.r)
            self.pi.set_PWM_dutycycle(Config.GREEN_PIN, self.g)
            self.pi.set_PWM_dutycycle(Config.BLUE_PIN, self.b)


def in_range(self, range, values):

    return_val = True
    if (values[0] < range[0][0]):
        return_val = False
    if (values[0] > range[0][1]):
        return_val = False
    if (values[1] < range[1][0]):
        return_val = False
    if (values[1] > range[1][1]):
        return_val = False
    if (values[2] < range[2][0]):
        return_val = False
    if (values[2] > range[2][1]):
        return_val = False

    return return_val



class color:
    def __init__(self, range, returnColor):
        self.range = range
        self.color = returnColor

    def getColor(self):
        return self.color

    def getRange(self):
        return self.range

    def __str__(self):
        return str(self.color)


if __name__ == '__main__':
    client().main()