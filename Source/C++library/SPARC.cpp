#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "SPARC.h"


namespace py = pybind11;

std::vector<std::vector<double>> classicalBeam(const double& voltage, const double& b_field)
{
	// Todo: try to re-implement this algorithm using eigen matrices 
	
	py::gil_scoped_release release;

	// The electron starts at the origin at rest
	std::vector<std::vector<double>> positionSet = { {0,0,0} };
	std::vector<double> velocity = { {0,0,0} };
	
	// The initial acceleration IS NOT zero, but we need to initialize this vector first
	// so it is padded with zeroes and its values will be changed before the first use
	// of the acceleration vector in subsequent calculations. Note that because the magnetic
	// field is parallel to the x-axis and the electric field is orthogonal to the x-axis,
	// then the acceleration in the x-direction is ALWAYS zero.
	std::vector<double> acceleration = { {0,0,0} };


	// The separation between the electrodes, which are parallel plates, is 10cm
	// To get the electric field, we simply divide the voltage by the separation 
	// and the quotient scaled by negative one is the electric field strength
	double EField = -capacitor_gap / voltage; // the separation is in meters and the voltage in volts
	double CoulombsForce = EField * charge_electron;

	
	// To generate the next point, the velocity is multiplied by the time interval
	// delta and then added to the last element of positionSet to get the next point
	std::vector<double> next_position = {
		positionSet.back()[0]+velocity[0]*delta, 
		positionSet.back()[1]+velocity[1]*delta,
		positionSet.back()[2]+velocity[2]*delta};

	// This process is repeated until the next point that is added is behind the 
	// phosphor screen. The velocity also needs to be updated in a similar manner
	// as the position. However, the past instances of velocity and acceleration
	// do not need to be tracked, so are kept as one dimensional vectors to be
	// overwritten in each loop.
	while (positionSet.back()[1] <= capacitor_gap)
	{
		positionSet.push_back(next_position);
		
		// Do cross product for Lorentz force qv x B
		acceleration[1] = (charge_electron * velocity[2] * b_field + CoulombsForce) / mass_electron;
		acceleration[2] = -charge_electron * velocity[1] * b_field / mass_electron;
		for (uint16_t i = 0; i < 3; i++)
		{
			next_position[i] = positionSet.back()[i] + velocity[i] * delta;
			velocity[i] = velocity[i] + acceleration[i] * delta;
		}
		
	}

	return positionSet;
}



// Hours wasted on PYBIND11_MODULE Bug: 7
// Fixed: Don't try to build an executable using CMake like a dumbass

PYBIND11_MODULE(SPARC, SPARC)
{
	SPARC.doc() = "";
	SPARC.attr("mass_electron") = py::float_(mass_electron);
	SPARC.attr("charge_electron") = py::float_(charge_electron);
	SPARC.attr("capacitor_gap") = py::float_(capacitor_gap);
	SPARC.attr("delta") = py::float_(delta);
	SPARC.def("classical_beam", [](const double& voltage, const double& b_field)
		{py::array out = py::cast(classicalBeam(voltage, b_field));
		 return out; });
}