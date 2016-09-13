import spi
import time
import RPi.GPIO as GPIO

class Controller():

    INSIDE_CONTROLLER_SS_PIN  = 7
    OUTSIDE_CONTROLLER_SS_PIN = 8
    WATER_CONTROLLER_SS_PIN   = 25

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.INSIDE_CONTROLLER_SS_PIN,  GPIO.OUT)

    def test(self):
        a = False
        for i in range(1000):
            GPIO.output(self.INSIDE_CONTROLLER_SS_PIN, a)
            a = not a
            time.sleep(1)

if __name__ == "__main__":
    c = Controller()
    c.test()