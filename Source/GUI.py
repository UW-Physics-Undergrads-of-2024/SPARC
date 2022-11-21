import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qtg
import vispy.scene as vs
import numpy as np
import vispy.visuals as vv

import sys
import trimesh
class MainWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()

        # set window icon
        self.setWindowIcon(qtg.QIcon('icon_temp.png'))

        # Set basic dimensions and attributes
        self.setWindowTitle("SPARC Visualizer")
        self.setGeometry(100, 100, 600, 600)

        # Add QWidget as central widget
        self.centralWidget = qt.QWidget()

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

        # *********** Set Vispy Canvas ********************************
        self.canvas = vs.SceneCanvas(title="Simulated SPARC", keys="interactive", bgcolor=(0.309, 0.345, 0.454, 1.0))
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = "turntable"
        self.canvasLayout.layout().addWidget(self.canvas.native)

        # Add XYZ
        axis = vs.visuals.XYZAxis(parent=self.view.scene)
        stransform = vv.transforms.STTransform(translate=(-5, -5), scale=(1, 1, 1, 1))
        affine = stransform.as_matrix()
        axis.transform = affine

        # Set initial camera position and orientation
        self.view.camera.azimuth = -15
        self.view.camera.elevation = 30
        self.view.camera.distance = 15

        # Add board that all components will be mounted on
        boardMesh = trimesh.load(r"Mesh/SPARC_board.stl")
        board = vs.visuals.Mesh(vertices=boardMesh.vertices, faces=boardMesh.faces, color=(0.8,0.4,0,1))
        board.attach(vv.filters.mesh.ShadingFilter(shading="smooth", ))
        self.view.add(board)

        # Add vacuum tube assembly to view
        vacuumMesh = trimesh.load(r"Mesh/SPARC_vacuum.stl")
        vacuum = vs.visuals.Mesh(vertices=vacuumMesh.vertices, faces=vacuumMesh.faces, color='blue')
        vacuum.attach(vv.filters.Alpha(0.2)) # makes mesh semi-transparent
        vacuum.attach(vv.filters.mesh.ShadingFilter(shading="smooth"))
        self.view.add(vacuum)

        # ****************** Add vacuum tube assembly to view ***************************

        # Add vacuum tube itself
        vacuumMountMesh = trimesh.load(r"Mesh/SPARC_vacuum_mount.stl")
        vacuumMount = vs.visuals.Mesh(vertices=vacuumMountMesh.vertices, faces=vacuumMountMesh.faces, color=(1,1,0.6,1))
        vacuumMount.attach(vv.filters.mesh.ShadingFilter(shading="smooth"))
        self.view.add(vacuumMount)

        # Add copper coil anode
        anodeMesh = trimesh.load(r"Mesh/SPARC_vacuum_anode.stl")
        anode = vs.visuals.Mesh(vertices=anodeMesh.vertices, faces=anodeMesh.faces, color=(0.7216, 0.451, 0.2, 1))
        self.view.add(anode)

        # ****************** End of vacuum tube assembly *****************************

        # Add phosphor screen
        phosphorMesh = trimesh.load(r"Mesh/SPARC_phosphor.stl")
        phosphorScreen = vs.visuals.Mesh(vertices=phosphorMesh.vertices, faces=phosphorMesh.faces, color=(0, 1, 0, 1))
        phosphorScreen.attach(vv.filters.mesh.ShadingFilter(shading="smooth"))
        self.view.add(phosphorScreen)

        # ****************** End of canvas configuration *********************************
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

    def addTrajectory(self, Voltage: float):
        '''
        addTrajectory adds a curve from the vacuum tube to the phosphor screen simulating the trajectory of the electron
        beam. The curve will consist of 100 points. For the base configuraiton, this will just be a straight line.
        For the extensions, this function will need to use an extrapolating algorithm to generate points sequentially
        based on the equation of motion of the electrons. This function is a WIP and will preferably use a C++ library
        in the future for added efficiency.
        :param Voltage: voltage of the power source
        :return: numpy 3x100 array
        '''

        # Determine line width based on voltage
        V = 0
        if Voltage < 10000:
            V = 1
        if 10000 < Voltage & Voltage < 50000:
            V = 3
        if 50000 < Voltage:
            V = 5
        # Declare numpy arrays for the x,y, and z coordinates of points along the curve
        xcoords = np.zeros(100)
        ycoords = np.linspace(-3.65, 4.775, 100)
        zcoords = np.array([1.3 for x in range(0,100)])

        # Declare uninitialized 3x100 array to store points on curve
        curvePoints = np.empty(100,3)

        # Add coordinates to curve
        for i in range(0,100):
            (curvePoints[i])[0] = xcoords[i]
            (curvePoints[i])[1] = ycoords[i]
            (curvePoints[i])[2] = zcoords[i]

        # Create line in vispy and add it to scene canvas
        curve = vs.Line(curvePoints, colo="blue", width=V)
        self.view.add(curve)


if __name__ == '__main__':
    app = qt.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


