[![Build Status](https://travis-ci.org/eliaskousk/conan-curl-cpp.svg?branch=release/latest)](https://travis-ci.org/eliaskousk/conan-curl-cpp)

# conan-curl-cpp

[Conan.io](https://conan.io) package for CURL C++ Client library

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py
    
## Upload packages to server

    $ conan upload curl-cpp/latest@eliaskousk/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install curl-cpp/latest@eliaskousk/stable/
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    curl-cpp/latest@latest/stable

    [options]

    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files
*conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that
you need to link with your dependencies.
