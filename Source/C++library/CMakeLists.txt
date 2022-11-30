cmake_minimum_required(VERSION 3.20)
set(CMAKE_CXX_STANDARD 20)
project(Trajectory)

# Add an option to either build a VS solution or a python module
option(BUILD_VS_PROJECT "Build VS solution project" ON)

# build visual studio project to test library
if(BUILD_VS_PROJECT)
	set(SOURCE_FILES Trajectory.h Test.cpp)
	add_executable(Trajectory ${SOURCE_FILES})
	target_include_directories(Trajectory PRIVATE ${EXTERNAL_LIB_HEADERS})
	target_compile_features(Trajectory PUBLIC cxx_std_20)
else()
	add_subdirectory(pybind11)
	pybind11_add_module(Trajectory Trajectory.cpp)
endif()


