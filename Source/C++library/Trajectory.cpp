#include <pybind11.h>
#include <numpy.h>
#include <common.h>
#include "Trajectory.h"

namespace py = pybind11;

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

PYBIND11_MODULE(Trajectory, SPARC)
{
	SPARC.doc() = "A function that takes the voltage across the electrodes in the SPARC electron gun and produces a numpy array for the pointwise representation of the trajectory curve.";
	SPARC.def("trajectoryClassical", &classicalBeam);
}