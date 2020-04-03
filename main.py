import sys

# import from UI library
from PyQt5.QtWidgets import QApplication

# local imports
from ui.mainWindow import MainWindow

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()