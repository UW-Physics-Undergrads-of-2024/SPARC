#include "pybind11/pybind11.h"
#include "pybind11/numpy.h"
#include "Trajectory.h"
#include <functional>


namespace py = pybind11;

py::array_t<double> classicalBeam(const int& voltage)
{
	std::vector<std::vector<double>> position;
	std::vector<double> next_position;
	std::vector<double> velocity;

	// Electron starts at the origin at rest
	position[0] = {0,0,0};


	// The separation between the electrodes, which are parallel plates, is 5cm
	// To get the electric field, we simply divide the voltage by the separation 
	// and the quotient scaled by negative one is the electric field strength
	double EField = -capacitor_gap / voltage; // the separation is in meters and the voltage in volts
	double CoulombsForce = EField * charge_electron;


	velocity[0] = 0;
	velocity[1] = delta * CoulombsForce / mass_electron;
	velocity[2] = 0;

	while (position.back()[1] != 0.5)
	{
		for (uint16_t i; i < 3; i++)
		{
			next_position[i] = position.back()[i] + velocity[i] * delta;

		}
		position.push_back(next_position);
	}
	py::array_t<double> beam = py::array_t<double>();

	return beam;
}

// Hours wasted on PYBIND11_MODULE Bug: 7
// Fixed: Don't try to build an executable using CMake like a dumbass

PYBIND11_MODULE(Trajectory, trajectory)
{
	trajectory.doc() = "";
	trajectory.attr("mass_electron") = py::cast(mass_electron);
	trajectory.attr("charge_electron") = py::cast(charge_electron);
	trajectory.attr("capacitor_gap") = py::cast(capacitor_gap);
	trajectory.attr("delta") = py::cast(delta);
	trajectory.attr("b_field") = py::cast(b_field);
}