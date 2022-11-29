#include <pynind11/pybind11.h>
#include <Pybind11/numpy.h>
#include <cmath> // exponential

namespace py = pybind11;
constexpr double mass_electron = std::pow(9.1093837015, -31);

py::array_t<double> classicalBeam(const py::ssize_t& size, int& voltage)
{

}