#!/home/pi/.virtualenvs/Lighting2/bin/python

import time
import threading

import phue
import rgbxy
import pigpio

### CONFIG ###
# As a user, this is what you will be editing

# The id of the group of lights your light strip will be mimicking
# This can also be the name of the group as a string
GROUP_ID = 2
# The light ID itself, this is difficult to obtain without access to the api
# TODO create an installer that gives users options about their light
LIGHT_ID = 7

# The IP of the bridge to use
HUE_BRIDGE_IP = '10.5.44.119'

# The output pins on the rpi that correspond to each color of the light strip
RED_PIN = 17
GREEN_PIN = 24
BLUE_PIN = 22

# The gamut type of the lights used
# Almost definitely GamutC if the lights are new
gamut = rgbxy.GamutC


def in_range(range_of_color, values):

    return_val = True
    if (values[0] < range_of_color[0][0]):
        return_val = False
    if (values[0] > range_of_color[0][1]):
        return_val = False
    if (values[1] < range_of_color[1][0]):
        return_val = False
    if (values[1] > range_of_color[1][1]):
        return_val = False
    if (values[2] < range_of_color[2][0]):
        return_val = False
    if (values[2] > range_of_color[2][1]):
        return_val = False

    return return_val


class Lighting:

    def __init__(self):
        self.pi = pigpio.pi()
        self.converter = rgbxy.Converter(gamut)
        self.bridge = phue.Bridge(HUE_BRIDGE_IP)
        self.rgb = [255,255,255]
        self.rgb_lock = threading.Lock()

        # Color pullups, the xy converter isn't optimal for the RGB led strips so I use these
        # to 'purify' the color
        self.red = Color([[255, 255], [48, 110], [0, 150]], [255, 0, 0])
        self.green = Color([[75, 245], [253, 255], [72, 170]], [0, 255, 0])
        self.blue = Color([[65, 130], [80, 180], [253, 255]], [0, 0, 255])
        self.purple = Color([[125, 169], [88, 91], [253, 255]], [255, 0, 255])
        self.pink = Color([[170, 255], [70, 90], [214, 255]], [255, 20, 147])
        self.orange = Color([[253, 255], [100, 155], [18, 45]], [255, 69, 0])
        # This list sets order of precedence for color, primaries are the most general so they have lowest precedence
        self.list_of_colors = [self.purple, self.pink, self.orange, self.green, self.red, self.blue]

    def main(self):
        polling_thread = threading.Thread(target=self.poll_bridge)
        polling_thread.daemon = True
        polling_thread.start()

        while True:
            self.pi.set_PWM_dutycycle(RED_PIN, self.rgb[0])
            self.pi.set_PWM_dutycycle(GREEN_PIN, self.rgb[1])
            self.pi.set_PWM_dutycycle(BLUE_PIN, self.rgb[2])





    def poll_bridge(self):
        while True:
            try:
                # Getting dict of status of light
                pilot_light = self.bridge.get_light(LIGHT_ID)['state']
                if pilot_light['on'] is False:
                    with self.rgb_lock:
                        self.rgb = [0,0,0]
                else:
                    x,y = pilot_light['xy']
                    brightness = pilot_light['bri']
                    lamp_color = self.converter.xy_to_rgb(x,y,brightness)
                    with self.rgb_lock:
                        for color in self.list_of_colors:
                            if in_range(color.range, lamp_color):
                                self.rgb = color.color
                                break
                            else:
                                self.rgb = lamp_color

            except phue.PhueRequestTimeout:
                print("Timeout, trying again")
            except OSError:
                print("Network error, trying again")

            time.sleep(0.5)


class Color:
    def __init__(self, range, returnColor):
        self.range = range
        self.color = returnColor

    def get_color(self):
        return self.color

    def get_range(self):
        return self.range

    def __str__(self):
        return str(self.color)

if __name__ == '__main__':
    Lighting().main()