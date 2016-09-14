import spidev
import time
import binascii

class Controller():

    INSIDE_CONTROLLER  = 0
    OUTSIDE_CONTROLLER = 1

    SUB_CMD_NETWORK_PING =                          [0x00, 0x00]

    SUB_CMD_FIRMWARE_GET_CONTROLLER_TYPE =          [0x10, 0x00]
    SUB_CMD_FIRMWARE_GET_FIRMWARE_VERSION =         [0x10, 0x10]
    SUB_CMD_FIRMWARE_GET_UPTIME =                   [0x10, 0x20]
    SUB_CMD_FIRMWARE_SET_REBOOT =                   [0x10, 0x30]

    SUB_CMD_SENSOR_GET_TEMPERATURE_OUTSIDE =        [0x20, 0x00]
    SUB_CMD_SENSOR_GET_TEMPERATURE_INSIDE =         [0x20, 0x01]
    SUB_CMD_SENSOR_GET_TEMPERATURE_WATER =          [0x20, 0x02]
    SUB_CMD_SENSOR_GET_TEMPERATURE_LIGHT1 =         [0x20, 0x03]
    SUB_CMD_SENSOR_GET_TEMPERATURE_LIGHT2 =         [0x20, 0x04]
    SUB_CMD_SENSOR_GET_TEMPERATURE_LIGHT3 =         [0x20, 0x05]
    SUB_CMD_SENSOR_GET_HUMIDITY_OUTSIDE =           [0x20, 0x10]
    SUB_CMD_SENSOR_GET_HUMIDITY_INSIDE =            [0x20, 0x11]
    SUB_CMD_SENSOR_GET_CO2 =                        [0x20, 0x20]
    SUB_CMD_SENSOR_GET_PH =                         [0x20, 0x30]
    SUB_CMD_SENSOR_GET_REDOX =                      [0x20, 0x40]

    SUB_CMD_MOTOR_GET_LIGHT_MOVEMENT_SPEED =        [0x30, 0x00]
    SUB_CMD_MOTOR_SET_LIGHT_MOVEMENT_SPEED =        [0x30, 0x01]
    SUB_CMD_MOTOR_GET_LIGHT_MOVEMENT_POSITION =     [0x30, 0x02]
    SUB_CMD_MOTOR_SET_LIGHT_MOVEMENT_POSITION =     [0x30, 0x03]
    SUB_CMD_MOTOR_GET_LIGHT_MOVEMENT_COUNTER =      [0x30, 0x04]
    SUB_CMD_MOTOR_GET_LIGHT_1_FAN_SPEED =           [0x30, 0x10]
    SUB_CMD_MOTOR_SET_LIGHT_1_FAN_SPEED =           [0x30, 0x11]
    SUB_CMD_MOTOR_GET_LIGHT_1_DESIRED_TEMPERATURE = [0x30, 0x12]
    SUB_CMD_MOTOR_SET_LIGHT_1_DESIRED_TEMPERATURE = [0x30, 0x13]
    SUB_CMD_MOTOR_GET_LIGHT_2_FAN_SPEED =           [0x30, 0x20]
    SUB_CMD_MOTOR_SET_LIGHT_2_FAN_SPEED =           [0x30, 0x21]
    SUB_CMD_MOTOR_GET_LIGHT_2_DESIRED_TEMPERATURE = [0x30, 0x22]
    SUB_CMD_MOTOR_SET_LIGHT_2_DESIRED_TEMPERATURE = [0x30, 0x23]
    SUB_CMD_MOTOR_GET_LIGHT_3_FAN_SPEED =           [0x30, 0x30]
    SUB_CMD_MOTOR_SET_LIGHT_3_FAN_SPEED =           [0x30, 0x31]
    SUB_CMD_MOTOR_GET_LIGHT_3_DESIRED_TEMPERATURE = [0x30, 0x32]
    SUB_CMD_MOTOR_SET_LIGHT_3_DESIRED_TEMPERATURE = [0x30, 0x33]
    SUB_CMD_MOTOR_GET_HATCH =                       [0x30, 0x40]
    SUB_CMD_MOTOR_SET_HATCH =                       [0x30, 0x41]
    SUB_CMD_MOTOR_GET_OUTSIDE_FAN =                 [0x30, 0x50]
    SUB_CMD_MOTOR_SET_OUTSIDE_FAN =                 [0x30, 0x51]
    SUB_CMD_MOTOR_GET_INSIDE_FAN =                  [0x30, 0x60]
    SUB_CMD_MOTOR_SET_INSIDE_FAN =                  [0x30, 0x61]

    SUB_CMD_LIGHT_GET_INTENSITY_IR =                [0x40, 0x00]
    SUB_CMD_LIGHT_SET_INTENSITY_IR =                [0x40, 0x01]
    SUB_CMD_LIGHT_GET_INTENSITY_FS =                [0x40, 0x10]
    SUB_CMD_LIGHT_SET_INTENSITY_FS =                [0x40, 0x11]
    SUB_CMD_LIGHT_GET_INTENSITY_UV =                [0x40, 0x20]
    SUB_CMD_LIGHT_SET_INTENSITY_UV =                [0x40, 0x21]

    SUB_CMD_HEATER_GET_HEATER_AIR =                 [0x50, 0x00]
    SUB_CMD_HEATER_SET_HEATER_AIR =                 [0x50, 0x01]
    SUB_CMD_HEATER_GET_HEATER_WATER =               [0x50, 0x10]
    SUB_CMD_HEATER_SET_HEATER_WATER =               [0x50, 0x11]

    def __init__(self):
        self._spi = spidev.SpiDev()

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

    def pingTest(self, controller):
        data = [0x23, 0x42, 0x69]
        r = self._xfer(controller, self.SUB_CMD_NETWORK_PING, data)
        for i in range(len(data)):
            if data[i] != r[i]:
                return False
        return True

    def getControllerType(self, controller):
        r = self._xfer(controller, self.SUB_CMD_FIRMWARE_GET_CONTROLLER_TYPE)
        return r[0]

    def getFirmwareVersion(self, controller):
        r = self._xfer(controller, self.SUB_CMD_FIRMWARE_GET_FIRMWARE_VERSION)
        return r[0:3]

    def getUptime(self, controller):
        r = self._xfer(controller, self.SUB_CMD_FIRMWARE_GET_UPTIME)
        return (r[0]<<(8*3))+(r[1]<<(8*2))+(r[2]<<(8*1))+(r[3]<<(8*0))

    def reboot(self, controller):
        r = self._xfer(controller, self.SUB_CMD_FIRMWARE_SET_REBOOT,[0x4D,0x53])
        return (r[0] == 0x00 and r[1] == 0x00)

    def getTemperatureOutside(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_TEMPERATURE_OUTSIDE)
        v = 0.0
        v += r[0]
        v += r[1] / 100.0
        return v

    def getTemperatureWater(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_TEMPERATURE_WATER)
        v = 0.0
        v += r[0]
        v += r[1] / 100.0
        return v

    def getTemperatureInside(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_TEMPERATURE_INSIDE)
        v = 0.0
        v += r[0]
        v += r[1] / 100.0
        return v

    def getTemperatureLight(self, number):
        if number == 1:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_TEMPERATURE_LIGHT1)
        elif number == 2:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_TEMPERATURE_LIGHT2)
        elif number == 3:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_TEMPERATURE_LIGHT3)
        else:
            raise ValueError
        v = 0.0
        v += r[0]
        v += r[1] / 100.0
        return v

    def getHumidityOutside(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_HUMIDITY_OUTSIDE)
        v = 0.0
        v += r[0]
        v += r[1] / 100.0
        return v

    def getHumidityInside(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_HUMIDITY_INSIDE)
        v = 0.0
        v += r[0]
        v += r[1] / 100.0
        return v

    def getCO2Level(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_CO2)
        return ((r[0]<<(8*1))+(r[1]<<(8*0)))

    def getPHLevel(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_PH)
        v = 0.0
        v += r[0]
        v += r[1] / 100.0
        return v

    def getRedoxLevel(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_SENSOR_GET_REDOX)
        return ((r[0]<<(8*1))+(r[1]<<(8*0)))

    def getLightMovementSpeed(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_MOVEMENT_SPEED)
        return r[0]

    def setLightMovementSpeed(self, speed):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_MOVEMENT_SPEED,[speed])
        return True

    def getLightMovementPosition(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_MOVEMENT_POSITION)
        return ((r[0]<<(8*1))+(r[1]<<(8*0)))

    def setLightMovementPosition(self, speed):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_MOVEMENT_POSITION,[(speed >>8) & 0xFF , speed & 0xFF])
        return True

    def getLightMovementCounter(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_MOVEMENT_COUNTER)
        return ((r[0]<<(8*1))+(r[1]<<(8*0)))

    def getLightFanSpeed(self, number):
        if number == 1:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_1_FAN_SPEED)
        elif number == 2:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_2_FAN_SPEED)
        elif number == 3:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_3_FAN_SPEED)
        else:
            raise ValueError
        return r[0]

    def setLightFanSpeed(self, number, speed):
        if number == 1:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_1_FAN_SPEED,[speed])
        elif number == 2:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_2_FAN_SPEED,[speed])
        elif number == 3:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_3_FAN_SPEED,[speed])
        else:
            raise ValueError
        return True

    def getLightDesiredTemperature(self, number):
        if number == 1:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_1_DESIRED_TEMPERATURE)
        elif number == 2:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_2_DESIRED_TEMPERATURE)
        elif number == 3:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_LIGHT_3_DESIRED_TEMPERATURE)
        else:
            raise ValueError
        return r[0]

    def setLightDesiredTemperature(self, number, speed):
        if number == 1:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_1_DESIRED_TEMPERATURE,[speed])
        elif number == 2:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_2_DESIRED_TEMPERATURE,[speed])
        elif number == 3:
            r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_LIGHT_3_DESIRED_TEMPERATURE,[speed])
        else:
            raise ValueError
        return True

    def getHatch(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_HATCH)
        return r[0]

    def setHatch(self, value):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_HATCH,[value])
        return True

    def getOutsideFan(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_OUTSIDE_FAN)
        return r[0]

    def setOutsideFan(self, value):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_OUTSIDE_FAN,[value])
        return True

    def getInsideFan(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_GET_INSIDE_FAN)
        return r[0]

    def setInsideFan(self, value):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_MOTOR_SET_INSIDE_FAN,[value])
        return True

    def getIRLevel(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_LIGHT_GET_INTENSITY_IR)
        return r[0]

    def setIRLevel(self, value):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_LIGHT_SET_INTENSITY_IR,[value])
        return True

    def getFSLevel(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_LIGHT_GET_INTENSITY_FS)
        return r[0]

    def setFSLevel(self, value):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_LIGHT_SET_INTENSITY_FS,[value])
        return True

    def getUVLevel(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_LIGHT_GET_INTENSITY_UV)
        return r[0]

    def setUVLevel(self, value):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_LIGHT_SET_INTENSITY_UV,[value])
        return True

    def getAirHeaterLevel(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_HEATER_GET_HEATER_AIR)
        return r[0]

    def setAirHeaterLevel(self, value):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_HEATER_SET_HEATER_AIR,[value])
        return True

    def getWaterHeaterLevel(self):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_HEATER_GET_HEATER_WATER)
        return r[0]

    def setWaterHeaterLevel(self, value):
        r = self._xfer(self.INSIDE_CONTROLLER, self.SUB_CMD_HEATER_SET_HEATER_WATER,[value])
        return True





    def test(self):
        print "Controller Ping Test:%s" % self.pingTest(self.INSIDE_CONTROLLER)

        print "Controller Type:%d" % self.getControllerType(self.INSIDE_CONTROLLER)
        print "Firmware %s" % self.getFirmwareVersion(self.INSIDE_CONTROLLER)
        for i in range(2):
            print "Uptime %d" % self.getUptime(self.INSIDE_CONTROLLER)
            time.sleep(1)
        print "Rebooting %d" % self.reboot(self.INSIDE_CONTROLLER)
        time.sleep(1)
        print "Uptime %s" % self.getUptime(self.INSIDE_CONTROLLER)

        print "Outside Temperature %f" % self.getTemperatureOutside()
        print "Inside Temperature %f" % self.getTemperatureInside()
        print "Water Temperature %f" % self.getTemperatureWater()
        for i in range(1,4):
            print "Light %d Temperature %f" %(i, self.getTemperatureLight(i))
        print "Outside Humidity %f" % self.getHumidityOutside()
        print "Inside Humidity %f" % self.getHumidityInside()
        print "CO2 %d" % self.getCO2Level()
        print "PH %f" % self.getPHLevel()
        print "Redox %d" % self.getRedoxLevel()

        print "LightMovement %d" % self.getLightMovementSpeed()
        self.setLightMovementSpeed(233)
        print "LightMovement %d" % self.getLightMovementSpeed()
        print "LightPosition %d" % self.getLightMovementPosition()
        self.setLightMovementPosition(2333)
        print "LightPosition %d" % self.getLightMovementPosition()
        print "LightCounter %d" % self.getLightMovementCounter()
        for i in range(1,4):
            print "LightFanSpeed %d is %d" % (i, self.getLightFanSpeed(i))
            self.setLightFanSpeed(i, 123)
            print "LightFanSpeed %d is %d" % (i, self.getLightFanSpeed(i))
            print "LightDesiredTemperature %d is %d" % (i, self.getLightDesiredTemperature(i))
            self.setLightDesiredTemperature(i, 123)
            print "LightDesiredTemperature %d is %d" % (i, self.getLightDesiredTemperature(i))
        print "Hatch %d" % self.getHatch()
        self.setHatch(67)
        print "Hatch %d" % self.getHatch()


        print "Outside Fan %d" % self.getOutsideFan()
        self.setOutsideFan(87)
        print "Outside Fan %d" % self.getOutsideFan()
        print "Inside Fan %d" % self.getInsideFan()
        self.setInsideFan(96)
        print "Inside Fan %d" % self.getInsideFan()


        print "IR Value %d" % self.getIRLevel()
        self.setIRLevel(33)
        print "IR Value %d" % self.getIRLevel()
        print "FS Value %d" % self.getFSLevel()
        self.setFSLevel(34)
        print "FS Value %d" % self.getFSLevel()
        print "UV Value %d" % self.getUVLevel()
        self.setUVLevel(35)
        print "UV Value %d" % self.getUVLevel()

        print "Air Heater Level %d" % self.getAirHeaterLevel()
        self.setAirHeaterLevel(75)
        print "Air Heater Level %d" % self.getAirHeaterLevel()
        print "Water Heater Level %d" % self.getWaterHeaterLevel()
        self.setWaterHeaterLevel(76)
        print "Water Heater Level %d" % self.getWaterHeaterLevel()

if __name__ == "__main__":
    c = Controller()
    c.test()