# SPARC
Visualization software for the Student Particle Accelerator Reduced-atmosphere Chamber. The program generates a 3D render of the electron beam's path through the magnetic field in the SPARC apparatus.

The python implementation of this program will use tkinter or an equivalent library to create a GUI app. The GUI will consist of at least one page with a 3D viewer widget that displays a plot and has buttons for controlling the viewing angle and the parameters being simulated. The app will allow the user to select a list of inputs for the magnets position, the voltage, and the amperage of the power source. Upon loading, the app will generate all the curves corresponding with each set of inputs and the objects associated with that combination of inputs into the 3D viewer. 

There are two main components to this software that need to be completed. The first (front-end) is to develop the front end of the app. This will require building a GUI with space allotted for a 3D viewer and buttons to control the camera angle and the parameters of the electron beam being simulated. The 3D viewer will be made with Vispy and programmed to have variable camera angles, can simulated blocks representing the magnets, and is scaled properly to create an accurate representation of the apparatus. The second major (back-end) component is to code a python script that will generate the curves representing electron trajectories. This will require an understanding of how to model electron trajectories through magnetic fields. 

A third, optional component, is to begin looking at developing a script that can run in the background to simulate the curves in real time to changes in the positioning of the magnets or changes to the voltage supply. The goal is to create a script that is fast enough to render at least 20 frames per second so that the apparatus being simulated isn't limited to a number of preset conditions. This will likely involve using a program written in another language that can be called from python. 

The documentation folder will contain files that document the physics involved that are modelled by the simulation. 

Within the source folder is all the source code used to build this program. The main.py file is the source code for the entire project. To allow different components to be developed in parallel, there are additional subfolders containing files related to each of the three main components listed above. With each successive iteration of the python scripts for each component, we will append or update the scripts contained in the main file. 

The build folder contains executables built from the source code that can be run on Windows. In the future, compatability with Mac and Linux is planned.
