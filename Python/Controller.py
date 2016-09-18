import spidev
import time
import binascii
import threading


class ControllerException(Exception):
    pass


class Controller(threading.Thread):

    TEMPERATURE_OUTSIDE    =  1
    TEMPERATURE_INSIDE     =  2
    TEMPERATURE_WATER      =  3
    TEMPERATURE_LIGHT_UV   =  4
    TEMPERATURE_LIGHT_FS   =  5
    TEMPERATURE_LIGHT_IR   =  6
    HUMIDITY_OUTSIDE       =  7
    HUMIDITY_INSIDE        =  8
    CO2                    =  9
    PH                     = 10
    REDOX                  = 11
    MOVEMENT_SPEED         = 12
    MOVEMENT_POSITION      = 13
    MOVEMENT_COUNTER       = 14
    UV_FAN_SPEED           = 15
    FS_FAN_SPEED           = 16
    IR_FAN_SPEED           = 17
    UV_DESIRED_TEMPERATURE = 18
    FS_DESIRED_TEMPERATURE = 19
    IR_DESIRED_TEMPERATURE = 20
    HATCH                  = 21
    OUTSIDE_FAN            = 22
    INSIDE_FAN             = 23
    INTENSITY_UV           = 24
    INTENSITY_FS           = 25
    INTENSITY_IR           = 26
    HEATER_AIR             = 27
    HEATER_WATER           = 28

    INSIDE_CONTROLLER      = 0
    OUTSIDE_CONTROLLER     = 1

    SUB_CMD_NETWORK_PING =                           [0x00, 0x00]

    SUB_CMD_FIRMWARE_GET_CONTROLLER_TYPE =           [0x10, 0x00]
    SUB_CMD_FIRMWARE_GET_FIRMWARE_VERSION =          [0x10, 0x10]
    SUB_CMD_FIRMWARE_GET_UPTIME =                    [0x10, 0x20]
    SUB_CMD_FIRMWARE_SET_REBOOT =                    [0x10, 0x30]

    SUB_CMD_SENSOR_GET_TEMPERATURE_OUTSIDE =         [0x20, 0x00]
    SUB_CMD_SENSOR_GET_TEMPERATURE_INSIDE =          [0x20, 0x01]
    SUB_CMD_SENSOR_GET_TEMPERATURE_WATER =           [0x20, 0x02]
    SUB_CMD_SENSOR_GET_TEMPERATURE_LIGHT_UV =        [0x20, 0x03]
    SUB_CMD_SENSOR_GET_TEMPERATURE_LIGHT_FS =        [0x20, 0x04]
    SUB_CMD_SENSOR_GET_TEMPERATURE_LIGHT_IR =        [0x20, 0x05]
    SUB_CMD_SENSOR_GET_HUMIDITY_OUTSIDE =            [0x20, 0x10]
    SUB_CMD_SENSOR_GET_HUMIDITY_INSIDE =             [0x20, 0x11]
    SUB_CMD_SENSOR_GET_CO2 =                         [0x20, 0x20]
    SUB_CMD_SENSOR_GET_PH =                          [0x20, 0x30]
    SUB_CMD_SENSOR_GET_REDOX =                       [0x20, 0x40]

    SUB_CMD_MOTOR_GET_LIGHT_MOVEMENT_SPEED =         [0x30, 0x00]
    SUB_CMD_MOTOR_SET_LIGHT_MOVEMENT_SPEED =         [0x30, 0x01]
    SUB_CMD_MOTOR_GET_LIGHT_MOVEMENT_POSITION =      [0x30, 0x02]
    SUB_CMD_MOTOR_SET_LIGHT_MOVEMENT_POSITION =      [0x30, 0x03]
    SUB_CMD_MOTOR_GET_LIGHT_MOVEMENT_COUNTER =       [0x30, 0x04]
    SUB_CMD_MOTOR_GET_LIGHT_UV_FAN_SPEED =           [0x30, 0x10]
    SUB_CMD_MOTOR_SET_LIGHT_UV_FAN_SPEED =           [0x30, 0x11]
    SUB_CMD_MOTOR_GET_LIGHT_UV_DESIRED_TEMPERATURE = [0x30, 0x12]
    SUB_CMD_MOTOR_SET_LIGHT_UV_DESIRED_TEMPERATURE = [0x30, 0x13]
    SUB_CMD_MOTOR_GET_LIGHT_FS_FAN_SPEED =           [0x30, 0x20]
    SUB_CMD_MOTOR_SET_LIGHT_FS_FAN_SPEED =           [0x30, 0x21]
    SUB_CMD_MOTOR_GET_LIGHT_FS_DESIRED_TEMPERATURE = [0x30, 0x22]
    SUB_CMD_MOTOR_SET_LIGHT_FS_DESIRED_TEMPERATURE = [0x30, 0x23]
    SUB_CMD_MOTOR_GET_LIGHT_IR_FAN_SPEED =           [0x30, 0x30]
    SUB_CMD_MOTOR_SET_LIGHT_IR_FAN_SPEED =           [0x30, 0x31]
    SUB_CMD_MOTOR_GET_LIGHT_IR_DESIRED_TEMPERATURE = [0x30, 0x32]
    SUB_CMD_MOTOR_SET_LIGHT_IR_DESIRED_TEMPERATURE = [0x30, 0x33]
    SUB_CMD_MOTOR_GET_HATCH =                        [0x30, 0x40]
    SUB_CMD_MOTOR_SET_HATCH =                        [0x30, 0x41]
    SUB_CMD_MOTOR_GET_OUTSIDE_FAN =                  [0x30, 0x50]
    SUB_CMD_MOTOR_SET_OUTSIDE_FAN =                  [0x30, 0x51]
    SUB_CMD_MOTOR_GET_INSIDE_FAN =                   [0x30, 0x60]
    SUB_CMD_MOTOR_SET_INSIDE_FAN =                   [0x30, 0x61]

    SUB_CMD_LIGHT_GET_INTENSITY_IR =                 [0x40, 0x00]
    SUB_CMD_LIGHT_SET_INTENSITY_IR =                 [0x40, 0x01]
    SUB_CMD_LIGHT_GET_INTENSITY_FS =                 [0x40, 0x10]
    SUB_CMD_LIGHT_SET_INTENSITY_FS =                 [0x40, 0x11]
    SUB_CMD_LIGHT_GET_INTENSITY_UV =                 [0x40, 0x20]
    SUB_CMD_LIGHT_SET_INTENSITY_UV =                 [0x40, 0x21]

    SUB_CMD_HEATER_GET_HEATER_AIR =                  [0x50, 0x00]
    SUB_CMD_HEATER_SET_HEATER_AIR =                  [0x50, 0x01]
    SUB_CMD_HEATER_GET_HEATER_WATER =                [0x50, 0x10]
    SUB_CMD_HEATER_SET_HEATER_WATER =                [0x50, 0x11]

    def _controllerTest(self):

        if not self._pingTest(self.INSIDE_CONTROLLER):
            raise ControllerException("No controller not responding on SPI0.0")

        if not self._pingTest(self.OUTSIDE_CONTROLLER):
            raise ControllerException("No controller not responding on SPI0.1")

        if self._getControllerType(self.INSIDE_CONTROLLER) != self.INSIDE_CONTROLLER:
            raise ControllerException("Inside Controller not connected on SPI0.0")

        if self._getControllerType(self.OUTSIDE_CONTROLLER) != self.OUTSIDE_CONTROLLER:
            raise ControllerException("Outside Controller not connected on SPI0.0")

        insideControllerFirmware = self._getFirmwareVersion(self.INSIDE_CONTROLLER)

        if insideControllerFirmware[0] != 0x05 or insideControllerFirmware[1] != 0x23 or insideControllerFirmware[2] != 0x42:
            raise ControllerException("Inside Controller has wrong firmware")

        outsideControllerFirmware = self._getFirmwareVersion(self.OUTSIDE_CONTROLLER)

        if outsideControllerFirmware[0] != 0x05 or outsideControllerFirmware[1] != 0x23 or outsideControllerFirmware[
            2] != 0x42:
            raise ControllerException("Outside Controller has wrong firmware")

    def _setSafeParameters(self):
        self._setAirHeaterLevel(0)
        self._setFSLevel(0)
        self._setHatch(100) # full open
        self._setInsideFan(0)
        self._setIRLevel(0)
        for i in range(1,4):
            self._setLightDesiredTemperature(i, 42)
            self._setLightFanSpeed(i, 50)
        self._setLightMovementPosition(0) # Deactivate fix position
        self._setLightMovementSpeed(0)
        self._setOutsideFan(0)
        self._setUVLevel(0)
        self._setWaterHeaterLevel(0)

    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self._spi = spidev.SpiDev()
        self.state = {}
        self._controllerTest()
        self._setSafeParameters()
        self.start()

    def _measure(self):
        self.state[self.TEMPERATURE_OUTSIDE]    = self._getTemperatureOutside()
        self.state[self.TEMPERATURE_INSIDE]     = self._getTemperatureInside()
        self.state[self.TEMPERATURE_WATER]      = self._getTemperatureWater()
        self.state[self.TEMPERATURE_LIGHT_UV]   = self._getTemperatureLight(1)
        self.state[self.TEMPERATURE_LIGHT_FS]   = self._getTemperatureLight(2)
        self.state[self.TEMPERATURE_LIGHT_IR]   = self._getTemperatureLight(3)
        self.state[self.HUMIDITY_OUTSIDE]       = self._getHumidityOutside()
        self.state[self.HUMIDITY_INSIDE]        = self._getHumidityInside()
        self.state[self.CO2]                    = self._getCO2Level()
        self.state[self.PH]                     = self._getPHLevel()
        self.state[self.REDOX]                  = self._getRedoxLevel()
        self.state[self.MOVEMENT_SPEED]         = self._getLightMovementSpeed()
        self.state[self.MOVEMENT_POSITION]      = self._getLightMovementPosition()
        self.state[self.MOVEMENT_COUNTER]       = self._getLightMovementCounter()
        self.state[self.UV_FAN_SPEED]           = self._getLightFanSpeed(1)
        self.state[self.FS_FAN_SPEED]           = self._getLightFanSpeed(2)
        self.state[self.IR_FAN_SPEED]           = self._getLightFanSpeed(3)
        self.state[self.UV_DESIRED_TEMPERATURE] = self._getLightDesiredTemperature(1)
        self.state[self.FS_DESIRED_TEMPERATURE] = self._getLightDesiredTemperature(2)
        self.state[self.IR_DESIRED_TEMPERATURE] = self._getLightDesiredTemperature(3)
        self.state[self.HATCH]                  = self._getHatch()
        self.state[self.OUTSIDE_FAN]            = self._getOutsideFan()
        self.state[self.INSIDE_FAN]             = self._getInsideFan()
        self.state[self.INTENSITY_UV]           = self._getUVLevel()
        self.state[self.INTENSITY_FS]           = self._getFSLevel()
        self.state[self.INTENSITY_IR]           = self._getIRLevel()
        self.state[self.HEATER_AIR]             = self._getAirHeaterLevel()
        self.state[self.HEATER_WATER]           = self._getWaterHeaterLevel()

    def run(self):
        while True:
            self._measure()
            time.sleep(1)

    def _getCRC(self, cmd, subcmd, data):
        return hex(binascii.crc32("HELLO") & 0xffffffff)

    def _xfer(self, controller, cmd, data=[]):
        s = []
        s.extend(cmd)
        s.append(len(data))
        s.extend(data)
        s.extend([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        self._spi.open(0, controller)
        self._spi.max_speed_hz = 5000
        r = self._spi.xfer2(s)
        self._spi.close()
        return r[4:]

    def _pingTest(self, controller):
        data = [0x23, 0x42, 0x69]
        r = self._xfer(controller, self.SUB_CMD_NETWORK_PING, data)
        for i in range(len(data)):
            if data[i] != r[i]:
                return False
        return True

    def _getControllerType(self, controller):
        r = self._xfer(controller, self.SUB_CMD_FIRMWARE_GET_CONTROLLER_TYPE)
        return r[0]

    def _getFirmwareVersion(self, controller):
        r = self._xfer(controller, self.SUB_CMD_FIRMWARE_GET_FIRMWARE_VERSION)
        return r[0:3]

    def _getUptime(self, controller):
        r = self._xfer(controller, self.SUB_CMD_FIRMWARE_GET_UPTIME)
        return (r[0]<<(8*3))+(r[1]<<(8*2))+(r[2]<<(8*1))+(r[3]<<(8*0))

    def _reboot(self, controller):
        r = self._xfer(controller, self.SUB_CMD_FIRMWARE_SET_REBOOT,[0x4D,0x53])
        return (r[0] == 0x4F and r[1] == 0x4B)

    def _getTemperatureOutside(self):
        r = self._xfer(self.OUTSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_TEMPERATURE_OUTSIDE)
        v = 0.0
        v += r[0]
        v += r[1] / 100.0
        return v

    def _getTemperatureWater(self):
        r = self._xfer(self.OUTSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_TEMPERATURE_WATER)
        v = 0.0
        v += r[0]
        v += r[1] / 100.0
        return v

    def _getTemperatureInside(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_TEMPERATURE_INSIDE)
        v = 0.0
        v += r[0]
        v += r[1] / 100.0
        return v

    def _getTemperatureLight(self, number):
        if number == 1:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_TEMPERATURE_LIGHT_UV)
        elif number == 2:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_TEMPERATURE_LIGHT_FS)
        elif number == 3:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_TEMPERATURE_LIGHT_IR)
        else:
            raise ValueError
        v = 0.0
        v += r[0]
        v += r[1] / 100.0
        return v

    def _getHumidityOutside(self):
        r = self._xfer(self.OUTSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_HUMIDITY_OUTSIDE)
        v = 0.0
        v += r[0]
        v += r[1] / 100.0
        return v

    def _getHumidityInside(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_HUMIDITY_INSIDE)
        v = 0.0
        v += r[0]
        v += r[1] / 100.0
        return v

    def _getCO2Level(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_CO2)
        return ((r[0]<<(8*1))+(r[1]<<(8*0)))

    def _getPHLevel(self):
        r = self._xfer(self.OUTSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_PH)
        v = 0.0
        v += r[0]
        v += r[1] / 100.0
        return v

    def _getRedoxLevel(self):
        r = self._xfer(self.OUTSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_REDOX)
        return ((r[0]<<(8*1))+(r[1]<<(8*0)))

    def _getLightMovementSpeed(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_MOVEMENT_SPEED)
        return r[0]

    def _setLightMovementSpeed(self, speed):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_MOVEMENT_SPEED,[speed])
        return True

    def _getLightMovementPosition(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_MOVEMENT_POSITION)
        return ((r[0]<<(8*1))+(r[1]<<(8*0)))

    def _setLightMovementPosition(self, speed):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_MOVEMENT_POSITION,[(speed >>8) & 0xFF , speed & 0xFF])
        return True

    def _getLightMovementCounter(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_MOVEMENT_COUNTER)
        return ((r[0]<<(8*1))+(r[1]<<(8*0)))

    def _getLightFanSpeed(self, number):
        if number == 1:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_1_FAN_SPEED)
        elif number == 2:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_2_FAN_SPEED)
        elif number == 3:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_3_FAN_SPEED)
        else:
            raise ValueError
        return r[0]

    def _setLightFanSpeed(self, number, speed):
        if number == 1:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_1_FAN_SPEED,[speed])
        elif number == 2:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_2_FAN_SPEED,[speed])
        elif number == 3:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_3_FAN_SPEED,[speed])
        else:
            raise ValueError
        return True

    def _getLightDesiredTemperature(self, number):
        if number == 1:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_1_DESIRED_TEMPERATURE)
        elif number == 2:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_2_DESIRED_TEMPERATURE)
        elif number == 3:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_3_DESIRED_TEMPERATURE)
        else:
            raise ValueError
        return r[0]

    def _setLightDesiredTemperature(self, number, speed):
        if number == 1:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_1_DESIRED_TEMPERATURE,[speed])
        elif number == 2:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_2_DESIRED_TEMPERATURE,[speed])
        elif number == 3:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_3_DESIRED_TEMPERATURE,[speed])
        else:
            raise ValueError
        return True

    def _getHatch(self):
        r = self._xfer(self.OUTSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_HATCH)
        return r[0]

    def _setHatch(self, value):
        r = self._xfer(self.OUTSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_HATCH,[value])
        return True

    def _getOutsideFan(self):
        r = self._xfer(self.OUTSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_OUTSIDE_FAN)
        return r[0]

    def _setOutsideFan(self, value):
        r = self._xfer(self.OUTSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_OUTSIDE_FAN,[value])
        return True

    def _getInsideFan(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_INSIDE_FAN)
        return r[0]

    def _setInsideFan(self, value):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_INSIDE_FAN,[value])
        return True

    def _getIRLevel(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_LIGHT_GET_INTENSITY_IR)
        return r[0]

    def _setIRLevel(self, value):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_LIGHT_SET_INTENSITY_IR,[value])
        return True

    def _getFSLevel(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_LIGHT_GET_INTENSITY_FS)
        return r[0]

    def _setFSLevel(self, value):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_LIGHT_SET_INTENSITY_FS,[value])
        return True

    def _getUVLevel(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_LIGHT_GET_INTENSITY_UV)
        return r[0]

    def _setUVLevel(self, value):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_LIGHT_SET_INTENSITY_UV,[value])
        return True

    def _getAirHeaterLevel(self):
        r = self._xfer(self.OUTSIDE_CONTROLLER, self.SUB_CMD_HEATER_GET_HEATER_AIR)
        return r[0]

    def _setAirHeaterLevel(self, value):
        r = self._xfer(self.OUTSIDE_CONTROLLER, self.SUB_CMD_HEATER_SET_HEATER_AIR,[value])
        return True

    def _getWaterHeaterLevel(self):
        r = self._xfer(self.OUTSIDE_CONTROLLER, self.SUB_CMD_HEATER_GET_HEATER_WATER)
        return r[0]

    def _setWaterHeaterLevel(self, value):
        r = self._xfer(self.OUTSIDE_CONTROLLER, self.SUB_CMD_HEATER_SET_HEATER_WATER,[value])
        return True

    def test(self):
        print "Controller Ping Test:%s" % self._pingTest(self.INSIDE_CONTROLLER)

        print "Controller Type:%d" % self._getControllerType(self.INSIDE_CONTROLLER)
        print "Firmware %s" % self._getFirmwareVersion(self.INSIDE_CONTROLLER)
        for i in range(2):
            print "Uptime %d" % self._getUptime(self.INSIDE_CONTROLLER)
            time.sleep(1)
        print "Rebooting %d" % self._reboot(self.INSIDE_CONTROLLER)
        time.sleep(1)
        print "Uptime %s" % self._getUptime(self.INSIDE_CONTROLLER)

        print "Outside Temperature %f" % self._getTemperatureOutside()
        print "Inside Temperature %f" % self._getTemperatureInside()
        print "Water Temperature %f" % self._getTemperatureWater()
        for i in range(1,4):
            print "Light %d Temperature %f" %(i, self._getTemperatureLight(i))
        print "Outside Humidity %f" % self._getHumidityOutside()
        print "Inside Humidity %f" % self._getHumidityInside()
        print "CO2 %d" % self._getCO2Level()
        print "PH %f" % self._getPHLevel()
        print "Redox %d" % self._getRedoxLevel()

        print "LightMovement %d" % self._getLightMovementSpeed()
        self._setLightMovementSpeed(233)
        print "LightMovement %d" % self._getLightMovementSpeed()
        print "LightPosition %d" % self._getLightMovementPosition()
        self._setLightMovementPosition(2333)
        print "LightPosition %d" % self._getLightMovementPosition()
        print "LightCounter %d" % self._getLightMovementCounter()
        for i in range(1,4):
            print "LightFanSpeed %d is %d" % (i, self._getLightFanSpeed(i))
            self._setLightFanSpeed(i, 123)
            print "LightFanSpeed %d is %d" % (i, self._getLightFanSpeed(i))
            print "LightDesiredTemperature %d is %d" % (i, self._getLightDesiredTemperature(i))
            self._setLightDesiredTemperature(i, 123)
            print "LightDesiredTemperature %d is %d" % (i, self._getLightDesiredTemperature(i))
        print "Hatch %d" % self._getHatch()
        self._setHatch(67)
        print "Hatch %d" % self._getHatch()

        print "Outside Fan %d" % self._getOutsideFan()
        self._setOutsideFan(87)
        print "Outside Fan %d" % self._getOutsideFan()
        print "Inside Fan %d" % self._getInsideFan()
        self._setInsideFan(96)
        print "Inside Fan %d" % self._getInsideFan()

        print "IR Value %d" % self._getIRLevel()
        self._setIRLevel(33)
        print "IR Value %d" % self._getIRLevel()
        print "FS Value %d" % self._getFSLevel()
        self._setFSLevel(34)
        print "FS Value %d" % self._getFSLevel()
        print "UV Value %d" % self._getUVLevel()
        self._setUVLevel(35)
        print "UV Value %d" % self._getUVLevel()

        print "Air Heater Level %d" % self._getAirHeaterLevel()
        self._setAirHeaterLevel(75)
        print "Air Heater Level %d" % self._getAirHeaterLevel()
        print "Water Heater Level %d" % self._getWaterHeaterLevel()
        self._setWaterHeaterLevel(76)
        print "Water Heater Level %d" % self._getWaterHeaterLevel()

if __name__ == "__main__":
    c = Controller()
    c.test()