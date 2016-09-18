import time

from IBMConnector import IBMConnector
from SystemSensor import SystemSensor
from Controller   import Controller
from Camera       import Camera

def commandCallback(cmd):
    print("Command received: %s with data: %s" % (cmd.command, cmd.data))

    value = cmd.data['d']['value']

    if cmd.command == "InsideFan":
        pass
    elif cmd.command == "OutsideFan":
        pass
    elif cmd.command == "Humidifier":
        pass
    elif cmd.command == "Hatch":
        pass
    elif cmd.command == "Stepper":
        pass
    elif cmd.command == "Picture":
        pass

    else:
        print "Unknown command, ignore"
        print(cmd.command)

if __name__ == "__main__":
    print "Mexican Strawberry Client Master Controll Program"
    print "Version 0.1"

    ibm          = IBMConnector(commandCallback())
    systemSensor = SystemSensor()
    camera       = Camera()
    controller   = Controller()

    time.sleep(1)