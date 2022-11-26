# SPARC
Visualization software for the Student Particle Accelerator Reproduction Complex. The program generates a 3D render of the electron beam's path through the magnetic field in the SPARC apparatus.

The python implementation of this program will use PyQt6 to create a GUI app. The GUI will consist of at least one page with a 3D viewer widget that displays a rendering of the SPARC apparatus and the trajectory the electron beam is expected to take. It will have widgets for controlling the viewing angle and the parameters being simulated. Upon loading, the app will generate all the curves corresponding with each set of inputs and the objects associated with that combination of inputs into the 3D viewer. 

There are two main components to this software that need to be completed. The first is to develop an interactable app with a GUI and widgets for selecting the parameters of SPARC to simulate. This will require building a GUI with space allotted for a 3D viewer and wdigets to input the parameters. The 3D viewer will be made with Vispy. The render will be scaled properly to create an accurate representation of the apparatus. The second major component is to code a script that will generate the curve representing the electron beam. This will require an understanding of how to model electron trajectories given various electromagnetic interactions. 

All documentation for the software, the hardware, and the underlying physics can be found in the Wiki page.

Within the source folder is all the source code used to build this program. The main.py file is the source code for the entire project. To allow different components to be developed in parallel, there are additional subfolders containing files related to each of the three main components listed above. With each successive iteration of the python scripts for each component, we will append or update the scripts contained in the main file. 

Additional information can be found in the wiki for this repository.

Build Instruction
-----------------
The app is not yet completed for build purposes.
