from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import time
import os
from communication import setGrabCoordinates, getGrabCoordinates

basedir = os.path.dirname(__file__)
exe_path = os.path.normpath('.\\')


class CaptureWindow(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent = None)
        
        coordinates_data = getGrabCoordinates()
        
        self.close_clicked = False
        
        self.parent = parent
        self.top_leftX = coordinates_data['topLeftX']
        self.top_leftY = coordinates_data['topLeftY']
        self.width = coordinates_data['width']
        self.height = coordinates_data['height']
        
        self.window_begin_point = QPoint(self.top_leftX - 5, self.top_leftY - 5)
        self.window_size = QSize(self.width + 10, self.height + 10 + 5 + 32)
        
        self.setGeometry(QRect(self.window_begin_point, self.window_size))
        
        self.custom_video_name = ''
        
        self.recordIcon = QIcon(os.path.join(basedir, 'icons', 'control-record.png'))
        self.stopIcon  = QIcon(os.path.join(basedir, 'icons', 'control-stop-square.png'))
        self.cancelIcon = QIcon(os.path.join(basedir, 'icons', 'cross.png'))
        
        # RESIZE WINDOW
#         self.resize(self.width,self.height)
        
#         self.setWindowOpacity(50);

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout()
        
        self.container = QFrame()
        self.container.setFrameShape(QFrame.NoFrame)
        self.container.setLineWidth(0)
        
        self.capture_frame = QFrame()
        
        self.size_grip = QSizeGrip(self.capture_frame)

        self.size_grip.resize(32, 32)
#         self.size_grip.setStyleSheet("background-color: red;"
#                                      "border: 0px;")
               
        
#         self.container.setStyleSheet("background-color: rgba(255, 0, 0, 125);"
#                                      "border: 1px solid black;")
        self.capture_frame.setObjectName("capture_frame");
        self.capture_frame.setStyleSheet("QWidget#capture_frame { background-color: rgba(125, 125, 125, 0); border: 5px dashed black}")
#         self.capture_frame.setStyleSheet("background-color: rgba(125, 125, 125, 0);"
#                                          "border: 5px dashed black;")
        
        self.record_button = QPushButton('', self)
        self.record_button.setIcon(self.recordIcon)
        self.record_button.setIconSize(QSize(24,24))
        self.record_button.setFixedSize(32,32)
        
        self.stop_record_button = QPushButton('', self)
        self.stop_record_button.setIcon(self.stopIcon)
        self.stop_record_button.setIconSize(QSize(24,24))
        self.stop_record_button.setFixedSize(32,32)
        
        self.close_button = QPushButton('', self)
        self.close_button.setIcon(self.cancelIcon)
        self.close_button.setIconSize(QSize(24,24))
        self.close_button.setFixedSize(32,32)
        
        
        self.record_button.clicked.connect(self.startRecord)
        self.stop_record_button.clicked.connect(self.stopRecord)
        self.close_button.clicked.connect(self.close_record_window)
        
        self.buttons_layout = QHBoxLayout()
        
        self.buttons_layout.setContentsMargins(0,0,0,0)
        
        self.buttons_layout.addStretch(1)
        self.buttons_layout.addWidget(self.record_button)
        self.buttons_layout.addWidget(self.stop_record_button)
        self.stop_record_button.hide()
        self.buttons_layout.addWidget(self.close_button)
        
        
#         self.layout.addStretch(0)
        self.layout.addWidget(self.capture_frame)
        
#         self.layout.addWidget(self.some_button)
#         self.layout.addWidget(self.some_button2)
#         self.layout.addSpacing(1)
        self.layout.addLayout(self.buttons_layout)
        self.layout.setSpacing(5)
#         self.layout.addWidget(self.size_grip)
#         self.layout.insertStretch(-1, 0)
        
        self.container.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.setCentralWidget(self.container)

    def get_window_geometry(self):
        return self.window_begin_point, self.window_size
    
    def close_record_window(self):
        setGrabCoordinates(self.top_leftX, self.top_leftY, self.width, self.height)
        self.close_clicked = True
        self.stopRecord()
        self.hide()
        self.parent.set_region_action.setDisabled(False)

    def startRecord(self):
        self.record_button.hide()
        self.stop_record_button.show()
        self.parent.communications.captureRHEED()
        
    def stopRecord(self):
        self.stop_record_button.hide()
        self.record_button.show()
        self.parent.communications.IsCapturing = False
        
    def save_video(self):
        if not self.close_clicked:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File",exe_path,"Video (*.mp4)")
            if file_name:
                self.custom_video_name = file_name
            else:
                self.custom_name = ''
        self.close_clicked = False
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.globalPosition()
#         if event.button() == Qt.RightButton:
#             self.close()
        
    def mouseMoveEvent(self, event):
        delta = event.globalPosition() - self.startPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.startPos = event.globalPosition()
        
        if event.buttons() & Qt.LeftButton:
            geometry = self.geometry()
            self.top_leftX = geometry.x()+5
            self.top_leftY = geometry.y()+5
            self.width = geometry.width()-10
            self.height = geometry.height()-47
            
            self.window_begin_point = QPoint(self.top_leftX - 5, self.top_leftY - 5)
            self.window_size = QSize(self.width + 10, self.height + 10 + 5 + 32)
        
    def resizeEvent(self, event):
        geometry = self.geometry()
        self.top_leftX = geometry.x()+5
        self.top_leftY = geometry.y()+5
        self.width = geometry.width()-10
        self.height = geometry.height()-47
        
        self.window_begin_point = QPoint(self.top_leftX - 5, self.top_leftY - 5)
        self.window_size = QSize(self.width + 10, self.height + 10 + 5 + 32)
    