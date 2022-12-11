import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qg
import vispy.scene as vs
import numpy as np
import vispy.visuals as vv
import time, sys, trimesh, linecache
import SPARC


class MainWindow(qt.QMainWindow):
    """
    A class to generate a GUI app.

    Attributes
    ----------
        centralWidget: PyQt6.QWidget
            The main widget that everything else on the GUI is embedded in

        topLavelLayout: PyQt6.QVBoxLayout
            A vertically oriented layout that several sub-layout's will be embedded in

        canvasLayout: PyQt6.QHBoxLayout
            A layout that the vispy SceneCanvas will be embedded in

        inputLayout: PyQt6.QGridLayout
            A layout that interactive widgets will be embedded in

        canvas: vispy.SceneCanvas
            A vispy SceneCanvas used to render meshes of the SPARC apparatus and curves that simulate the electron beam




    Methods
    -------

    """

    def __init__(self):
        super().__init__()

        # set window icon
        self.setWindowIcon(qg.QIcon('icon_temp.png'))

        # Set basic dimensions and attributes
        self.setWindowTitle("SPARC Visualizer")
        self.setGeometry(100, 100, 600, 600)
        self.centralWidget = qt.QWidget()
        palette = self.centralWidget.palette()
        palette.setColor(self.centralWidget.backgroundRole(), qg.QColor(0, 0, 139, 255))
        self.centralWidget.setPalette(palette)

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
        board = vs.visuals.Mesh(vertices=boardMesh.vertices, faces=boardMesh.faces, color=(0.8, 0.4, 0, 1))
        board.attach(vv.filters.mesh.ShadingFilter(shading="smooth", ))
        self.view.add(board)

        # Add vacuum tube assembly to view
        vacuumMesh = trimesh.load(r"Mesh/SPARC_vacuum.stl")
        vacuum = vs.visuals.Mesh(vertices=vacuumMesh.vertices, faces=vacuumMesh.faces, color='blue')
        vacuum.attach(vv.filters.Alpha(0.2))  # makes mesh semi-transparent
        vacuum.attach(vv.filters.mesh.ShadingFilter(shading="smooth"))
        self.view.add(vacuum)

        # ****************** Add vacuum tube assembly to view ***************************

        # Add vacuum tube itself
        vacuumMountMesh = trimesh.load(r"Mesh/SPARC_vacuum_mount.stl")
        vacuumMount = vs.visuals.Mesh(vertices=vacuumMountMesh.vertices, faces=vacuumMountMesh.faces,
                                      color=(1, 1, 0.6, 1))
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

        # ****************** Add trajectory curve ****************************************

        # Declare numpy array for the x,y, and z coordinates of points along the curve
        # Array is left uninitialized. This is because the curve will only be rendered
        # when the setScene button is clicked, not when the app is loaded.
        curvePoints = np.empty([1, 3])
        self.curve = vs.Line(curvePoints, color="blue", width=1)
        self.view.add(self.curve)

        # ****************** End of trajectory curve *************************************

        # ****************** End of canvas configuration *********************************

        # Add labelled combo box for voltage
        self.labelVoltage = qt.QLabel(self)
        self.labelVoltage.setText("Voltage (kilovolt)")
        self.labelVoltage.setStyleSheet("border: 1px solid black;")
        self.inputLayout.layout().addWidget(self.labelVoltage, 0, 0)

        self.voltageSelector = qt.QComboBox(self)
        self.voltageSelector.addItems(["10", "20", "50"])
        self.inputLayout.layout().addWidget(self.voltageSelector, 0, 1)

        # Add labelled combo box for magnetic flux density
        self.labelMagneticField = qt.QLabel(self)
        self.labelMagneticField.setText("B Field (Teslas)")
        self.labelMagneticField.setStyleSheet("border: 1px solid black;")
        self.inputLayout.layout().addWidget(self.labelMagneticField, 1, 0)

        self.magneticFieldSelector = qt.QComboBox(self)
        self.magneticFieldSelector.addItems(["0", "0.001", "0.01"])
        self.inputLayout.layout().addWidget(self.magneticFieldSelector, 1, 1)

        # Add button widget to load scene
        self.setSceneButton = qt.QPushButton(self)
        self.setSceneButton.setText("Load Scene")
        # addWidget(QWidget, row, column, rowSpan, columnSpan)
        self.inputLayout.layout().addWidget(self.setSceneButton, 2, 0, 1, 2)

        # Add connection
        self.setSceneButton.clicked.connect(lambda: self.addTrajectory(voltage=self.voltageSelector.currentText(),
                                                                       magneticField=self.magneticFieldSelector.currentText()))

    def addTrajectory(self, voltage: str, magneticField: str):
        """
        Summary
        -------
        addTrajectory adds a curve from the vacuum tube to the phosphor screen simulating the trajectory of the electron
        beam. The curve will consist of 100 points. For the base configuraiton, this will just be a straight line.
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
        :param magneticField: string representation float value from QComboBox widget

        :type voltage: str
        :type magneticField: str

        :return: None
        :rtype: None
        """

        # In the event of changes to the widgets on the GUI, the ability to convert the strings from the QComboBoxes
        # to floats will be tested in a try block
        V = 0
        b_field = 0
        try:
            V = float(voltage)
            b_field = float(magneticField)
        except ValueError:
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            print
            'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)

        # time the function
        start = time.time()

        # Determine line width based on voltage
        V = float(voltage)

        voltageInput = V * 10 ** 3
        b_field = float(magneticField)

        curvePoints = SPARC.classical_beam(voltageInput, b_field)
        # Create line in vispy and add it to scene canvas
        self.curve.set_data(curvePoints, width=V)
        end = time.time()
        print(end - start)


if __name__ == '__main__':
    app = qt.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
