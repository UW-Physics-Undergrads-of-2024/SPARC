import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qtg
import vispy as vp
import sys

vp.use('PyQt6')

class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()

        # set window icon
        self.setWindowIcon(qtg.QIcon('icon_temp.png'))

        # Set basic dimensions and attributes
        self.setWindowTitle("SPARC Visualizer")
        self.setGeometry(100, 100, 600, 600)

        # ******** Add widgets ************

        # Add labelled combo box for left magnet position
        self.labelLeftMagnet = qt.QLabel(self)
        self.labelLeftMagnet.setText("Left Magnet Pos.")
        self.labelLeftMagnet.resize(110,30)
        self.labelLeftMagnet.setStyleSheet("border: 1px solid black;")
        self.labelLeftMagnet.move(50, 400)
        self.leftMagnetPosition = qt.QComboBox(self)
        self.leftMagnetPosition.addItems(["1", "2", "3"])
        self.leftMagnetPosition.move(160,400)

        # Add labelled combo box for right magnet position
        self.labelRightMagnet = qt.QLabel(self)
        self.labelRightMagnet.setText("Right Magnet Pos.")
        self.labelRightMagnet.resize(110, 30)
        self.labelRightMagnet.setStyleSheet("border: 1px solid black;")
        self.labelRightMagnet.move(300, 400)
        self.rightMagnetPosition = qt.QComboBox(self)
        self.rightMagnetPosition.addItems(["1", "2", "3"])
        self.rightMagnetPosition.move(410, 400)

        # Add labelled combo box for voltage
        self.labelVoltage = qt.QLabel(self)
        self.labelVoltage.setText("Voltage")
        self.labelVoltage.resize(110, 30)
        self.labelVoltage.setStyleSheet("border: 1px solid black;")
        self.labelVoltage.move(50, 500)
        self.rightMagnetPosition = qt.QComboBox(self)
        self.rightMagnetPosition.addItems(["10kV", "20kV", "50kV"])
        self.rightMagnetPosition.move(160, 500)

        # Add button widget to load scene
        self.setSceneButton = qt.QPushButton(self)
        self.setSceneButton.setText("Load Scene")
        self.setSceneButton.resize(210,30)
        self.setSceneButton.setStyleSheet("border: 1px solid black;")
        self.setSceneButton.move(300,500)

        # add connections
        self.leftMagnetPosition.connect("currentIndexChanged(int)", self.updateLeftMagnetPos)


if __name__ == '__main__':
    app = qt.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


