## CMake configuration 
The CMakeLists.txt is used to build either a Visual Studios project used for building the python library. Create a new folder for building your VS project in and open that directory in a terminal. Use the following command:
```console
cmake ../
```


## Initiate pybind11 submodule
If you clone or pull the repository and the pybind11 folder is empty, use:
```console
git submodule init
```
```console
git submodule update
```