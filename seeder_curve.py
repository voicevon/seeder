import sys
sys.path.append('C:\\Users\\von\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python38\\site-packages')

import serial, time
# pip install pyserial
# 
import xlsxwriter
# pip install xlsxWriter



class CurveMaker():

    def __init__(self, portname, rate, rows=9999):
            self.__serialport = serial.Serial()
            self.__serialport.port = portname
            self.__serialport.baudrate = rate
            self.__serialport.writeTimeout = 2
            self.__serialport.open()

            self.__synced = False
            self.__package_length = 8
            self.workbook = xlsxwriter.Workbook('seeder.xlsx')
            self.worksheet = self.workbook.add_worksheet()
            self.rows = rows
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
        count = 0
        while count < self.rows:
            err, val = self.read_packages()
            count += 1
            print(count, err, val)
            self.worksheet.write('A' + str(count), err)
            self.worksheet.write('B' + str(count), val)
            # print(err)
        self.workbook.close()

tester = CurveMaker('COM4', 115200, rows= 9999)
tester.main()
