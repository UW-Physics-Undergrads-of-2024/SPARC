## CMake configuration 
The CMakeLists.txt is used to build either a Visual Studios project where the cpp file can be compiled and tested, or the python module using pybind11. To create a Visual Studios project, use the following command:
```console
cmake -D DBUILD_VS_PROJECT=ON ../
```

To build the python module, use:
```console
cmake -D DBUILD_VS_PROJECT=OFF ../
```

## Initiate pybind11 submodule
If you clone or pull the repository and the pybind11 folder is empty, use:
```console
git submodule update --init
```
