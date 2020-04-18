from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, \
                            QTextEdit, QLabel, QPushButton
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtCore import QSize

# local imports
from network.client import ClientThread

class MainWindow(QMainWindow):
    """
    Top level UI class, contains all other widgets.
    """
    def __init__(self):
        """
        Sets window attributes, initializes main widget, calls UI initialization method
        """
        super().__init__()
        # setup main window parameters
        self.title = "UniNotes"
        self.left = 100
        self.top = 100
        self.width = 1080
        self.height = 720
        self.minWidth = 800
        self.minHeight = 600
        self._main = MainWidget()   # main widget contains the important UI elements and functions
        self.setCentralWidget(self._main)

        # call initUI method
        self.initUI()


        # set up connection from client to server
        self.client = ClientThread()
        self.client.start()


    def initUI(self):
        """
        Applies window attributes, dimensions to UI
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumSize(self.minWidth, self.minHeight)

        self.show()

class MainWidget(QWidget):
    """
    Contains all UI elements
    """
    def __init__(self):
        super().__init__()
        self.createLayouts()
        self.textWidget = TextWidget()  # create instance of text widget
        self.drawingWidget = DrawingWidget()    # create instance of drawing widget
        self.addLayouts()
        self.setLayout(self.mainLayout)

    def createLayouts(self):
        self.mainLayout = QHBoxLayout() # main layout for the entire widget

        self.menuLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.documentLayout = QHBoxLayout()

    def addLayouts(self):
        """
        Adds widgets and layouts to their proper layouts
        """
        self.documentLayout.addWidget(self.textWidget, 50)
        self.documentLayout.addWidget(self.drawingWidget, 50)

        self.rightLayout.addLayout(self.topLayout, 10)
        self.rightLayout.addLayout(self.documentLayout, 90)
        
        self.mainLayout.addLayout(self.menuLayout, 15)
        self.mainLayout.addLayout(self.rightLayout, 85)

class TextWidget(QTextEdit):
    """
    Widget for editing document text
    """
    def __init__(self):
        super().__init__()

class DrawingWidget(QWidget):
    """
    Combines canvas and color palette buttons
    """
    def __init__(self):
        super().__init__()
        self.canvas = Canvas()  # canvas 

        self.layout = QVBoxLayout() # layout to hold canvas and color palette
        self.setLayout(self.layout)
        self.layout.addWidget(self.canvas)

        self.palette = QHBoxLayout()    # holds color buttons
        self.addColorButtons()    # adds color buttons to palette
        self.layout.addLayout(self.palette)

    def addColorButtons(self):
        for c in ColorButton.COLORS:
            b = ColorButton(c)
            b.pressed.connect(lambda c=c: self.canvas.setPenColor(c))
            self.palette.addWidget(b)

class Canvas(QLabel):
    """
    Widget for drawing notes

    source: https://www.learnpyqt.com/courses/custom-widgets/bitmap-graphics/
    """
    def __init__(self):
        super().__init__()
        pixmap = QPixmap(400, 600) # create pixmap with initial size of 400 x 650
        # self.setScaledContents(True)    # allow label to scale with window re-sizing
        self.setPixmap(pixmap)

        self.last_x = None  # stores last known mouse x position
        self.last_y = None  # stores last known mouse y position
        self.penColor = QColor('#000000')   # initial pen color is black

    def setPenColor(self, c):
        self.penColor = QColor(c)

    def mouseMoveEvent(self, e):
        # ignore event if mouse button is not held
        if self.last_x is None:
            self.last_x = e.x()
            self.last_y = e.y()
            return

        painter = QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.penColor)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        # update origin for next time
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

class ColorButton(QPushButton):

    COLORS = [
                # 17 undertones https://lospec.com/palette-list/17undertones
                '#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49', 
                '#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b', 
                '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
    ]

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QSize(24, 24))
        self.color = color
        self.setStyleSheet(f'background-color: {color}')
