# preamble 
cmake_minimum_required(VERSION 3.4)

project(Trajectory)
add_subdirectory(../../pybind11)
pybind11_add_module(module_name Trajectory.h)