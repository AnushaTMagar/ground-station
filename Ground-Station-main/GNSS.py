import serial
from serial.tools.list_ports import comports
from pynmeagps import NMEAReader
import numpy as np
import time as tp

latitude_array = np.linspace(0, 0, 18)
longitude_array = np.linspace(0, 0, 18)
count = 0


class GNSS_data:
    def __init__(self):
        self.latitude = ''
        self.latitude = ''
        self.time = ''
        self.attitude = ''
        self.port_connect()

    def port_connect(self):
        self.port = comports()
        self.portlist = [port for port, desc, hwid in sorted(self.port)]
        print(self.portlist)
        self.stream = serial.Serial(self.portlist[1], 115200, timeout=5)
        tp.sleep(0.1)
        self.stream.flushInput()

    def get_gpsdata(self):
        global longitude_array, latitude_array, count
        while 1:
            try:

                nmr = NMEAReader(self.stream)
                (raw_data, parsed_data) = nmr.read()
                print("trying")
                # print(parsed_data)

                if "GGA" in parsed_data.msgID:
                    print(parsed_data)
                    altitude = parsed_data.alt
                    time = parsed_data.time.replace(microsecond=0)
                    latitude = parsed_data.lat
                    longitude = parsed_data.lon
                    numsv = parsed_data.numSV
                    # print("Time is {}".format(time))
                    # print("Latitude is {}".format(latitude, 4))
                    # print("Longitude is {}".format(longitude, 4))
                    # print("Altitude is {}".format(altitude))
                    print("No. of satellite in use is {}".format(numsv))
                    # print("---------------------------------------------------------------------------------------")
                    latitude_array[:-1] = latitude_array[1:]
                    latitude_array[-1] = float(latitude)
                    longitude_array[:-1] = longitude_array[1:]
                    longitude_array[-1] = float(longitude)
                    self.stream.flushInput()

                    #taking precison upto 1.1m,by 5 decimal digits
                    return latitude_array, longitude_array
                else:
                    if latitude_array[17] == [0]:
                        self.get_gpsdata()
                    elif count <= 2:
                        # tp.sleep(0.1)
                        count = count + 1
                        self.get_gpsdata()
                    # print("else", latitude_array, longitude_array)
                    count = 0
                    self.stream.flushInput()
                    return latitude_array, longitude_array


            except:

                pass

# if __name__=="__main__":
#     great =  GNSS_data()
#     great.get_gpsdata()
