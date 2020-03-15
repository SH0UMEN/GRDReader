from reader import read_and_draw
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import struct
import sys
import multiprocessing
import time
import numpy as np
from colour import Color
from MapView import MapView
from AreaList import AreaList
from AreaAddPanel import AreaAddPanel

class GRDReader(QMainWindow):
    points = []
    pointsCounter = 0
    areasCounter = 0
    areaWidgets = []

    def __init__(self, *args, **kwargs):
        super(GRDReader, self).__init__(*args, **kwargs)
        self.setWindowTitle("GRD-reader")

        self.setMenu()

        self.map = MapView(self)
        self.map.photoClicked.connect(self.addPoint)

        #Main
        self.layoutMain = QGridLayout()

        #Instruments panel
        self.instrumentPanel = QWidget()
        self.instrumentPanelLayout = QHBoxLayout()
        self.instrumentPanelLayout.setContentsMargins(0, 2, 0, 2)
        self.toggleDragMode = QPushButton("Прокрутка/выбор точек")
        self.toggleDragMode.clicked.connect(self.map.toggleDragMode)
        self.instrumentPanelLayout.addWidget(self.toggleDragMode)
        self.instrumentPanelLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.instrumentPanel.setLayout(self.instrumentPanelLayout)

        #Right panel
        self.rightPanel = QWidget()
        self.rightPanel.setFixedWidth(350)
        self.rightPanelLayout = QBoxLayout(QBoxLayout.TopToBottom)
        self.rightPanelLayout.setSpacing(0)

        #Widget for adding areas
        self.areaAddPanel = AreaAddPanel()

        #Add new area button
        self.addAreaButton = QPushButton("Добавить зону")
        self.addAreaButton.clicked.connect(self.addArea)

        #List of areas
        self.areaList = AreaList()

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.layoutMain.addWidget(self.instrumentPanel, 0, 0, 1, 2)
        self.layoutMain.addWidget(self.map, 1, 0)
        self.rightPanelLayout.addWidget(self.areaAddPanel)
        self.rightPanelLayout.addWidget(self.addAreaButton)
        self.rightPanelLayout.addWidget(self.areaList)
        self.rightPanelLayout.addItem(self.verticalSpacer)
        self.rightPanel.setLayout(self.rightPanelLayout)
        self.layoutMain.addWidget(self.rightPanel, 1, 1)

        mw = QWidget()
        mw.setLayout(self.layoutMain)
        self.setGeometry(500, 300, 800, 600)
        self.setCentralWidget(mw)

    #Creating menu
    def setMenu(self):
        #Open .grd
        openGRDAction = QAction("Открыть .grd файл", self)
        openGRDAction.setStatusTip('Открыть .grd файл')
        openGRDAction.triggered.connect(self.openFileDialog)

        #Export
        exportAction = QAction("Экспорт", self)
        exportAction.setStatusTip('Экспортировать зоны')
        exportAction.triggered.connect(self.exportAreas)

        self.statusBar()

        mainMenu = self.menuBar()
        menu = mainMenu.addMenu('&Меню')
        menu.addAction(openGRDAction)
        menu.addAction(exportAction)
        
    def openFileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Открыть файл', '/home')[0]
        if not fname:
            return 0
        elif not fname.endswith(".grd"):
            self.openMesBox("Ошибка!", "Программа принимает только файлы формата .grd")
            return 0

        self.matrix, self.img = self.readGRD(fname, 30)
        self.map.setPhoto(self.img)
       
    def readGRD(self, filename, levels):
        green = Color("green")
        red = Color("red")
        print(red.get_hex())
        colorRange = list(green.range_to(red, levels))
        colorRangeCopy = []

        for c in colorRange:
            col = QColor(c.get_hex())
            colorRangeCopy.append([col.blue(), col.green(), col.red(), col.alpha()])

        colorRange = colorRangeCopy

        matrix, imgMatrix = read_and_draw([filename, colorRange])

        img = QImage(len(imgMatrix[0]), len(imgMatrix), 5)
        ptr = img.bits()
        ptr.setsize(img.byteCount())
        arr = np.asarray(ptr).reshape(img.height(), img.width(), 4)
        np.copyto(arr, imgMatrix, casting="unsafe")

        return matrix, QPixmap(QPixmap.fromImage(img))

    #Add new point
    def addPoint(self, event):
        if(not self.map.isDragMode):
            x, y = event.x()+1, len(self.matrix) - event.y() + 1
            point = self.areaAddPanel.addPoint(x, y)

            if(point == 0):
                self.openMesBox("Ошибка!", "Не удалось построить зону. Выберите другую точку")
            elif(point):
                self.points.append(self.map.drawPoint(event.x(), event.y()))
            else:
                self.openMesBox("Ошибка!", "Нельзя указать больше 2-х точек")

    #Remove last point
    def removeLastPoint(self):
        removedPoint = self.areaAddPanel.removeLastPoint()

        if(removedPoint):
            self.map._scene.removeItem(self.points.pop())

    #Add area with parameters to list
    def addArea(self):
        #text += "({};{})|".format(point[0], point[1])

        if(len(self.points) == 2):
            self.areaList.addArea(self.areaAddPanel.points[0], 
                                  self.areaAddPanel.points[1], 
                                  self.areaAddPanel.angle)

            self.removeLastPoint()
            self.removeLastPoint()
            self.areaAddPanel.angleLabel.setText("Угол: ")
            self.areaAddPanel.angle = ""

    #Message box
    def openMesBox(self, title, text):
        dlg = QDialog(self)
        dlg.setWindowTitle(title)
        l = QHBoxLayout()
        label = QLabel()
        label.setText(text)
        l.addWidget(label)
        dlg.setLayout(l)
        dlg.exec_()

    #Export areas
    def exportAreas(self):
        fname = QFileDialog.getSaveFileName(self, 'Экспорт', '/home', "*.dat")[0]
        file = open(fname, "w")
        areas = self.areaList.areas

        for i in range(len(areas)):
            area = areas[i]
            file.write(str(area.angle)+"\n")
            
            if(area.points[0][0] >= area.points[1][0]):
                file.write(str(area.points[1][0])+"\n")
                file.write(str(area.points[0][0])+"\n")
            else:
                file.write(str(area.points[0][0])+"\n")
                file.write(str(area.points[1][0])+"\n")

            if(area.points[0][1] >= area.points[1][1]):
                file.write(str(area.points[1][1])+"\n")
                file.write(str(area.points[0][1]))
            else:
                file.write(str(area.points[0][1])+"\n")
                file.write(str(area.points[1][1]))

            if(i < len(areas) - 1):
                file.write("\n")

        file.close()

    #Check shortcuts
    def keyPressEvent(self, event):
        
        #Remove last point
        if int(event.modifiers()) == (Qt.ControlModifier) and event.key() == Qt.Key_Z:
            self.removeLastPoint()

app = QApplication(sys.argv)

window = GRDReader()
window.show()

# Start the event loop.
app.exec_()