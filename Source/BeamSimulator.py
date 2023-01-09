import scipy as sp
import scipy.constants as scp
import numpy as np


def relativistic_beam(voltage: float | int, magnetic_field: float | int) -> np.ndarray:
    """
    RelativisticBeam takes the inputs of the SPARC apparatus and simulates the trajectory of the electron beam using
    relativistic models of physics

    TODO: create preliminary script for generating curve using relativistic electrodynamic equations of motion

    :param voltage: voltage of the parallel plate capacitor
    :param magnetic_field: magnetic field permeating the space between the parallel plates
    :return: Array consisting of 3 column rows representing points along the trajectory of the electron beam
    """

    # Declare a constant for the speed of light
    c = scp.c


if __name__ == '__main__':
    pass
