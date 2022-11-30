#include <pybind11.h>
#include <numpy.h>
#include <cmath> // exponential
#include "Trajectory.h"

py::array_t<double> classicalBeam(const int& voltage)
{
	double position[100][3];
	double velocity[99][3];
	double acceleration[98][3];

	// Define the initial values of these quantities to be initially zero
	for (unsigned int i = 0; i < 3; i++)
	{
		position[0][i] = 0;
		velocity[0][i] = 0;
		acceleration[0][i] = 0;
	}

	py::array_t<double> beam = py::array_t<double>();

	return beam;
}