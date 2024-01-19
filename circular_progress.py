from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class CircularProgress(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        # CUSTOM PROPERTIES
        self.value = 0
        self.text_value = 0
        self.width = 200
        self.height = 200
        self.progress_width = 10
        self.progress_rounded_cap = True
        self.max_value = 100
        self.progress_color = 0x498BD1
        # Text
        self.font_family = "Segoe UI"
        self.font_size = 12
        self.suffix = "%"
        self.text_color = 0x498BD1
        # BG
        self.enable_bg = True
        self.bg_color = 0x44475a
        
        # SET DEFAULT SIZE WITHOUT LAYOUT
        self.resize(self.width, self.height)
        
    # ADD DROPSHADOW
    def add_shadow(self, enable):
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0,0,0,255))
        self.setGraphicsEffect(self.shadow)
        
    # SET VALUE
    def set_value(self, value, text_value):
        self.value = value
        self.text_value = text_value
        self.repaint()
        
        # PAINT EVENT (CIRCULAR PROGRESS DESIGN)
    def paintEvent(self, event):
        # SET PROGRESS PARAMETERS
        width = self.width - self.progress_width
        height = self.height - self.progress_width
        margin = self.progress_width / 2
        value = self.value * 360 / self.max_value
        
        # PAINTER
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing) # remove pixelated edges
        paint.setFont(QFont(self.font_family, self.font_size))
        
        # CREATE RECTANGLE
        rect = QRect(0, 0, self.width, self.height)
        paint.setPen(Qt.NoPen)
        paint.drawRect(rect)
        
        # PEN
        pen = QPen()
        pen.setColor(QColor(self.progress_color))
#         pen.setWidth(self.progress_width)
        # Set Round Cap
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)
            
        # ENABLE BG
        if self.enable_bg:
            pen.setColor(QColor(self.bg_color))
            pen.setWidth(self.progress_width-2)
            paint.setPen(pen)
            paint.drawArc(margin, margin, width, height, 0, 360 * 16)
            
        # CREATE ARC
        pen.setColor(QColor(self.progress_color))
        pen.setWidth(self.progress_width)
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90 * 16, -value * 16)
        
        # CREATE TEXT
        pen.setColor(QColor(self.text_color))
        paint.setPen(pen)
        paint.drawText(rect, Qt.AlignCenter, f"{self.text_value}{self.suffix}")
        
        
        # END
        paint.end()
        