'''
Author: Bartlomiej Turowski

Some icons by Yusuke Kamiyamane.'''

import sys
import os
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# IMPORT CIRCULAR PROGRESS
from circular_progress import CircularProgress
from communication import PcComm
from drawWindow import DrawWindow
from captureWindow import CaptureWindow

import ctypes
myappid = 'RHEED' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

basedir = os.path.dirname(__file__)

exe_path = os.path.normpath('.\\')

temp_path = os.path.join(exe_path, 'temp_video')
save_path = os.path.join(exe_path, 'auto_capture_videos')

if not os.path.exists(temp_path):
    os.makedirs(temp_path)
if not os.path.exists(save_path):
    os.makedirs(save_path)

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # RESIZE WINDOW
        self.resize(100,100)
        
        self.connect_text = 'Connect to PC'
        self.connectEnable = True

        self.setWindowIcon(QIcon(os.path.join(basedir, 'icons', 'RHEED.ico')))
        
        self.connectIcon = QIcon(os.path.join(basedir, 'icons', 'chain.png'))
        self.disconnectIcon = QIcon(os.path.join(basedir, 'icons', 'chain-unchain.png'))
        self.closeIcon = QIcon(os.path.join(basedir, 'icons', 'cross-octagon.png'))
        self.captureRegionIcon = QIcon(os.path.join(basedir, 'icons', 'border-down.png'))
        self.startCaptureIcon = QIcon(os.path.join(basedir, 'icons', 'films.png'))
        
        self.statusIcon = self.connectIcon
        
        self.draw_window = DrawWindow(self)
        self.capture_window = CaptureWindow(self)
        
        self.draw_window.setCursor((Qt.CrossCursor))
        
        self.contextMenu = QMenu(self)
            
        self.connectAction = QAction(QIcon(self.statusIcon), self.connect_text, self)
        self.set_region_action = QAction(QIcon(self.captureRegionIcon), "Set capture region", self)
        startCaptureAction = QAction(self.startCaptureIcon, "Start capture", self)
        self.connectAction.setEnabled(self.connectEnable)     
        closeAction = QAction(self.closeIcon, "Close", self)
        
        self.connectAction.triggered.connect(self.connect_to_pc)
        self.set_region_action.triggered.connect(self.create_capture_window)
        startCaptureAction.triggered.connect(self.show_capture_window)
        closeAction.triggered.connect(self.close_all)
        
        self.contextMenu.addAction(self.connectAction)
        self.contextMenu.addAction(self.set_region_action)
        self.contextMenu.addAction(startCaptureAction)
        self.contextMenu.addAction(closeAction)

        # REMOVE TITLE BAR
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # CONTAINER AND LAYOUT
        self.container = QFrame()
        self.container.setStyleSheet("background-color: #B8405E;"
                                     "border-radius: 50")
        self.borderRadius = 1
        self.layout = QVBoxLayout()
        
        # CREATE CIRCULAR PROGRESS
        self.progress = CircularProgress()
        self.progress.value = 0
        self.progress.suffix = " s"
        self.progress.font_size = 15
        self.progress.width = 80
        self.progress.height = 80
        self.progress.progress_width = 10
        self.progress.text_color = 0x000000
        self.progress.progress_color = 0x313552
        self.progress.progress_rounded_cap = True
        self.progress.add_shadow(True)
        self.progress.enable_bg = True
        self.progress.bg_color = 0xEEE6CE
        self.progress.setMinimumSize(self.progress.width, self.progress.height)
        
        # WIDGETS
        self.layout.addWidget(self.progress, Qt.AlignCenter, Qt.AlignCenter)
        
        # SET CENTRAL WIDGET
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        
        # SHOW WINDPW
        self.show()
        
        self.communications = PcComm(self)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.globalPosition()
        elif event.button() == Qt.RightButton:
            self.contextMenu.popup(QCursor.pos())
            
    def mouseDoubleClickEvent(self, event):
        print("doublePress")
        
    def close_all(self):
        self.capture_window.close()
        self.close()
                
    def show_capture_window(self):
        a, b = self.capture_window.get_window_geometry()
        self.capture_window.setGeometry(QRect(a,b))
        self.capture_window.show()
        self.set_region_action.setDisabled(True)
    
    def close_capture_window(self):
        self.capture_window.hide()
            
    def create_capture_window(self):
        self.draw_window.showFullScreen()
        
            
    def enableConnect(self, enabled):
        self.connectEnable = enabled
        
    def connect_to_pc(self):
        isListening = self.communications.StartClicked()
        if isListening:
            self.container.setStyleSheet("background-color: #2EB086;"
                                         "border-radius: 50")
            self.connectAction.setText("Disconnect from PC")
            self.connectAction.setIcon(self.disconnectIcon)
        else:
            self.container.setStyleSheet("background-color: #B8405E;"
                                         "border-radius: 50")
            self.connectAction.setText("Connect to PC")
            self.connectAction.setIcon(self.connectIcon)
#         
    def mouseMoveEvent(self, event):
        delta = event.globalPosition() - self.startPos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.startPos = event.globalPosition()
        
    # CHANGE VALUE
    def change_value(self, value, text_value):
        self.progress.set_value(value, text_value)       
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())