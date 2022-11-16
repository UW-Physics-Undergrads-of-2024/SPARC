import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qtg
import vispy.scene as vp
import vispy.geometry as geo
import sys
class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()

        # set window icon
        self.setWindowIcon(qtg.QIcon('icon_temp.png'))

        # Set basic dimensions and attributes
        self.setWindowTitle("SPARC Visualizer")
        self.setGeometry(100, 100, 600, 600)

        # ******** Add widgets ************
        self.centralWidget = qt.QWidget()

        # ******** Configure layout *******

        # Create layouts
        self.topLevelLayout = qt.QVBoxLayout()
        self.canvasLayout = qt.QHBoxLayout()
        self.inputLayout = qt.QGridLayout()

        # nest layouts and bind them together and to the central widget
        self.topLevelLayout.addLayout(self.canvasLayout)
        self.topLevelLayout.addLayout(self.inputLayout)
        self.centralWidget.setLayout(self.topLevelLayout)

        # set QMainWindow's central widget to centralWidget QWidget*
        self.setCentralWidget(self.centralWidget)

        # Add vispy canvas to canvas layout
        self.canvas = vp.SceneCanvas(bgcolor=(0.788, 0.765, 0.776, 0.8))
        self.view = self.canvas.central_widget.add_view()
        self.canvasLayout.layout().addWidget(self.canvas.native)

        # Add vacuum tube assembly (cylinder as placeholder for now) to view
        self.vacuum = geo.generation.create_cylinder(rows = 10, cols = 10, radius=[1.0, 1.0], length = 10)
        self.view.add(self.vacuum)

        # Add labelled combo box for left magnet position
        self.labelLeftMagnet = qt.QLabel(self)
        self.labelLeftMagnet.setText("Left Magnet Pos.")
        self.labelLeftMagnet.setStyleSheet("border: 1px solid black;")
        self.inputLayout.layout().addWidget(self.labelLeftMagnet,0,0)

        self.leftMagnetPosition = qt.QComboBox(self)
        self.leftMagnetPosition.addItems(["1", "2", "3"])
        self.inputLayout.layout().addWidget(self.leftMagnetPosition,0,1)

        # Add labelled combo box for right magnet position
        self.labelRightMagnet = qt.QLabel(self)
        self.labelRightMagnet.setText("Right Magnet Pos.")
        self.labelRightMagnet.setStyleSheet("border: 1px solid black;")
        self.inputLayout.layout().addWidget(self.labelRightMagnet,0,2)

        self.rightMagnetPosition = qt.QComboBox(self)
        self.rightMagnetPosition.addItems(["1", "2", "3"])
        self.inputLayout.layout().addWidget(self.rightMagnetPosition,0,3)

        # Add labelled combo box for voltage
        self.labelVoltage = qt.QLabel(self)
        self.labelVoltage.setText("Voltage")
        self.labelVoltage.setStyleSheet("border: 1px solid black;")
        self.inputLayout.layout().addWidget(self.labelVoltage,1,0)

        self.voltageSelector = qt.QComboBox(self)
        self.voltageSelector.addItems(["10kV", "20kV", "50kV"])
        self.inputLayout.layout().addWidget(self.voltageSelector,1,1)

        # Add button widget to load scene
        self.setSceneButton = qt.QPushButton(self)
        self.setSceneButton.setText("Load Scene")
        self.setSceneButton.setStyleSheet("border: 1px solid black;")
        self.inputLayout.layout().addWidget(self.setSceneButton,1,2)
        


if __name__ == '__main__':
    app = qt.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


