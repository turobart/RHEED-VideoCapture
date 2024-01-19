from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from communication import getGrabCoordinates, setGrabCoordinates
import time
import json

class DrawWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        # RESIZE WINDOW
        self.resize(100,100)
        self.parent = parent
        
#         coordinates_data = getGrabCoordinates()

#         self.windowBeginPoint = QPoint(coordinates_data['topLeftX']-5, coordinates_data['topLeftY']-5)
#         self.windowDestinationPoint = QPoint(coordinates_data['topLeftX']+coordinates_data['width']+5, coordinates_data['topLeftY']+coordinates_data['height']+5+32+5)
#         self.windowSize = QSize(coordinates_data['width'] + 10, coordinates_data['height'] + 10 + 5 + 32)
        
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.container = QFrame()
        self.container.setStyleSheet("background-color: rgba(125, 125, 125, 125);")
        self.borderRadius = 1
        self.layout = QVBoxLayout()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        
        self.pix = QPixmap(self.rect().size())

        self.beginPoint, self.destinationPoint = QPoint(), QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.pix)
        
        if not self.beginPoint.isNull() and not self.destinationPoint.isNull():
            rect = QRect(self.beginPoint, self.destinationPoint)
            painter.drawRect(rect.normalized())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.beginPoint = event.pos()
            self.destinationPoint = self.beginPoint
            self.update()
            
        elif (event.buttons() & Qt.RightButton) and (event.buttons() & Qt.LeftButton):
            self.beginPoint, self.destinationPoint = QPoint(), QPoint()
            self.update()
            
        elif event.button() == Qt.RightButton:
            self.close()
               
    def mouseMoveEvent(self, event):
        self.destinationPoint = event.pos()
        self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            rect = QRect(self.beginPoint, self.destinationPoint)
            painter = QPainter(self.pix)
            painter.drawRect(rect.normalized())
            
            self.update()
            
            if not self.beginPoint.isNull() and not self.destinationPoint.isNull():
                
                if self.beginPoint.x() < self.destinationPoint.x():
                    beginX = self.beginPoint.x()
                    endX = self.destinationPoint.x()
                else:
                    beginX = self.destinationPoint.x()
                    endX = self.beginPoint.x()
                if self.beginPoint.y() < self.destinationPoint.y():
                    beginY = self.beginPoint.y()
                    endY = self.destinationPoint.y()
                else:
                    beginY = self.destinationPoint.y()
                    endY = self.beginPoint.y()
                
#                 adjusted_begin_point = QPoint(beginX, beginY)
#                 adjusted_end_point = QPoint(endX, endY)
                
                self.parent.capture_window.top_leftX = beginX
                self.parent.capture_window.top_leftY = beginY
                self.parent.capture_window.width = endX - beginX
                self.parent.capture_window.height = endY - beginY
                
                self.parent.capture_window.window_begin_point = QPoint(beginX - 5, beginY - 5)
                self.parent.capture_window.window_size = QSize(endX - beginX + 10, endY - beginY + 47)
                
#                 self.windowBeginPoint = self.beginPoint - QPoint(5, 5)
#                 self.windowDestinationPoint = self.destinationPoint + QPoint(5, 5)+ QPoint(0, 32)+ QPoint(0, 5)
                
#                 self.windowSize = QSize(self.windowDestinationPoint.x() - self.windowBeginPoint.x(), self.windowDestinationPoint.y() - self.windowBeginPoint.y())

                setGrabCoordinates(beginX, beginY, beginX - endX, beginY - endY)
                
                
                time.sleep(1)               
                self.beginPoint, self.destinationPoint = QPoint(), QPoint()
                
                self.close()

#     def getRectangleCoords(self):
#         return self.windowBeginPoint, self.windowSize 