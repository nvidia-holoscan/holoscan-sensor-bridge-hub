# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.24)
project(adi_sensors LANGUAGES CXX CUDA)

find_package(holoscan 4.4 REQUIRED CONFIG PATHS "/opt/nvidia/holoscan")
find_package(CUDAToolkit REQUIRED)

set(HSB_SOURCE_DIR "/opt/hsb" CACHE PATH "HSB source checkout prepared with prepare_hsb.py")
if(NOT EXISTS "${HSB_SOURCE_DIR}/src/hololink/core/CMakeLists.txt")
  message(FATAL_ERROR
    "Set HSB_SOURCE_DIR to an HSB checkout prepared with prepare_hsb.py. See README.md.")
endif()

# Use HSB targets to propagate include paths, CUDA, fmt, and receiver dependencies.
set(HOLOLINK_BUILD_EXAMPLES OFF CACHE BOOL "Build upstream examples")
set(HOLOLINK_BUILD_TESTS OFF CACHE BOOL "Build upstream tests")
set(HOLOLINK_BUILD_TOOLS OFF CACHE BOOL "Build upstream tools")
set(HOLOLINK_BUILD_ROCE OFF CACHE BOOL "Build RoCE receivers")
set(HOLOLINK_BUILD_GPUNETIO_ROCE OFF CACHE BOOL "Build DOCA receivers")
set(HOLOLINK_MODULE_BUILD_OPERATORS OFF CACHE BOOL "Build module operators")
set(HOLOLINK_BUILD_PYTHON ON CACHE BOOL "Build Hololink Python bindings")
set(HOLOLINK_PYTHON_INSTALL_DIR "python" CACHE PATH "Python installation directory")
list(APPEND CMAKE_MODULE_PATH "${HSB_SOURCE_DIR}/cmake")
include(hololink_deps/fmt)
include(hololink_deps/pybind11)
add_subdirectory("${HSB_SOURCE_DIR}" hsb)

add_subdirectory(aditof)
add_subdirectory(adi_imu)
add_subdirectory(a2baudio)

include(CTest)
if(BUILD_TESTING)
  add_test(NAME adi_tof_help COMMAND adcam_player --help)
  add_test(NAME adi_audio_help COMMAND audio_viz_disp --help)
  set_tests_properties(adi_tof_help adi_audio_help PROPERTIES TIMEOUT 30)
endif()
