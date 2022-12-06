#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"
#include "Trajectory.h"
#include <functional>


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

// Hours wasted on PYBIND11_MODULE Bug: 7
// Fixed: Don't try to build an executable using CMake like a dumbass

PYBIND11_MODULE(Trajectory, trajectory)
{
	trajectory.doc() = "This is some module docs";
	trajectory.def("some_fn_python_name", &classicalBeam);
}