#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath> // exponential

namespace py = pybind11;

const double mass_electron = 9.1093837015 * std::pow(10, -31);
const double charge_electron = -1.602176634 * std::pow(10, -19);
constexpr double capacitor_gap = 0.10; // meters
constexpr double delta = 0.001; // time interval when numerically determining position
constexpr double b_field = 0.01; // magnetic flux density in the x-axis. Note that it is zero in the yz-plane

/**
* @brief classicalBeam calculates the trajectory the electrons take and returns it as a set of 100 points
* stored in a python array.
*
* @param voltage is the voltage between the electrodes
*
* @return beam is the 100x3 numpy array representing points along the trajectory of the electron
*/
py::array_t<double> classicalBeam(const int& voltage);