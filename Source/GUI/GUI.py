import PyQt6.QtWidgets as qt
import vispy as vp
import sys

vp.use('PyQt6')

class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set basic dimensions and attributes
        self.setWindowTitle("SPARC Visualizer")
        self.setGeometry(100, 100, 500, 500)

        # Create vispy canvas

# Declare a Qt application
app = qt.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec()

