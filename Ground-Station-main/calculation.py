import tracemalloc
import numpy as np

from communication import Communication


value_chainD = [0] * 18
# Altitude values
altitude_dataU = np.linspace(0, 0, 18) #Altitude Upper
altitude_dataL = np.linspace(0, 0, 18) #Altitude Lower
ptr1 = 0
xa_data = np.linspace(0, 0, 18)
maxAlt = 0
ignition = 0
height_a = 0
# Acceleration values
acceleration_dataUx = np.linspace(0, 0, 18)
acceleration_dataLz = np.linspace(0, 0, 18)
acceleration_dataUy = np.linspace(0, 0, 18)
acceleration_dataUz = np.linspace(0, 0, 18)
xa4_data = np.linspace(0, 0, 18)
ptr5 = 0
maxAcc = 0
# Velocity values
velocity_dataU = np.linspace(0, 0, 18)
velocity_dataL = np.linspace(0, 0, 18)
xa1_data = np.linspace(0, 0, 18)
ptr2 = 0
maxVe = 0
# Temperature values
temperature_dataU = np.linspace(0, 0, 18)
temperature_dataL = np.linspace(0, 0, 18)
xa2_data = np.linspace(0, 0, 18)
ptr3 = 0
maxTemp = 0
# Pressure values
pressure_dataU = np.linspace(0, 0, 18)
pressure_dataL = np.linspace(0, 0, 18)
xa3_data = np.linspace(0, 0, 18)
ptr4 = 0
maxPress = 0
# Vibration values
vibration_dataU = np.linspace(0, 0, 18)
vibration_dataL = np.linspace(0, 0, 18)
xa6_data = np.linspace(0, 0, 18)
ptr7 = 0
# Gyroscope values
gyro_data_x = np.linspace(0, 0, 18)
gyro_data_y = np.linspace(0, 0, 18)
gyro_dataU_z = np.linspace(0, 0, 18)
gyro_dataL_z = np.linspace(0, 0, 18)
xa5_data = np.linspace(0, 0, 18)
ptr6 = 0
# other
val = Communication()
satellite_deployment = 0
drough_parachute = 0
main_parachute = 0
touch_down = 0
liftoff = 0
value_chainL = [0] * 18
value_chainU = [0] * 18

gps_data_lat = np.linspace(0, 0, 18)
gps_data_long = np.linspace(0, 0, 18)
map_update = 0
i = 0
z = -1
x = 0
# data_keys = ['Pointer','Altitude','Temperature','Pressure','AcclerationU_x','AccelerationU_y','AccelerationU_z','GyroUx','GyroUy','GyroUz','Latitude','Longitude']
# status_keys = ['Stagelock','SecStageBurn','GPS']
big_array = {}
overall_status = {}
runtime_min, runtime_sec, runtime_hr = 0, 0, 0
tracemalloc.start()

class Calculation:
    global big_array

    def altitude_func(self,data):
        
        global altitude_dataU, altitude_dataL, ptr1, xa_data, maxAlt, ignition, height_a, drough_parachute, main_parachute, satellite_deployment
        altitude_dataU[:-1] = altitude_dataU[1:]
        altitude_dataU[-1] = float(data[10])
        # altitude_dataL[:-1] = altitude_dataL[1:]
        # altitude_dataL[-1] = float(value_chainL[10])
        ptr1 += 1
        xa_data[:-1] = xa_data[1:]
        xa_data[-1] = float(ptr1)
        return xa_data, altitude_dataU, altitude_dataL


    def temp_func(self, data):
        global temperature_dataU, temperature_dataL, ptr3, xa2_data, maxTemp
        temperature_dataU[:-1] = temperature_dataU[1:]
        temperature_dataU[-1] = float(data[8])
        # temperature_dataL[:-1] = temperature_dataL[1:]
        # temperature_dataL[-1] = float(value_chainL[8])
        # ptr3 += 1
        # xa2_data[:-1] = xa2_data[1:]
        # xa2_data[-1] = float(ptr3)
        return temperature_dataU
        # print('temperature =', temperature_data)
        # test = temperature_dataU[12]
        # if test > maxTemp:
        #     self.maxi_temp.display(test)
        #     maxTemp = test
        # else:
        #     self.maxi_temp.display(maxTemp)

    def press_func(self,data):
        global pressure_dataU, pressure_dataL, ptr4, xa3_data, maxPress
        pressure_dataU[:-1] = pressure_dataU[1:]
        pressure_dataU[-1] = float(data[9])  # find position in value chain
        # pressure_dataL[:-1] = pressure_dataL[1:]
        # pressure_dataL[-1] = float(value_chainL[9])
        # ptr4 += 1
        # xa3_data[:-1] = xa3_data[1:]
        # xa3_data[-1] = float(ptr4)
        return pressure_dataU
        # print('pressure =', pressure_data)
        # test = pressure_dataU[12]
        # if test > maxPress:
        #     self.maxi_pressure.display(test)
        #     maxPress = test
        # else:
        #     self.maxi_pressure.display(maxPress)

    def acc_func(self, data):
        global acceleration_dataUx, acceleration_dataUy, acceleration_dataUz, acceleration_dataLz, ptr5, xa4_data, maxAcc, liftoff

        acceleration_dataUx[:-1] = acceleration_dataUx[1:]
        acceleration_dataUx[-1] = float(data[2])
        acceleration_dataUy[:-1] = acceleration_dataUy[1:]
        acceleration_dataUy[-1] = float(data[3])
        acceleration_dataUz[:-1] = acceleration_dataUz[1:]
        acceleration_dataUz[-1] = float(data[4])
        # acceleration_dataLz[:-1] = acceleration_dataLz[1:]
        # acceleration_dataLz[-1] = float(value_chainL[4])
        # ptr5 += 1
        # xa4_data[:-1] = xa4_data[1:]
        # xa4_data[-1] = float(ptr5)
        return acceleration_dataUx, acceleration_dataUy, acceleration_dataUz

    def gyro_func(self, data):

        global gyro_data_x, gyro_data_y, gyro_dataU_z, gyro_dataL_z, ptr6, xa5_data

        gyro_data_x[:-1] = gyro_data_x[1:]
        gyro_data_x[-1] = float(data[5])
        gyro_data_y[:-1] = gyro_data_y[1:]
        gyro_data_y[-1] = float(data[6])
        gyro_dataU_z[:-1] = gyro_dataU_z[1:]
        gyro_dataU_z[-1] = float(data[7])
        # gyro_dataL_z[:-1] = gyro_dataL_z[1:]
        # gyro_dataL_z[-1] = float(value_chainL[7])
        # ptr6 += 1
        # xa5_data[:-1] = xa5_data[1:]
        # xa5_data[-1] = float(ptr6)
        return gyro_data_x, gyro_data_y, gyro_dataU_z

    # def vibration_func(self, value_chainU, value_chainL):
    #     global vibration_dataU, vibration_dataL, ptr7, xa6_data, map_update
    #     vibration_dataU[:-1] = vibration_dataU[1:]
    #     vibration_dataU[-1] = float(value_chainU[8])
    #     vibration_dataL[:-1] = vibration_dataL[1:]
    #     vibration_dataL[-1] = float(value_chainL[8])
    #     ptr7 += 1
    #     xa6_data[:-1] = xa6_data[1:]
    #     xa6_data[-1] = float(ptr7)
    #     return vibration_dataU, vibration_dataL


    def gps_func(self, value_chainU):
        global gps_data_lat,gps_data_long,x
        try:
            lat = float(value_chainU[0][:-8]) + float("{:.8f}".format((float(value_chainU[0][-8:])/60)))
            lon = float(value_chainU[1][:-8]) + float("{:.8f}".format((float(value_chainU[1][-8:])/60)))
            x = 1
        except:
            lon = 86.04890050
            lat = 26.9007483
            x = 0
        gps_data_lat[:-1] = gps_data_lat[1:]
        gps_data_lat[-1] = lat
        gps_data_long[:-1] = gps_data_long[1:]
        gps_data_long[-1] = lon
    

        return gps_data_long,gps_data_lat, x

    def progress_bar(self, value_chainU, value_chainL):
        if int(value_chainU[1]) == 1294:  # SET VALUE
            self.ignition.setStyleSheet("QProgressBar"
                                        "{"
                                        "background-color : rgb(0, 0, 0);"
                                        "border : 1px"
                                        "}"

                                        "QProgressBar::chunk"
                                        "{"
                                        "background : rgb(100, 50,0);"
                                        "}"
                                        )
        else:
            self.ignition.setStyleSheet("QProgressBar"
                                        "{"
                                        "background-color : rgb(0, 0, 0);"
                                        "border : 1px"
                                        "}"

                                        "QProgressBar::chunk"
                                        "{"
                                        "background : rgb(0, 0,0);"
                                        "}"
                                        )

        self.Maxheight.setStyleSheet("QProgressBar"
                                     "{"
                                     "background-color : rgb(0, 0, 0);"
                                     "border : 1px"
                                     "}"
                                     "QProgressBar::chunk"
                                     "{"
                                     "background : rgb(0, 0,0);"
                                     "}"
                                     )



    def update_graph(self):
        value_chain = val.getData()
        value_chainL = value_chain[0]  # change it while testing
        value_chainU = value_chain[0]
        gps_data_lat[:-1] = gps_data_lat[1:]
        gps_data_lat[-1] = float(value_chainU[8])
        gps_data_long[:-1] = gps_data_long[1:]
        gps_data_long[-1] = float(value_chainL[9])

    def all_func(self):
        global gps_array, big_array
        data,status = val.getData()
        
        # value_chainL = value_chain[0]  # change it while testing
        
        # value_chainU = value_chain[0] # change it while testing

        # ###############################turn it on for actual testing###################
        # if value_chain[0] == 'L':
        #     value_chainL = value_chain
        #     # print('from main', value_chainL)
        # elif value_chain[0] == 'U':
        #     value_chainU = value_chain
        #     print('from main', value_chainU)
        #
        # if len(value_chain) <= 18:
        #     value_chainL = value_chainU
        # if value_chain[0] != 'L' and value_chain[0] != 'U':
        #     gps_array = value_chain
        big_array.clear()
        overall_status.clear()
        # big_array = dict.fromkeys(data_keys)
        # overall_status = dict.fromkeys(status_keys)
        
        altitude = self.altitude_func(data)
        big_array['Pointer'] = altitude[0]
        big_array['Altitude'] = altitude[1]
        big_array['Voltage'] = data[11]
        # big_array['AltitudeL'] = altitude[2]
        
    
        big_array['Temperature'] = self.temp_func(data)
        # big_array['Temperature'] = temperature[1]

       
        big_array['Pressure'] =  self.press_func(data)
        # big_array['PressureU'] = pressure[1]

        acceleration = self.acc_func(data)
        big_array['Acceleration_x'] = acceleration[0]
        big_array['Acceleration_y'] = acceleration[1]
        big_array['Acceleration_z'] = acceleration[2]
        # big_array['AccelerationLz'] = acceleration[3]

        gyro = self.gyro_func(data)
        big_array['Gyro_x'] = gyro[0]
        big_array['Gyro_y'] = gyro[1]
        big_array['Gyro_z'] = gyro[2]
        # big_array['GyroLz'] = gyro[3]

        # vibration = self.vibration_func(data)
        # big_array['VibrationU'] = vibration[0]
        # big_array['VibrationL'] = vibration[1]

        gps = self.gps_func(data)
        big_array['Longitude'] = gps[0]
        big_array['Latitude'] = gps[1]
        overall_status['GPS'] = gps[2]

        overall_status['Stagelock'] = status[0]
        overall_status['SecStageBurn'] = status[1]
        try:
            overall_status['Rflink'] = status[2]
        except:
            overall_status['Rflink'] = 0
        return big_array,overall_status
        # self.progress_bar(value_chainU, value_chainL)
        # self.add_marker(value_chainU, value_chainL)
        # self.run_time()
        # data_base.guardar(value_chain)
if __name__=="__main__":
    great = Calculation()
    great.all_func()
