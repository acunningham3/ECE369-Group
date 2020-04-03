from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout

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
        self._main = MainWidget()
        self.setCentralWidget(self._main)

        # call initUI method
        self.initUI()

    def initUI(self):
        """
        Applies window attributes, dimensions to UI
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumSize(self.minWidth, self.minHeight)
        self.horizontalLayout = QHBoxLayout()
        self.setCentralWidget = self.horizontalLayout

        self.show()

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
