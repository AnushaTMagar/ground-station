import io
from jinja2 import Template
import folium
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import calculation
import main


calc = calculation.Calculation()
z = 0


class Map_UI(QtWidgets.QMainWindow):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        loadUi("map.ui", self)
        # value_chain = com.getData()
        layout = QVBoxLayout(self.frame)
        self.setLayout(layout)
        big_data_array = calc.all_func()
        latitude = big_data_array['Latitude']
        longitude = big_data_array['Longitude']
        coordinate = (latitude[17], longitude[17])
        self.map = folium.Map(
            tiles='http://mt1.google.com/vt/lyrs=m&h1=p1Z&x={x}&y={y}&z={z}',
            name='real',
            zoom_start=19,
            max_zoom=20,
            attr='Google Map',
            location=coordinate,

        )
        # save map data to data object
        data = io.BytesIO()
        self.map.save(data, close_file=False)
        self.map_view = QWebEngineView()
        self.map_view.setHtml(data.getvalue().decode())
        layout.addWidget(self.map_view)
        self.minimize_button.clicked.connect(self.minimize_window)
        self.close_button.clicked.connect(self.close_window)
        self.go_loop = main.Main_UI()
        self.plot_thread()
        self.go_loop.show()
        

    def minimize_window(self):
        self.showMinimized()

    def maximize_window(self):
        self.showMaximized()

    def close_window(self):
        self.go_loop = main.Main_UI()
        self.close()
        self.go_loop.show()
        self.go_loop.plot_thread()

    def add_marker(self):
        global z
        big_data_array = calc.all_func()
        self.map.fit_bounds(self.map.get_bounds(), padding=(10, 10))
        latitude = big_data_array['Latitude']
        longitude = big_data_array['Longitude']
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
            ).render(map=self.map.get_name(), latitude=latitude[17], longitude=longitude[17])
            self.map_view.page().runJavaScript(js)
        if z == 1:
            js = Template(
                """
            L.circleMarker(
                [{{latitude}}, {{longitude}}], {
                    "bubblingMouseEvents": true,
                    "color": "blue",
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
            ).render(map=self.map.get_name(), latitude=latitude[17], longitude=longitude[17])
            self.map_view.page().runJavaScript(js)
        if z == 2:
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
            ).render(map=self.map.get_name(), latitude=latitude[17], longitude=longitude[17])
            self.map_view.page().runJavaScript(js)
            z = -1

    def plot_thread(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.add_marker)
        self.timer.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Map_UI()
    window.show()
    app.exec_()
