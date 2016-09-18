import ibmiotf.device
import time
import json

def callBackTest():
    pass

class IBMConnector():

    def __init__(self, callback):
        self.callback = callback

    def connectToIBM(self):
        try:
            self.client = ibmiotf.device.Client(json.load(open("clientconfig.txt")))
            self.client.connect()
            self.client.commandCallback = self.callback
        except:
            print "Error connection to IBM"

    def pushDataToIBM(self, measurements):
        try:
            measurements['answer'] = 42
            data = {}
            data['d'] = measurements
            self.client.publishEvent("Measurements", "json", data)
            #print "Data send:" + str(data)
        except:
            self.connectToIBM()

if __name__ == "__main__":
    ibm = IBMConnector(callBackTest)
    test = {}
    test['a'] = 1
    test['b'] = 2
    ibm.connectToIBM()
    ibm.pushDataToIBM(test)
    time.sleep(1)