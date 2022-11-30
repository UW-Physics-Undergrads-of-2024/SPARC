cmake_minimum_required(VERSION 3.20)
set(CMAKE_CXX_STANDARD 20)
project(Trajectory)
add_subdirectory("..//..//extern//pybind11")


# Add an option to either build a VS solution or a python module
option(BUILD_VS_PROJECT "Build VS solution project" ON)

# build visual studio project to test library
if(BUILD_VS_PROJECT)
	set(SOURCE_FILES Trajectory.h Trajectory.cpp)
	add_executable(Trajectory ${SOURCE_FILES})
	target_link_libraries(Trajectory PRIVATE pybind11)
	target_compile_features(Trajectory PUBLIC cxx_std_20)
# build python module
else()
	pybind11_add_module(Trajectory Trajectory.cpp Trajectory.h)
endif()


