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
py::array_t<double> classicalBeam(const int& voltage)
{
	double position[100][3];
	double velocity[99][3];
	double acceleration[98][3];

	for (unsigned int i = 0; i < 3; i++)
	{
		position[0][i] = 0;
		velocity[0][i] = 0;
		acceleration[0][i] = 0;
	}

	py::ssize_t size = 100;
	py::array_t<double> beam = py::array_t(100);

	return beam;
}