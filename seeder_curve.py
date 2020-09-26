import sys
sys.path.append('C:\\Users\\von\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python38\\site-packages')

import serial, time
# pip install pyserial
# pip3 install pyserial
class CurveMaker():

    def __init__(self, portname, rate):
            self.__serialport = serial.Serial()
            self.__serialport.port = portname
            self.__serialport.baudrate = rate
            self.__serialport.writeTimeout = 2
            self.__serialport.open()

            self.__synced = False
            self.__package_length = 8

    def read_packages(self):
        head = 0
        while True:
            data = self.__serialport.read_until(size=1)
            if data == b'\xff':
                head += 1
                if head >= 3:

                    err_source = self.__serialport.read_until(size=2)
                    err_array =bytearray(err_source)
                    err = err_array[0] * 256 + err_array[1]
                    sync = self.__serialport.read_until(size=1)

                    val_source = self.__serialport.read_until(size=2)
                    val_array = bytearray(val_source)
                    val = val_array[0] * 256 + val_array[1]
                    if sync != b'\xff':
                        print('Warning, Lost sync')
                    return err,val
    def main(self):
        while True:
            err, val = self.read_packages()
            print(err, val)
            # print(err)

tester = CurveMaker('COM4', 115200)
tester.main()
