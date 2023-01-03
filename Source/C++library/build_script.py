from os import listdir, system


def main() -> None:
    """
    Check if the pybind11 directory is empty or not and then build the build-environment in the build directory. If the
    directory is empty, the function will initiate and update the submodule to populate the pybind11 directory from the
    pybind11 GitHub repository.

    :return: None
    """

    path = "pybind11"

    # Python list of files in the pybind11 directory
    directory_contents = listdir(path)

    # Use implicit boolean value of empty structures in Python
    if not directory_contents:
        system("git submodule init")
        system("git submodule update")
        system(r"cmake -B/build/")

    else:
        system(r"cmake -B/build/")


if __name__ == "__main__":
    main()
