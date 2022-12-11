cmake_minimum_required(VERSION 3.20)
set(CMAKE_CXX_STANDARD 20)
project(SPARC)
add_subdirectory(pybind11)
pybind11_add_module(SPARC SPARC.cpp SPARC.h)


