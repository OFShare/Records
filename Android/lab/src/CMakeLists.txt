cmake_minimum_required(VERSION 3.0)
project(main)

add_definitions("-Wall -g -std=c++11")

include_directories(${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/../simple_libs/)

add_executable(${PROJECT_NAME} main.cc)

set(hello "${CMAKE_CURRENT_SOURCE_DIR}/../simple_libs/android_release_v8a/libhello.so")
target_link_libraries(${PROJECT_NAME} ${hello})
