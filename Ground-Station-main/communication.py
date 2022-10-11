
from serial.tools.list_ports import comports
import serial
import time
import csv


class Communication:
    portName = ''
    dummyPlug = False
    ports = serial.tools.list_ports.comports()

    ser = serial.Serial()

    def __init__(self):
        
        self.tempdata = None
        self.port = comports()
        self.portlist = [port for port, desc, hwid in sorted(self.port)]
        if serial.Serial() is not open:
            try:
                self.ser = serial.Serial(self.portlist[0], 115200,timeout = None)
                self.ser.flushInput()
                # self.ser.write("get")
                # sleep(1) for 100 millisecond delay
                # 100ms dely
                time.sleep(.1)
            except serial.serialutil.SerialException:
                print("Can't open : ", self.portlist[0])
                self.dummyPlug = True
                print("Retrying")
        else:
            print("error")

    def latest_data(self):
        try:
            local_data = self.ser.readline() 
            print(local_data)
            local_data = local_data.decode("utf-8")[1:-3].split(',')
            print(local_data)
            print(len(local_data))
            if (len(local_data) == 14):
                self.tempdata = local_data
                self.tempdata.append(1)
                self.ser.flushInput()
                return self.tempdata
    


            if (len(local_data)>14):
                print('Ya k')
                local_data = local_data[-12:]
                local_data.insert(0,'0.00')
                local_data.insert(1,'0.00')
                local_data.append(1)
                print(local_data)
                return local_data

            else:
                print(self.tempstatus)
                self.tempdata.pop()
                self.tempdata.append(0)
                self.ser.flushInput()
                return self.tempdata
        except:
            self.tempdata.pop()
            self.tempdata.append(0)
            return self.tempdata



    def getData(self):
        total_data  = self.latest_data()
        print('_____________________________________________________________')
        print(total_data)
        print("_______________________________________________________")
        with open("flight_data2.csv", "a") as f:
            
            writer = csv.writer(f)
            writer.writerow(total_data)

        data = total_data[:-3]
        status = total_data [-3:]
        print("-------------------------------------------------------------------")
        print(status)
        print(data)
        print('------------------------------------------------------------------------------')

        return data, status

        

    def isOpen(self):
        return self.ser.isOpen()