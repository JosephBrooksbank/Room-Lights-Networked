from light_client import client
import threading
from Config import Config
import phue
import rgbxy

class light_hue_client(client):

    def __init__(self):
        super().__init__()
        self.bridge = phue.Bridge(Config.HUE_BRIDGE_IP)
        self.converter = rgbxy.Converter()
        self.currentColor = self.color


        self.bridge.set_group(Config.HUE_GROUP_ID, 'bri', self.brightness)
        xy_value = self.converter.rgb_to_xy(r, g, b)
        self.bridge.set_group(Config.HUE_GROUP_ID, 'xy', xy_value)

    def main(self):
        pollingThread = threading.Thread(target=self.get_command)
        pollingThread.daemon = True
        pollingThread.start()


        while True:
            if self.currentColor != self.color:
                r,g,b = self.color
                xy_value = self.converter.rgb_to_xy(r,g,b)
                self.bridge.set_group(Config.HUE_GROUP_ID, 'bri', self.brightness)
                self.bridge.set_group(Config.HUE_GROUP_ID, 'xy', xy_value)
                self.currentColor = self.color


