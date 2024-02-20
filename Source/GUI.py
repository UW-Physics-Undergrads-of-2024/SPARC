from time import process_time
from sys import argv
import trimesh
import PyQt6.QtGui as QtGui
import PyQt6.QtWidgets as Qt
import SPARC
import numpy as np
import vispy.scene as vs
import vispy.visuals as vv


class MainWindow(Qt.QMainWindow):
    """
    A class to generate a GUI app.

    Attributes
    ----------
    centralWidget: PyQt6.QWidget
        The main widget that everything else on the GUI is embedded in

    topLevelLayout: PyQt6.QVBoxLayout
        A vertically oriented layout that several sub-layout's will be embedded in

    canvasLayout: PyQt6.QHBoxLayout
        A layout that the vispy SceneCanvas will be embedded in

    inputLayout: PyQt6.QGridLayout
        A layout that interactive widgets will be embedded in

    canvas: vispy.SceneCanvas
        A vispy SceneCanvas used to render meshes of the SPARC apparatus and curves that simulate the electron beam


    Methods
    -------
    add_trajectory: Returns None
        Updates the vispy canvas with a curve representing the trajectory of the electron beam

    """

    def __init__(self):
        super().__init__()

        # set window icon
        self.setWindowIcon(QtGui.QIcon('icon_temp.png'))

        # Set basic dimensions and attributes
        self.setWindowTitle("SPARC Visualizer")
        self.setGeometry(100, 100, 600, 600)
        self.centralWidget = Qt.QWidget()
        palette = self.centralWidget.palette()
        palette.setColor(self.centralWidget.backgroundRole(), QtGui.QColor(0, 0, 139, 255))
        self.centralWidget.setPalette(palette)

        # Create layouts
        self.topLevelLayout = Qt.QVBoxLayout()
        self.canvasLayout = Qt.QHBoxLayout()
        self.inputLayout = Qt.QGridLayout()

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
        transform = vv.transforms.STTransform(translate=(-5, -5), scale=(1, 1, 1, 1))
        affine = transform.as_matrix()
        axis.transform = affine

        # Set initial camera position and orientation
        self.view.camera.azimuth = -15
        self.view.camera.elevation = 30
        self.view.camera.distance = 15

        # Add board that all components will be mounted on
        board_mesh = trimesh.load(r"Mesh/SPARC_board.stl")
        board = vs.visuals.Mesh(vertices=board_mesh.vertices, faces=board_mesh.faces, color=(0.8, 0.4, 0, 1))
        board.attach(vv.filters.mesh.ShadingFilter(shading="smooth", ))
        self.view.add(board)

        # Add vacuum tube assembly to view
        vacuum_mesh = trimesh.load(r"Mesh/SPARC_vacuum.stl")
        vacuum = vs.visuals.Mesh(vertices=vacuum_mesh.vertices, faces=vacuum_mesh.faces, color='blue')
        vacuum.attach(vv.filters.Alpha(0.2))  # makes mesh semi-transparent
        vacuum.attach(vv.filters.mesh.ShadingFilter(shading="smooth"))
        self.view.add(vacuum)

        # ****************** Add vacuum tube assembly to view ***************************

        # Add vacuum tube itself
        vacuum_mount_mesh = trimesh.load(r"Mesh/SPARC_vacuum_mount.stl")
        vacuum_mount = vs.visuals.Mesh(vertices=vacuum_mount_mesh.vertices, faces=vacuum_mount_mesh.faces,
                                       color=(1, 1, 0.6, 1))
        vacuum_mount.attach(vv.filters.mesh.ShadingFilter(shading="smooth"))
        self.view.add(vacuum_mount)

        # Add copper coil anode
        anode_mesh = trimesh.load(r"Mesh/SPARC_vacuum_anode.stl")
        anode = vs.visuals.Mesh(vertices=anode_mesh.vertices, faces=anode_mesh.faces, color=(0.7216, 0.451, 0.2, 1))
        self.view.add(anode)

        # ****************** End of vacuum tube assembly *****************************

        # Add phosphor screen
        phosphor_mesh = trimesh.load(r"Mesh/SPARC_phosphor.stl")
        phosphor_screen = vs.visuals.Mesh(vertices=phosphor_mesh.vertices, faces=phosphor_mesh.faces,
                                          color=(0, 1, 0, 1))
        phosphor_screen.attach(vv.filters.mesh.ShadingFilter(shading="smooth"))
        self.view.add(phosphor_screen)

        # ****************** Add trajectory curve ****************************************

        # Declare numpy array for the x,y, and z coordinates of points along the curve
        # Array is left uninitialized. This is because the curve will only be rendered
        # when the setScene button is clicked, not when the app is loaded.
        curve_points = np.empty([1, 3])
        self.curve = vs.Line(curve_points, color="blue", width=1)
        self.view.add(self.curve)

        # ****************** End of trajectory curve *************************************

        # ****************** End of canvas configuration *********************************

        # Add labelled combo box for voltage
        self.labelVoltage = Qt.QLabel(self)
        self.labelVoltage.setText("Voltage (kilovolt)")
        self.labelVoltage.setStyleSheet("border: 1px solid black;")
        self.inputLayout.layout().addWidget(self.labelVoltage, 0, 0)

        self.voltageSelector = Qt.QComboBox(self)
        self.voltageSelector.addItems(["10", "20", "50"])
        self.inputLayout.layout().addWidget(self.voltageSelector, 0, 1)

        # Add labelled combo box for magnetic flux density
        self.labelMagneticField = Qt.QLabel(self)
        self.labelMagneticField.setText("B Field (Teslas)")
        self.labelMagneticField.setStyleSheet("border: 1px solid black;")
        self.inputLayout.layout().addWidget(self.labelMagneticField, 1, 0)

        self.BFieldSelector = Qt.QComboBox(self)
        self.BFieldSelector.addItems(["0", "0.001", "0.01"])
        self.inputLayout.layout().addWidget(self.BFieldSelector, 1, 1)

        # Add button widget to load scene
        self.setSceneButton = Qt.QPushButton(self)
        self.setSceneButton.setText("Load Scene")
        # addWidget(QWidget, row, column, rowSpan, columnSpan)
        self.inputLayout.layout().addWidget(self.setSceneButton, 2, 0, 1, 2)

        # Add connection
        self.setSceneButton.clicked.connect(lambda:
                                            self.add_trajectory(voltage=self.voltageSelector.currentText(),
                                                                magnetic_field=self.BFieldSelector.currentText()))

    def add_trajectory(self, voltage: str, magnetic_field: str) -> None:
        """
        Summary
        -------
        addTrajectory adds a curve from the vacuum tube to the phosphor screen simulating the trajectory of the electron
        beam. The curve will consist of 100 points. For the base configuration, this will just be a straight line.
        For the extensions, this function will need to use an extrapolating algorithm to generate points sequentially
        based on the equation of motion of the electrons.

        Note
        ----
        This function utilizes a custom library SPARC coded natively in C++, which is an ongoing work in progress and
        isn't configured to return meaningful error messages. Errors produced from running this function will always
        trace back to the SPARC library. Since configuring an IDE to debug Python and C++ simultaneously, it's
        recommended to build a test project using the C++ source code and run the native code within the test project
        to debug it.

        :param voltage: string representation of float value from QComboBox widget
        :param magnetic_field: string representation float value from QComboBox widget

        :return: None
        """

        start = process_time()

        voltage_input = float(voltage) * 10 ** 3
        b_field = float(magnetic_field)

        curve_points = np.array(SPARC.classical_beam(voltage_input, b_field))
        # Create line in vispy and add it to scene canvas
        self.curve.set_data(curve_points, width=voltage_input)
        end = process_time()
        print(end - start)


if __name__ == '__main__':
    app = Qt.QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()
