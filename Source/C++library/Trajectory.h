#include <pybind11.h>
#include <numpy.h>
#include <cmath> // exponential

namespace py = pybind11;

const double mass_electron = 9.1093837015*std::pow(10, -31);
const double charge_electron = -1.602176634 * std::pow(10, -19);


/**
* @brief classicalBeam calculates the trajectory the electrons take and returns it as a set of 100 points
* stored in a python array.
*
* @param voltage is the voltage between the electrodes
*
* @return beam is the 100x3 numpy array representing points along the trajectory of the electron
*/
py::array_t<double> classicalBeam(const int& voltage);

