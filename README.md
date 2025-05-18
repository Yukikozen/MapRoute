# WELCOME TO GROUP P2-6 ICT 1008 Project 

## INSTALLATION GUIDE

<h3 /h3>

1) **Install PyQt (GUI)**

```
pip install PyQt5
      OR
conda install -c anaconda pyqt
```

2) **Download repository**
<img src="Git-Image/Step 1.PNG" width="700" height="500" >

3) **Unzip the folder**

4) **Placed the Folium folder into your project interpreter**

<img src="Git-Image/Folium_folder.PNG" width="700" height="500" >

**In my case, I am using anaconda as my project interpretor in PyCharm**

<img src="Git-Image/project_interpreter.PNG" width="700" height="80" >

5) **If all libraries are installed correctly, there should not be any errors importing of folium in pyqtGUI.py**

6) **Run pyqtGUI.py**
<img src="Git-Image/projectApplication.PNG" width="700" height="400" >

#

## INTRODUCTION
Developing a path finding program, utilizing PyQT5 for the Graphical User Interface (GUI) and Folium for the interactive map component. Our program allow users to find the shortest path from their Source location to Destination location. 

### Building Dataset
Dataset containing coordinates of a desginated area of Punggol
- exportBuilding.geojson

### Bus Service Dataset
Dataset containing the routes of each Bus Services operating at a desginated area og Punggol
- BusService.geojson
- BUS ROUTES

### MRT Dataset
Dataset containing the LRT track operating at Punggol
- MRT ROUTES

### Algorithm
The program is using Dijkstra'a algorithm to plot:
1) Shortest Walking Path
2) Fastest Bus Path
3) Fast Train Path
