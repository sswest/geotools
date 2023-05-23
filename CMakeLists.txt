cmake_minimum_required(VERSION 3.25)
project(geotools C)

set(CMAKE_C_STANDARD 99)

find_package(Python3 COMPONENTS Development NumPy)
include_directories(${Python3_INCLUDE_DIRS})
include_directories(${Python3_NumPy_INCLUDE_DIRS})

add_library(geotools src/geotools.c src/export.c src/export_vec.c)
