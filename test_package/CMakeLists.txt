cmake_minimum_required(VERSION 3.0)
PROJECT(MyHello)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

include(../cmake/detect.cpp11.cmake)

ADD_EXECUTABLE(mytest test.cpp)
TARGET_LINK_LIBRARIES(mytest ${CONAN_LIBS})
