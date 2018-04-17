from light_client import client
import threading

RED_PIN = 17
GREEN_PIN = 24
BLUE_PIN = 22
MAX_BRIGHTNESS = 255

class light_strip_client(client):

    def __init__(self):
        super().__init__()
        #self.pi = pigpio.pi()

    def main(self):

        # Setting up Polling thread to get lighting from server
        pollingThread = threading.Thread(target=self.get_command)
        pollingThread.daemon = True
        pollingThread.start()

        while True:
            brightness_ratio = self.brightness / MAX_BRIGHTNESS
            r,g,b = self.color
            self.pi.set_PWM_dutycycle(RED_PIN, r * brightness_ratio)
            self.pi.set_PWM_dutycycle(GREEN_PIN, g * brightness_ratio)
            self.pi.set_PWM_dutycycle(BLUE_PIN, b * brightness_ratio)




if __name__ == '__main__':
    light_strip_client().main()
