import scipy as sp
import scipy.constants as scp
import numpy as np

def ClassicalBeam(V: int, LM: int, RM: int):
    '''
    ClassicalBeam takes the inputs of the SPARC apparatus and simulates the trajectory of the electron beam using
    non-relativistic models of physics

    :param V: Voltage input
    :param LM: Left Magnet Position
    :param RM:  Right Magnet Position
    :return: np.array
    '''

    # Define charge q_e and rest mass m_e of an electron
    q_e = (scp.physical_constants["elementary charge"])[0]
    m_e = scp.m_e

    # Find speed v_e of electron at the start of its trajectory
    v_e = np.sqrt(2*(V*q_e)/m_e)

    # Define initial velocity vector of electron. By convention, we will set the forward axis of the electron gun
    # assembly as the y-axis, with the direction of the right magnet being given by positive x-axis. By the right hand
    # rule, the z-axis will be vertically upward.
    vel_0 = np.array([0,v_e,0])

    # [code for defining magnetic field]

def RelativisticBeam(V: int, LM: int, RM: int):
    '''
    RelativisticBeam takes the inputs of the SPARC apparatus and simulates the trajectory of the electron beam using
    relativistic models of physics

    :param V: Voltage input
    :param LM: Left Magnet Position
    :param RM:  Right Magnet Position
    :return: np.array
    '''

    # Declare a constant for the speed of light
    CONST_c = scp.c

    # Define charge q_e and rest mass m_e of an electron
    q_e = (scp.physical_constants["elementary charge"])[0]
    m_e = scp.m_e

    # Find speed v_e of electron at the start of its trajectory
    v_e = CONST_c*np.sqrt(1-(1/(1+V*q_e/(m_e*CONST_c**2)))**2)

    # Define initial velocity vector of electron. By convention, we will set the forward axis of the electron gun
    # assembly as the y-axis, with the direction of the right magnet being given by positive x-axis. By the right hand
    # rule, the z-axis will be vertically upward.
    vel_0 = np.array([0,v_e,0])

    # [code for defining magnetic field]

if __name__ == '__main__':
    pass
