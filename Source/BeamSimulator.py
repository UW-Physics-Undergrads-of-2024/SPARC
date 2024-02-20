import scipy.constants as scv
from scipy.integrate import odeint
import numpy as np
from collections.abc import Callable

# time interval for the simulated movement of electrons (units to be determined)
time_interval = np.linspace(0, 1, 1000)

# distance between electrodes in electron gun in meters
electrode_gap = 0.15


def uniform_fields_eom(pos_vel: np.array, time: float, charge: float = -scv.e, mass: float = scv.m_e,
                       voltage: float = 0, b_mag: float = 0, mag_pos: np.array = np.array([0, 0, 0])) -> np.array:
    """
    Returns the coupled system of ODEs for the cartesian components of a charged particle's position within a uniform
    EM field inside an EM accelerator. The second order vector ODE for the Lorentz force has been rewritten as a system
    of coupled first order ODEs. The electric field is approximated as that of a parallel plate capacitor. The axes are
    oriented such that the xy-plane is in the plane of "parallel plate electrodes" with the origin in the center of the
    anode while the z-axis is normal to theis plane and points in the direction of the cathode from the anode. The
    magnetic field is assumed to be purely in the xy-plane and is given by the projection of the displacement of the
    origin from the magnet onto the xy-plane, scaled by the field strength at the magnet.

    :param pos_vel: Array [p_x,p_y,p_z,v_x,v_y,v_z] of the cartesian components of the position and velocity
    :param time: Time input. scipy's odeint requires this argument to solve the system of EOMs over a given time
    interval
    :param charge: the charge of the particle, elementary electron charge by default
    :param mass: the mass of the particle, mass of an electron by default
    :param voltage: The potential difference between electrodes
    :param b_mag: the magnitude of a uniform B field in Teslas
    :param mag_pos: The position of the magnet
    :return: Array with each component being the EOM for the respective component of pos_vel
    """

    E = np.array([0, 0, voltage / electrode_gap], dtype=np.float32)

    # calculates the magnetic field
    origin = np.zeros(3, dtype=np.float32)
    BField = b_mag * origin - mag_pos

    return np.array([pos_vel[3],
                     pos_vel[4],
                     pos_vel[5],
                     (1/mass) * (charge * E[0] + pos_vel[4] * BField[2] - pos_vel[5] * BField[1]),
                     (1/mass) * (charge * E[1] + pos_vel[5] * BField[0] - pos_vel[5] * BField[2]),
                     (1/mass) * (charge * E[2] + pos_vel[3] * BField[1] - pos_vel[5] * BField[0])])


def classical_beam(voltage: float, mag_field: np.array, mag_pos: np.array, therm_emission_speed: float,
                   eom: Callable[[np.array, float, float, np.array, np.array], np.array]) -> np.array:
    """
    Calculates the trajectory of an electron that obeys some equation of motion within the electron gun
    :param voltage: potential difference between electrodes
    :param mag_field: strength of the magnetic field at the magnet
    :param mag_pos: position of the magnet
    :param therm_emission_speed: the speed at which electrons are ejected by the tungsten filament
    :param eom: callable ([p_x,p_y,p_z,v_x,v_y,v_z], t, charge, mass, voltage, [B_x,B_y,B_z]) that returns the coupled
    ODEs the electron obeys in a 1x6 array
    :return: Nx3 array [[x_0,y_0,z_0], [x_1,y_1,z_1], ...] for the position of the electron over the time interval
    """

    # Define charge q_e and rest mass m_e of an electron
    q_e = -scv.e

    # initial position and velocity of particle
    initial_conditions = np.array([0, 0, 0, 0, 0, therm_emission_speed])

    solved_system = odeint(eom, y0=initial_conditions, t=time_interval, args=(q_e, voltage, mag_field, mag_pos))

    return np.array([[x, y, z] for x in solved_system[:, 0] for y in solved_system[:, 1] for z in solved_system[:, 2]],
                    dtype=np.float32)


if __name__ == '__main__':
    pass
