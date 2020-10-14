cmake_minimum_required(VERSION 3.0)
project(hello)

add_definitions("-Wall -g -std=c++11")

include_directories(${CMAKE_CURRENT_SOURCE_DIR})

add_library( 
        # Sets the name of the library.
        hello

        # Sets the library as a shared library.
        SHARED

        ${CMAKE_CURRENT_SOURCE_DIR}/hello.cc
        )
