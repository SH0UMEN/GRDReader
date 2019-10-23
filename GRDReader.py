from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from colour import Color
import struct
import sys
import multiprocessing
import time
import numpy as np
from reader import read_and_draw
import PIL


class GRDReader(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(GRDReader, self).__init__(*args, **kwargs)
        self.setWindowTitle("GRD-reader")
            
        self.img = self.read_grd('D:/Projects/VS/GRDReader/Bezymyanka-Abramov_raschet.grd', 100)
        #img = self.get_grd_image(1000)

        label = QLabel()
        label.setPixmap(QPixmap(QPixmap.fromImage(self.img)))
        print("{} sec".format(time.time()-s_time))
        label.mousePressEvent = self.get_pos
        layout = QVBoxLayout()
        layout.addWidget(label)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def read_grd(self, filename, levels):
        #matrix
        #file = open(filename, 'rb')
        #file.read(4)
        #Nx, Ny = struct.unpack("h", file.read(2))[0], struct.unpack("h", file.read(2))[0]
        #Xmin, Xmax = struct.unpack("d", file.read(8))[0], struct.unpack("d", file.read(8))[0]
        #Ymin, Ymax = struct.unpack("d", file.read(8))[0], struct.unpack("d", file.read(8))[0]
        #self.Zmin, self.Zmax = struct.unpack("d", file.read(8))[0], struct.unpack("d", file.read(8))[0]
        #matrix = []

        #image
        green = Color("green")
        red = Color("red")
        colorRange = list(green.range_to(red, levels))
        colorRangeCopy = []

        for c in colorRange:
            col = QColor(c.get_hex())
            colorRangeCopy.append((col.red(), col.green(), col.blue(), col.alpha()))

        colorRange = colorRangeCopy

        s_time = time.time()

        try:
            img = read_and_draw(["D:/Projects/VS/GRDReader/relief.grd", 
                                colorRange])[1]
            img = QImage.loadFromData(img)

        except Exception as ex:
            print(ex)

        #h = (self.Zmax - self.Zmin) / levels
        #zLevels = []

        #for i in range(1, levels + 1):
        #    zLevels.append(self.Zmin + h * i)

        #img = QImage(Nx, Ny, 5)
        #ptr = img.bits()
        #ptr.setsize(img.byteCount())
        #arr = np.asarray(ptr).reshape(img.height(), img.width(), 4)

        ##handler
        #for y in range(Ny):
        #    raw = []
        #    for x in range(Nx):
        #        z = struct.unpack("f", file.read(4))[0]
        #        raw.append(z)

        #        for level in range(levels):
        #            if (z <= zLevels[level]):
        #                arr[y, x] = colorRange[level]
        #                break

        #    matrix.append(raw)

        #file.close()
        #self.matrix = matrix

        return img

    def get_grd_image(self, levels):
        levels = 50
        green = Color("green")
        red = Color("red")
        colorRange = list(green.range_to(red, levels))
        colorRangeCopy = []

        for c in colorRange:
            col = QColor(c.get_hex())
            colorRangeCopy.append((col.red(), col.green(), col.blue(), col.alpha()))

        colorRange = colorRangeCopy

        h = (self.Zmax - self.Zmin) / levels
        zLevels = []

        for i in range(1, levels + 1):
            zLevels.append(self.Zmin + h * i)

        Ys, Xs = len(self.matrix), len(self.matrix[0])
        img = QImage(Xs, Ys, 5)
        ptr = img.bits()
        ptr.setsize(img.byteCount())
        arr = np.asarray(ptr).reshape(img.height(), img.width(), 4)

        for y in range(Ys):
            for x in range(Xs):
                for level in range(levels):
                    if (self.matrix[y][x] <= zLevels[level]):
                        arr[y, x] = colorRange[level]
                        break

        return QPixmap(QPixmap.fromImage(img))

    def get_pos(self, event):
        color = self.img.pixelColor(event.pos().x(), event.pos().y())
        print(color.red(), color.green(), color.blue(), color.alpha())


app = QApplication(sys.argv)

window = GRDReader()
window.show()

# Start the event loop.
app.exec_()