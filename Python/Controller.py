import spidev
import time

class Controller():

    def __init__(self):
        self._spi = spidev.SpiDev()

    def test(self):
        self._spi.open(0, 0)
        self._spi.max_speed_hz = 5000
        for i in range(5):
            r = self._spi.xfer2([0x10,0x20,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF])
            print "Firmware Major %d, Minor %d, BuildVersion %d" % (r[4],r[5],r[6])
            time.sleep(1)
        self._spi.close()

if __name__ == "__main__":
    c = Controller()
    c.test()