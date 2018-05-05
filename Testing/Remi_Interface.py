import json

import remi.gui as gui
from Testing.Config import Config
from remi import *
import socket


class Light_Interface(App):
    def __init__(self, *args):
        super(Light_Interface, self).__init__(*args)
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.c.connect((Config.SERVER_IP, Config.PORT))
        except:
            print("Didn't Connect")
            exit(1) # break I guess lmao I don't want to deal with this




    def main(self):
        mainContainer = gui.HBox(width=500, height=500)
        self.leftContainer = gui.VBox(width=250, height=500)
        self.RightContainer = gui.VBox(width=250, height = 500)

        self.topRightContainer = gui.VBox(width=250, height=250)
        self.bottomRightContainer = gui.VBox(width=250, height=250)

        self.colorPicker = gui.ColorPicker(width=250, height=500)
        self.colorPicker.set_on_change_listener(self.colorPicker_listener)
        self.leftContainer.append(self.colorPicker)

        self.RightContainer.append(self.topRightContainer)
        self.RightContainer.append(self.bottomRightContainer)

        mainContainer.append(self.leftContainer)
        mainContainer.append(self.RightContainer)

        return mainContainer
    def colorPicker_listener(selfself, widget, value):
        hex_value = value.lstrip('#')
        rgb = tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))

        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            c.connect((Config.SERVER_IP, Config.PORT))
        except:
            print("Didn't Connect")

        command = 'interface' # This is very insecure as far as handshakes go, lmao
        c.send(command.encode())
        data = c.recv(2048).decode('utf-8')
        print(data)
        data_dump = json.dumps(rgb)
        c.send(data_dump.encode())


start(Light_Interface, address='', port=8081)