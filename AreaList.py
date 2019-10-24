from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Area import Area

class AreaList(QWidget):
    areasWidgets = []
    areas = []

    def __init__(self):
        super(AreaList, self).__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,10,0,10)

    #Add new area
    def addArea(self, pointOne, pointTwo, angle):
        areaWidget = QWidget()
        areaLayout = QHBoxLayout()
        areaLayout.setContentsMargins(0,0,0,0)
        area = Area(pointOne, pointTwo, angle)
        self.areas.append(area)
        areaText = QLabel("({};{})|({};{})|{}".format(pointOne[0], pointOne[1], pointTwo[0], pointTwo[1], angle))

        selfDeleteButton = QPushButton("Удалить")
        selfDeleteButton.clicked.connect(lambda: self.removeArea(areaWidget))

        areaLayout.addWidget(areaText)
        areaLayout.addWidget(selfDeleteButton)

        areaWidget.setLayout(areaLayout)
        self.areasWidgets.append(areaWidget)
        self.layout.addWidget(areaWidget)

    #Remove area
    def removeArea(self, area):
        index = self.areasWidgets.index(area)
        area = self.areasWidgets.pop(index)
        self.areas.pop(index)
        label, button = area.layout().takeAt(0), area.layout().takeAt(1)
        area.layout().removeItem(label)
        area.layout().removeItem(button)
        self.layout.removeWidget(area)
        area.deleteLater()