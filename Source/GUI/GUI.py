import PyQt6.QtWidgets as Qt
import sys

# Declare a Qt application
app = Qt.QApplication([])

# Create a window
window = Qt.QWidget()
window.setWindowTitle("PyQt App")
window.setGeometry(100, 100, 280, 80)

window.show()

