from cProfile import label
import io
import math
import folium
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor,QPixmap,QTransform
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.uic import loadUi
from jinja2 import Template
import calculation
import communication
import zoomed_map

com = communication.Communication()
calc = calculation.Calculation()
z = 0
zo = 0
maxAlt = 0
maxTemp = 0
maxPress = 0
maxAcc = 0
runtime_min, runtime_sec, runtime_hr = 0, 0, 0
seconday_map_window = 0

DEFAULT_STYLE1 = """QFrame{ border-radius:55px; background-color:qconicalgradient(cx:0.5, cy:0.5, 
           angle:90.0, stop:0 rgba(5, 3, 65, 255), stop:{STOP_1} rgba(5, 3, 65, 255), stop:{STOP_2} rgba(0, 0, 0, 
           0));} """

class Main_UI(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        loadUi("UI_V3.ui", self)
        self.textBrowser.append("Port Connection Successful")
        self.latitude_lcd.setDigitCount(11)
        self.longitude_lcd.setDigitCount(11)
        self.altitude_lcd.setDigitCount(7)
        self.Max_Altitude.setDigitCount(7)
        self.Max_Pressure.setDigitCount(7)
        self.pressure_lcd.setDigitCount(7)
        # value_chain = com.getData()
        self.textBrowser.setTextColor(QColor(0, 0, 0)) 
        self.system_check.setStyleSheet(DEFAULT_STYLE)
        self.ignition.setStyleSheet(DEFAULT_STYLE)
        self.liftoff.setStyleSheet(DEFAULT_STYLE)
        self.stage_seperation.setStyleSheet(DEFAULT_STYLE)
        self.rcs_fire.setStyleSheet(DEFAULT_STYLE)
        self.system_all_good.setStyleSheet(DEFAULT_STYLE)
        self.launch_success.setStyleSheet(DEFAULT_STYLE)
        layout = QVBoxLayout(self.frame)
        self.setLayout(layout)
        big_array, overall = calc.all_func()

        coordinate = (big_array['Latitude'][17], big_array['Longitude'][17])
        self.map = folium.Map(
            tiles='http://mt1.google.com/vt/lyrs=s&h1=p1Z&x={x}&y={y}&z={z}',
            name='real',
            zoom_start=19,
            attr='Google Map',
            location=coordinate,
            zoom_control=False,
            scrollWheelZoom=False,
            dragging=False
        )
        # folium.raster_layers.TileLayer(
        #     tiles='http://mt1.google.com/vt/lyrs=m&h1=p1Z&x={x}&y={y}&z={z}',
        #     name='Standard ',
        #     attr='Google Map',
        # ).add_to(self.map)
        #
        # folium.raster_layers.TileLayer(
        #     tiles='http://mt1.google.com/vt/lyrs=y&h1=p1Z&x={x}&y={y}&z={z}',
        #     name='Combined',
        #     attr='Google Map',
        # ).add_to(self.map)
        # folium.LayerControl().add_to(self.map)

        # save map data to data object
        data = io.BytesIO()
        folium.Marker(
            location=[big_array['Latitude'][17],  big_array['Longitude'][17]],
                   ).add_to(self.map)
        self.map.save(data, close_file=False)
        self.map_view = QWebEngineView()
        self.map_view.setHtml(data.getvalue().decode())
        layout.addWidget(self.map_view)
        self.function()
        self.plot_thread()

    def altitude_plot(self):
        global maxAlt
        self.mplWidget.canvas.ax1.cla()
        self.mplWidget.canvas.ax1.grid(color='w', linestyle='-', linewidth=0.1)
        self.mplWidget.canvas.ax1.plot(self.big_array['Pointer'], self.big_array['Altitude'], c="orange")
        # self.mplWidget.canvas.ax1.plot(self.self.big_array['Pointer'], self.self.big_array['AltitudeL'], c="blue")
        self.altitude_lcd.display(self.big_array['Altitude'][17])
        self.pressure_lcd.display(self.big_array['Pressure'][17])
        test = self.big_array['Altitude'][17]
        if test > maxAlt:
            self.Max_Altitude.display(test)
            maxAlt = test
        else:
            self.Max_Altitude.display(maxAlt)
        if self.big_array['Altitude'][17] > 250:
            self.system_check.setStyleSheet(COMPLETED_STYLE)
        elif self.big_array['Altitude'][17] >= 200:
            self.system_check.setStyleSheet(NOTGOOD_STYLE)

    # def vibration_plot(self):
        # self.mplWidget.canvas.ax2.cla()
        # self.mplWidget.canvas.ax2.grid(color='w', linestyle='-', linewidth=0.1)
        # self.mplWidget.canvas.ax2.plot(self.self.big_array['Pointer'], self.self.big_array['VibrationU'], c="green")  # upper only

    def temperature_plot(self):
        global maxTemp
        self.mplWidget.canvas.ax3.cla()
        self.mplWidget.canvas.ax3.grid(color='w', linestyle='-', linewidth=0.1)
        self.mplWidget.canvas.ax3.plot(self.big_array['Pointer'], self.big_array['Temperature'], c="orange")  # upper only
        self.Temperature_lcd.display('{:.02f}'.format(self.big_array['Temperature'][17]))
        test = self.big_array['Temperature'][17]
        if test > maxTemp:
            self.Max_Temperature.display('{:.02f}'.format(test))
            maxTemp = test
        else:
            self.Max_Temperature.display('{:.02f}'.format(maxTemp))

    def pressure_plot(self):
        global maxPress
        self.mplWidget.canvas.ax4.cla()
        self.mplWidget.canvas.ax4.grid(color='w', linestyle='-', linewidth=0.1)
        self.mplWidget.canvas.ax4.plot(self.big_array['Pointer'], self.big_array["Pressure"], c="yellow")
        test =  self.big_array["Pressure"][17]
        if test > maxPress:
            self.Max_Pressure.display(test)
            maxPress = test
        else:
            self.Max_Pressure.display(maxPress)

    def acceleration_plot(self):
        global maxAcc
        self.mplWidget.canvas.ax5.cla()
        self.mplWidget.canvas.ax5.grid(color='w', linestyle='-', linewidth=0.1)
        self.mplWidget.canvas.ax5.plot(self.big_array['Pointer'], self.big_array['Acceleration_x'])  # upper only x
        self.mplWidget.canvas.ax5.plot(self.big_array['Pointer'], self.big_array['Acceleration_y'])  # y
        self.mplWidget.canvas.ax5.plot(self.big_array['Pointer'], self.big_array['Acceleration_z'])  # z
        self.mplWidget.canvas.ax5.legend(['x', 'y','z'])
        test = self.big_array['Acceleration_z'][17]
        if test > maxAcc:
            self.Max_Acceleration.display('{:.02f}'.format(test))
            maxAcc = test
        else:
            self.Max_Acceleration.display(maxAcc)
    
    def gyro_plot(self):
        self.mplWidget.canvas.ax2.cla()
        self.mplWidget.canvas.ax2.grid(color='w', linestyle='-', linewidth=0.1)
        self.mplWidget.canvas.ax2.plot(self.big_array['Pointer'],  self.big_array['Gyro_x'])  # upper only x
        self.mplWidget.canvas.ax2.plot(self.big_array['Pointer'], self.big_array['Gyro_y'])  # y
        self.mplWidget.canvas.ax2.plot(self.big_array['Pointer'], self.big_array['Gyro_z'])  # z
        roll_angle = 180 * math.atan(self.big_array['Acceleration_y'][17] / math.sqrt(
                self.big_array['Acceleration_x'][17] * self.big_array['Acceleration_x'][17] + self.big_array['Acceleration_z'][17] *
                self.big_array['Acceleration_z'][17])) / math.pi
            # pixmap = Image.open("bottom_view.png")
        # print("roll_angle",roll_angle)
        image = QPixmap("bottom_view.png")
            # angle should be changed according to the gyro data
            # roll,pitch and yaw also depends on how the avionics is placed
            # if vertical, change in y-axis gives roll
        t = QTransform()
        t.rotate(roll_angle)
        rotated_pixmap = image.transformed(t)
        rotated_pixmap = rotated_pixmap.scaled(300, 300)
            # rotate_img = pixmap.rotate(angle)
            # rotate_img.save("bottom_view.png")
            # rotate_img = ImageQt(rotate_img)
            # self.photo.setPixmap(QPixmap.transformed(rotate_img))
        self.photo.setPixmap(QPixmap(rotated_pixmap))
            # pixmap = pixmap.transformed(self.PyQt5.QtGui.QTransform().rotate(angle))

    def lat_altitude_plot(self):
        self.mplWidget.canvas.ax_3d.cla()
        self.mplWidget.canvas.ax2.grid(color='w', linestyle='-', linewidth=0.1)
        self.mplWidget.canvas.ax_3d.scatter(self.big_array['Latitude'], self.big_array['Longitude'], self.big_array['Altitude'],
                                                c="black")

    def status_display(self,bigarray,overall):
        self.voltage.display(bigarray['Voltage'])

        if (overall['Rflink'] == 1 and overall['GPS'] == 1):
            self.gps.setStyleSheet("background-color:rgb(85, 255, 0);qproperty-alignment: AlignCenter;")
        else:
            self.gps.setStyleSheet("background-color:rgb(255, 0, 0);qproperty-alignment: AlignCenter;")
        
        if overall['Stagelock'] == 1:
            self.stagelock.setStyleSheet("background-color:rgb(85, 255, 0);qproperty-alignment: AlignCenter;")
        else:
            self.stagelock.setStyleSheet("background-color:rgb(255, 0, 0);qproperty-alignment: AlignCenter;")
        
        if overall['SecStageBurn'] == 1:
            self.secstageburn.setStyleSheet("background-color:rgb(85, 255, 0);qproperty-alignment: AlignCenter;")
        else:
            self.secstageburn.setStyleSheet("background-color:rgb(255, 0, 0);qproperty-alignment: AlignCenter;")
        
        if overall['Rflink'] == 1:
            self.rflink.setStyleSheet("background-color:rgb(85, 255, 0);qproperty-alignment: AlignCenter;")
        else:
            self.rflink.setStyleSheet("background-color:rgb(255, 0, 0);qproperty-alignment: AlignCenter;")

        if ((overall['Rflink'] == 1) and (bigarray['Acceleration_z'][17] is not None)):
            self.imu.setStyleSheet("background-color:rgb(85, 255, 0);qproperty-alignment: AlignCenter;")
        else:
            self.imu.setStyleSheet("background-color:rgb(255, 0, 0);qproperty-alignment: AlignCenter;")

        if ((overall['Rflink'] == 1) and (bigarray['Altitude'][17] is not None)):
            self.bmp.setStyleSheet("background-color:rgb(85, 255, 0);qproperty-alignment: AlignCenter;")
        else:
            self.bmp.setStyleSheet("background-color:rgb(255, 0, 0);qproperty-alignment: AlignCenter;")
        


    
    def plot_matplot(self):
        global z, seconday_map_window, altitude_value, maxAlt, maxTemp, maxPress, maxAcc
        self.big_array,self.overall = calc.all_func()
        # print(self.big_array)

 


        # self.run_time()
        if seconday_map_window == 0:  # donot run primary window if zoomed_map is open

            self.altitude_plot()
            # self.vibration_plot()
            self.temperature_plot()
            self.pressure_plot()
            self.acceleration_plot()
            self.gyro_plot()
            self.lat_altitude_plot()

            self.status_display(self.big_array,self.overall)

            


            self.latitude_lcd.display('{:0.4f}'.format(self.big_array['Latitude'][17]))
            self.longitude_lcd.display('{:0.4f}'.format(self.big_array['Longitude'][17]))

            self.mplWidget.canvas.draw()
            self.add_marker(self.big_array['Latitude'],self.big_array['Longitude'])
            # self.textBrowser.append(str(gps_value))

            # flight status meaning ignition , liftoff or any other state
            self.textBrowser_2.append(str("Latest flight status is shown here"))
            self.textBrowser_2.append(str(z))
            temperature_progress = self.big_array['Pointer']
            progress = (100 - temperature_progress[17]) / 100.0
            # print(progress)
            STOP_1 = str(progress)
            STOP_2 = str(progress)
            if progress < 0:
                progress = 0
            styleSheet = DEFAULT_STYLE1.replace("{STOP_1}", str(progress - 0.001)).replace("{STOP_2}", str(progress))
            self.temperature_visual.setStyleSheet(styleSheet)
            self.textBrowser.verticalScrollBar().maximum()
            temperature_progress = self.big_array['Temperature']
            progress = (100 - temperature_progress[17]) / 100.0
            # print(progress)
            STOP_1 = str(progress)
            STOP_2 = str(progress)
            if progress < 0:
                progress = 0
            styleSheet_1 = DEFAULT_STYLE1.replace("{STOP_1}", str(progress - 0.001)).replace("{STOP_2}", str(progress))
            self.temperature_visual_1.setStyleSheet(styleSheet_1)

        else:
            return self.big_array['Latitude'],self.big_array['Longitude']

    def plot_thread(self):
        self.plot_matplot()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(400)
        self.timer.timeout.connect(self.plot_matplot)
        self.timer.start()
        self.run_time()

    def add_marker(self, lat, lon):
        global z
        z = z + 1
        if z == 0:
            js = Template(
                """
            L.circleMarker(
                [{{latitude}}, {{longitude}}], {
                    "bubblingMouseEvents": true,
                    "color": "red",
                    "dashArray": null,
                    "dashOffset": null,
                    "fill": false,
                    "fillColor": "#3388ff",
                    "fillOpacity": 0.2,
                    "fillRule": "evenodd",
                    "lineCap": "round",
                    "lineJoin": "round",
                    "opacity": 1.0,
                    "radius": 0.1,
                    "stroke": true,
                    "weight": 5
                }
            ).addTo({{map}});
            """
            ).render(map=self.map.get_name(), latitude=lat[17], longitude=lon[17])
            self.map_view.page().runJavaScript(js)

        if z == 1:
            js = Template(
                """
            L.circleMarker(
                [{{latitude}}, {{longitude}}], {
                    "bubblingMouseEvents": true,
                    "color": "yellow",
                    "dashArray": null,
                    "dashOffset": null,
                    "fill": false,
                    "fillColor": "#3388ff",
                    "fillOpacity": 0.2,
                    "fillRule": "evenodd",
                    "lineCap": "round",
                    "lineJoin": "round",
                    "opacity": 1.0,
                    "radius": 0.1,
                    "stroke": true,
                    "weight": 5
                }
            ).addTo({{map}});
            """
            ).render(map=self.map.get_name(), latitude=lat[17], longitude=lon[17])
            self.map_view.page().runJavaScript(js)
            z = -1

    def function(self):
        self.map_button.setStyleSheet("background-color : #005500")
        self.wifi.setStyleSheet("background-color : #005500")
        self.record_button.setStyleSheet("background-color :#a60000")
        self.gps_connection.setStyleSheet("background-color : #005500")
        self.minimize_button.clicked.connect(self.minimize_window)
        # self.maximize_button.clicked.connect(self.maximize_window)
        self.close_button.clicked.connect(self.close_window)
        self.map_button.clicked.connect(self.show_map_window)

    def show_map_window(self, checked):
        global seconday_map_window
        seconday_map_window = 1
        self.close()
        self.w = zoomed_map.Map_UI()
        self.w.show()
        # self.close()

    def minimize_window(self):
        self.showMinimized()

    def close_window(self):
        global seconday_map_window
        seconday_map_window = 0
        QtCore.QCoreApplication.instance().quit()

    def run_time(self):
        global runtime_min, runtime_sec, runtime_hr
        runtime_sec = runtime_sec + 1
        self.second_lcd.display(runtime_sec)
        if runtime_sec == 59:
            runtime_sec = 0
            runtime_min = runtime_min + 1
            self.minute_lcd.display(runtime_min)
            if runtime_min == 59:
                runtime_min = 0
                runtime_hr = runtime_hr + 1
                self.hour_lcd.display(runtime_hr)


DEFAULT_STYLE = """
QProgressBar{
    background-color :rgb(0,0,0);
    border-radius: 10px;
}

QProgressBar::chunk {
    background : rgb(29, 185, 84);;
    width: 10px;
    margin: 1px;
}
"""

COMPLETED_STYLE = """
QProgressBar{
    background-color :rgb(29, 185, 84);
    border-radius: 10px;
}

QProgressBar::chunk {
    background : rgb(29, 185, 84);;
    width: 10px;
    margin: 1px;
}
"""

NOTGOOD_STYLE = """
QProgressBar{
    background-color :YELLOW;
    border-radius: 10px;
}

QProgressBar::chunk {
    background : rgb(29, 185, 84);;
    width: 10px;
    margin: 1px;
}
"""

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Main_UI()
    window.show()
    app.exec_()