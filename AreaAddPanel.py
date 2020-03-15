from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

class AreaAddPanel(QWidget):
    points = []
    pointLabels = []
    angle = ""

    def __init__(self):
        super(AreaAddPanel, self).__init__()
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 20)
       
        self.angleLabel = QLabel("Угол: ")

        self.pointLabels.append(QLabel("Первая точка:"))
        self.pointLabels.append(QLabel("Вторая точка:"))

        self.layout.addWidget(self.pointLabels[0], 0, 0)
        self.layout.addWidget(self.pointLabels[1], 0, 1)
        self.layout.addWidget(self.angleLabel, 1, 0)

        self.setLayout(self.layout)

    #Add new point
    def addPoint(self, x, y):
        if(len(self.points) == 0):
            self.pointLabels[0].setText("Первая точка: ({};{})".format(x, y))
            self.points.append([x, y])
            return [x, y]

        elif(len(self.points) == 1):
            if(self.points[0][0] == x):
                return 0

            self.pointLabels[1].setText("Вторая точка: ({};{})".format(x, y))

            if(y > self.points[0][1]):
                point = [x - self.points[0][0], y - self.points[0][1]]
            else:
                point = [self.points[0][0] - x, self.points[0][1] - y]

            self.angle = -((math.atan(point[1]/point[0])*(180/math.pi))/90)
            self.angleLabel.setText("Угол: " + str(self.angle))
            self.points.append([x, y])
            return [x, y]

    #Remove last point
    def removeLastPoint(self):
        if(len(self.points) == 2):
            self.pointLabels[1].setText("Вторая точка:")
            return self.points.pop()
        elif(len(self.points) == 1):
            self.pointLabels[0].setText("Первая точка:")
            return self.points.pop()
