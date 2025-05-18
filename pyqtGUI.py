import io
import sys
import os
import json
import time
import folium

import retrieveJSON
# from PyQt5 import QtWidgets, QtWebEngineWidgets, QtGui
# # from PyQt5 import QtWidgets, QtWebEngineWidgets, QtGui

# from PyQt5.QtWidgets import QMainWindow
# from qtconsole import QtCore
# from PyQt5.QtCore import QtCore


from PySide6 import QtWidgets, QtWebEngineWidgets, QtGui
from PySide6.QtWidgets import QMainWindow
from PySide6 import QtCore
from PySide6.QtCore import QSize

# from PySide6.QtCore import QSize  # Correct import for PySide6
from collections import OrderedDict
from Dijkstra import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set PyQt window size
        self.pathLabel = QtWidgets.QLabel()
        self.transPathLabel = QtWidgets.QLabel()
        self.destinationLabel = QtWidgets.QLabel()
        self.sourceLabel = QtWidgets.QLabel()
        self.destinationDDL = QtWidgets.QComboBox()
        self.sourceDDL = QtWidgets.QComboBox()
        self.busPathDDL = QtWidgets.QComboBox()
        self.title = "Group P2-6 ICT 1008 PROJECT"
        self.left = 200
        self.top = 100
        self.width = 1800
        self.height = 950

        self.initWindow()

    def initWindow(self):
        # set window title
        self.setWindowTitle(self.title)
        # set window geometry
        # self.setGeometry(self.left, self.top, self.width, self.height)
        # Disable PyQt 5 application from resizing
        self.setFixedSize(self.width, self.height)
        self.guiSettings()
        self.show()

    def guiSettings(self):
        # "Select Path" Label
        self.pathLabel.setText("Select Paths:")
        self.pathLabel.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        self.pathLabel.setFixedSize(200, 30)

        # Creating Buttons for the different paths
        walkingPathButton = QtWidgets.QPushButton("Walking Path")
        walkingPathButton.setFont(QtGui.QFont("Arial", 13, QtGui.QFont.Bold))
        walkingPathButton.setFixedSize(150, 80)
        walkingPathButton.setIcon(QtGui.QIcon("image/walk.png"))
        walkingPathButton.setIconSize(QtCore.QSize(30, 30))
        walkingPathButton.clicked.connect(self.generateWalkingPath)

        busPathButton = QtWidgets.QPushButton("Bus path")
        busPathButton.setFont(QtGui.QFont("Arial", 13, QtGui.QFont.Bold))
        busPathButton.setIcon(QtGui.QIcon("image/bus.png"))
        busPathButton.setFixedSize(150, 80)
        busPathButton.setIconSize(QtCore.QSize(30, 30))
        busPathButton.clicked.connect(self.generateBusPath)

        mrtPathButton = QtWidgets.QPushButton("Mrt path")
        mrtPathButton.setFont(QtGui.QFont("Arial", 13, QtGui.QFont.Bold))
        mrtPathButton.setIcon(QtGui.QIcon("image/mrt.png"))
        mrtPathButton.setFixedSize(150, 80)
        # mrtPathButton.setIconSize(QtCore.QSize(30, 30))
        # mrtPathButton.setIconSize(QtWidgets.QSize(30, 30))
        mrtPathButton.setIconSize(QSize(30, 30))


        mrtPathButton.clicked.connect(self.generateMrtPath)

        # "View Transport Service Paths" label
        self.transPathLabel.setText("View Transport Service Paths:")
        self.transPathLabel.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        self.transPathLabel.setFixedSize(200, 30)

        # Creating button for side feature to show bus service route
        showBusPathButton = QtWidgets.QPushButton("Bus Service Path")
        showBusPathButton.setFont(QtGui.QFont("Arial", 13, QtGui.QFont.Bold))
        showBusPathButton.setIcon(QtGui.QIcon("image/bus.png"))
        showBusPathButton.setFixedSize(180, 70)
        showBusPathButton.clicked.connect(self.generateBusServicePath)

#######################################################################################################################

        # Source Label
        self.sourceLabel.setText("SELECT SOURCE")
        self.sourceLabel.setFont(QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        self.sourceLabel.setFixedSize(200, 30)

        # Destination Label
        self.destinationLabel.setText("SELECT DESTINATION")
        self.destinationLabel.setFont(
            QtGui.QFont("Arial", 11, QtGui.QFont.Bold))
        self.destinationLabel.setFixedSize(200, 30)

        # Retrieve names from json file (Drop Down List)
        for feature_data in retrieveJSON.retrieveBuilding():
            buildingName = feature_data['properties']
            if 'name' in buildingName:
                retrieveHDB = buildingName['name']
                self.sourceDDL.addItem(retrieveHDB)
                self.destinationDDL.addItem(retrieveHDB)

        # Set font size
        self.sourceDDL.setFixedSize(250, 70)
        self.sourceDDL.setFont(QtGui.QFont("Arial", 13))

        self.destinationDDL.setFixedSize(250, 70)
        self.destinationDDL.setFont(QtGui.QFont("Arial", 13))

        # Retrieve names from json file (Drop Down List)
        for bus_data in retrieveJSON.retrieveBusService():
            bus_name = bus_data['properties']
            if 'name' in bus_name:
                retrieveBus = bus_name['name']
                self.busPathDDL.addItem(retrieveBus)

        self.busPathDDL.setFixedSize(180, 70)
        self.busPathDDL.setFont(QtGui.QFont("Arial", 13))

#######################################################################################################################

        self.view = QtWebEngineWidgets.QWebEngineView()
        # set margin for the map (left, top, right, down)
        self.view.setContentsMargins(5, 10, 10, 5)

        # Creating Folium Map
        self.m = folium.Map(
            location=[1.400150, 103.910172], titles="Punggol", zoom_start=17)
        nodeData = os.path.join('exportBuilding.geojson')

        # Setting popup for each individual building and display the name
        geo_json = folium.GeoJson(
            nodeData, popup=folium.GeoJsonPopup(fields=['name']))
        geo_json.add_to(self.m)
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.view.setHtml(data.getvalue().decode())

        # PyQt Horizontal Box layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        lay = QtWidgets.QHBoxLayout(central_widget)

        # Create vertical layout container to contains all buttons, label, combobox, etc.
        controller_container = QtWidgets.QWidget()
        vlay = QtWidgets.QVBoxLayout(controller_container)
        vlay.addWidget(self.sourceLabel)
        vlay.addWidget(self.sourceDDL)
        vlay.addWidget(self.destinationLabel)
        vlay.addWidget(self.destinationDDL)
        vlay.addWidget(self.pathLabel)
        vlay.addWidget(walkingPathButton)
        vlay.addWidget(busPathButton)
        vlay.addWidget(mrtPathButton)
        vlay.addStretch()
        vlay.addWidget(self.transPathLabel)
        vlay.addWidget(self.busPathDDL)
        vlay.addWidget(showBusPathButton)
        vlay.addStretch()

        lay.addWidget(controller_container)
        lay.addWidget(self.view, stretch=1)

#######################################################################################################################

    # Walking Path Function
    def generateWalkingPath(self):
        run_time = time.time()

        # Initializing the default map
        self.m = folium.Map(location=[1.400150, 103.910172], zoom_start=17)
        nodeData = os.path.join('exportBuilding.geojson')
        geo_json = folium.GeoJson(
            nodeData, popup=folium.GeoJsonPopup(fields=['name']))
        geo_json.add_to(self.m)
        src = self.sourceDDL.currentText()
        dest = self.destinationDDL.currentText()

        nodes = {}
        for feature_data in retrieveJSON.retrieveBuilding():
            buildingName = feature_data['properties']
            if 'name' in buildingName:
                retrieveHDB = buildingName['name']
                # Find the middle point in the list of coordinates (see exportBuilding.geojson)
                nodes[retrieveHDB] = find_midpoint(
                    feature_data['geometry']['coordinates'])

        pathfinder = Dijkstra(nodes)
        pathfinder.create_edges()
        graph = pathfinder.build_graph()
        path = pathfinder.find_shortest_path(graph, src, dest)

        # Plot the walking path on the map
        folium.PolyLine(path, opacity=1, color='red').add_to(self.m)
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.view.setHtml(data.getvalue().decode())

        print("----------------- Run Time ------------------")
        print("%s seconds" % (time.time() - run_time))
        print("")

#######################################################################################################################

    # Mrt Path Function
    def generateMrtPath(self):
        run_time = time.time()

        # initiliase GUI map
        self.m = folium.Map(location=[1.400150, 103.910172], zoom_start=17)
        nodeData = os.path.join('exportBuilding.geojson')
        geo_json = folium.GeoJson(nodeData, popup=folium.GeoJsonPopup(fields=['name']))
        geo_json.add_to(self.m)
        src = self.sourceDDL.currentText()
        dest = self.destinationDDL.currentText()

        nodes = OrderedDict()
        edges = []
        mrtPath = []
        mrtRoutes = OrderedDict()  # containing routes
        mrtNodes = {}  # used for reverse finding
        temp = {}  # used for reverse finding of routes

        # get all the names of geojson files for mrt routes
        filedir = "MRT ROUTES\\"
        json_files = [pos_json for pos_json in os.listdir(filedir) if pos_json.endswith('.geojson')]

        for f in json_files:

            # load the mrt routes geojson file
            with open(filedir + f) as json_file:
                data = json.load(json_file)

            for feature in data['features']:

                # if the first item is a multilinestring, AKA mrt route , then add it to a list called mrtpath
                if feature['geometry']['type'] == 'LineString':
                    for y in feature['geometry']['coordinates']:
                        mrtPath.append(y)
                else:
                    # else it is a lrt node

                    # step1 : find the midpoint of the polygon
                    coord = find_midpoint(feature['geometry']['coordinates'])
                    # step2 :add the lrt node into the dictionary of nodes. k = name , v =coordinates
                    nodes[feature['id']] = coord  #
                    mrtNodes[tuple(coord)] = feature['id']  # mrtNodes is reverse find , k=coordinates, v =name

                    # step 3: add the coordinates of the lrt node together with path.
                    # This is necessary because the data set does not link the nodes and routes
                    lowest = 999
                    lowestIndex = 0

                    # loops through the coordinates of the mrtpath
                    for i in range(len(mrtPath)):

                        # find the shortest distance between the current lrt nodes and the path.
                        # The shortest distance means that the mrt belongs in behind that coordinate
                        d = calc_distance(coord, mrtPath[i])
                        if d < lowest:
                            lowest = d
                            lowestIndex = i
                    mrtPath.insert(lowestIndex, coord)  # insert the mrt node's coordinate into the mrtpath

            length = len(mrtPath)
            for i in range(length):
                c = tuple(mrtPath[i])
                k = str(i)
                # key = i(a name for mrt path coordinates)
                # value = coordinates
                mrtRoutes[k] = c
                temp[c] = k  # for reverse finding path coordinates to get name

            # creating edges for lrt
            for i in range(length):
                if i + 1 != length:
                    d = calc_distance(mrtPath[i], mrtPath[i + 1])
                    # if the coordinates of the mrtpath is a lrt , then the next coordinate is a path
                    if tuple(mrtPath[i]) in mrtNodes:
                        edges.append((mrtNodes[tuple(mrtPath[i])], temp[tuple(mrtPath[i + 1])], d / 30, "LRT"))

                    # else if the next coordinates of the mrtpath is a lrt, then the current coordinate is a path
                    elif tuple(mrtPath[i + 1]) in mrtNodes:
                        edges.append((temp[tuple(mrtPath[i])], mrtNodes[tuple(mrtPath[i + 1])], d / 30, "LRT"))
                    else:
                        # else both are mrt path
                        edges.append((temp[tuple(mrtPath[i])], temp[tuple(mrtPath[i + 1])], d / 30, "LRT"))

            temp.clear()
            mrtPath.clear()

        # initialise hdb nodes
        for feature_data in retrieveJSON.retrieveBuilding():
            buildingName = feature_data['properties']
            if 'name' in buildingName:
                retrieveHDB = buildingName['name']
                nodes[retrieveHDB] = find_midpoint(feature_data['geometry']['coordinates'])

        pathfinder = Dijkstra(nodes)  # parse in the nodes of hdb and lrt
        pathfinder.create_edges()  # create edges
        pathfinder.create_mrt_edgenodes(edges, mrtNodes, mrtRoutes)  # create mrt edges
        graph = pathfinder.build_MRTgraph()

        path = pathfinder.find_shortest_path(graph, src, dest)
        folium.PolyLine(path, opacity=1, color='red').add_to(self.m)
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.view.setHtml(data.getvalue().decode())

        print("----------------- Run Time ------------------")
        print("%s seconds" % (time.time() - run_time))
        print("")

#######################################################################################################################

    # Bus Path Function
    def generateBusPath(self):
        run_time = time.time()

        # initiliase GUI map
        self.m = folium.Map(
            location=[1.400150, 103.910172], zoom_start=17)
        nodeData = os.path.join('exportBuilding.geojson')
        geo_json = folium.GeoJson(nodeData, popup=folium.GeoJsonPopup(fields=['name']))
        geo_json.add_to(self.m)
        src = self.sourceDDL.currentText()
        dest = self.destinationDDL.currentText()

        nodes = OrderedDict()
        edges = []
        buspath = []
        busroutes = OrderedDict()  # containing routes
        busnode = {}  # containing busnode
        temp = {}  # used for reverse finding

        # get all the names of geojson files for bus routes
        filedir = "BUS ROUTES\\"
        json_files = [pos_json for pos_json in os.listdir(filedir) if pos_json.endswith('.geojson')]

        # for file service
        for f in json_files:

            with open(filedir + f) as json_file:
                data = json.load(json_file)

            # get the bus service number
            service = data['features'][0]['properties']['ref']

            for feature in data['features']:
                # if the first item is a multilinestring, AKA bus route , then add it to a list called buspath
                if feature['geometry']['type'] == 'MultiLineString':
                    for i in range(len(feature['geometry']['coordinates'])):
                        for y in feature['geometry']['coordinates'][i]:
                            buspath.append(y)

                else:
                    # else it is a bus node

                    coord = feature['geometry']['coordinates']
                    # add the bus node into dictionary of nodes
                    nodes[feature['id']] = coord
                    # busnode is used for reverse finding
                    busnode[tuple(coord)] = feature['id']

                    # add the coordinates of the bus node together with path.
                    # This is necessary because the data set does not link the nodes and routes
                    lowest = 999
                    lowestIndex = 0
                    for i in range(len(buspath)):

                        # find the shortest distance between the current bus nodes and the path.
                        # The shortest distance means that the bus belongs in behind that coordinate
                        d = calc_distance(coord, buspath[i])
                        if d < lowest:
                            lowest = d
                            lowestIndex = i
                    buspath.insert(lowestIndex, coord)
                    # insert the busnode's coordinate into the buspath

            length = len(buspath)
            for i in range(length):
                c = tuple(buspath[i])
                k = str(service) + "-" + str(i)
                # key = service number + counter(for the routes coordinate)
                # value = coordinates

                busroutes[k] = c
                temp[c] = k
                # for reverse finding path coordinates to get name

            # creating edges for bus. Time is used for the weights
            for i in range(length):
                if i + 1 != length:
                    d = calc_distance(buspath[i], buspath[i + 1])
                    if tuple(buspath[i]) in busnode:
                        # if the coordinates of the buspath is a busstop , then the next coordinate is a path
                        edges.append((busnode[tuple(buspath[i])], temp[tuple(buspath[i + 1])], d / 30, service))

                    # else if the next coordinates of the buspath is a busnode, then the current coordinate is a path
                    elif tuple(buspath[i + 1]) in busnode:
                        edges.append((temp[tuple(buspath[i])], busnode[tuple(buspath[i + 1])], d / 30, service))
                    else:
                        # else both are bus paths
                        edges.append((temp[tuple(buspath[i])], temp[tuple(buspath[i + 1])], d / 30, service))

            temp.clear()
            buspath.clear()

        # initialise hdb nodes
        for feature_data in retrieveJSON.retrieveBuilding():
            buildingName = feature_data['properties']
            if 'name' in buildingName:
                retrieveHDB = buildingName['name']
                nodes[retrieveHDB] = find_midpoint(feature_data['geometry']['coordinates'])

        pathfinder = Dijkstra(nodes)  # parse in the nodes of hdb and busstops
        pathfinder.create_edges()  # create walk edges
        pathfinder.create_bus_edgenodes(edges, busnode, busroutes)  # create bus edges
        graph = pathfinder.build_graph()
        path = pathfinder.find_shortest_path(graph, src, dest)

        folium.PolyLine(path, opacity=1, color='red').add_to(self.m)
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.view.setHtml(data.getvalue().decode())

        print("----------------- Run Time ------------------")
        print("%s seconds" % (time.time() - run_time))
        print("")

#######################################################################################################################

    # Show Bus Service Path Function
    def generateBusServicePath(self):

        # Initializing the default map
        self.m = folium.Map(location=[1.400150, 103.910172], zoom_start=17)
        nodeData = os.path.join('exportBuilding.geojson')
        geo_json = folium.GeoJson(nodeData, popup=folium.GeoJsonPopup(fields=['name']))
        geo_json.add_to(self.m)
        busPath = self.busPathDDL.currentText()

        # Retrieving coordinates of the bus services route
        for bus_data in retrieveJSON.retrieveBusService():
            busName = bus_data['properties']
            if busPath == busName['name']:
                busCoord = [v[::-1] for v in bus_data['geometry']['coordinates'][0]]

        # Plot path on the map
        folium.PolyLine(busCoord, opacity=1, color='red').add_to(self.m)
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.view.setHtml(data.getvalue().decode())


#######################################################################################################################

if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
