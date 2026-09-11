# SPDX-FileCopyrightText: Copyright (c) 2022-2026, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

cmake_minimum_required(VERSION 3.20.1)
# Check if we can find a CXX compiler before enabling it
find_program(CXX_COMPILER_FOUND NAMES g++ clang++ c++)
if(CXX_COMPILER_FOUND)
  project(Holohub CXX)
else()
  project(Holohub NONE)
endif()

# Load shared helpers from the same pinned CLI used for build and run commands.
execute_process(
  COMMAND "${CMAKE_CURRENT_SOURCE_DIR}/hsb" version --json
  OUTPUT_VARIABLE _holoscan_cli_info
  COMMAND_ERROR_IS_FATAL ANY
)
string(JSON _holoscan_cli_main GET "${_holoscan_cli_info}" executable)
get_filename_component(HOLOSCAN_CLI_PACKAGE_DIR "${_holoscan_cli_main}" DIRECTORY)
list(APPEND CMAKE_MODULE_PATH
  "${HOLOSCAN_CLI_PACKAGE_DIR}/cmake"
  "${CMAKE_CURRENT_SOURCE_DIR}/cmake"
  "${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules"
)

# To configure which apps/operators to build
include(HoloHubConfigHelpers)

# Set install directory
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "${CMAKE_SOURCE_DIR}/install" CACHE PATH "Installation directory" FORCE)
endif()

# Set default build type to Release if not specified
if(NOT CMAKE_BUILD_TYPE)
  message(STATUS "Setting build type to 'Release' as none was specified.")
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build." FORCE)
endif()

# Enable Testing
include(CTest)

# Options
option(HOLOHUB_DOWNLOAD_DATASETS "Download datasets" ON)
option(HOLOHUB_BUILD_CPP "Build support for C++" ON)
option(HOLOHUB_BUILD_PYTHON "Build support for Python" ON)

# Enable flow benchmarking
option(FLOW_BENCHMARKING "Enable Flow Benchmarking" OFF)
if(FLOW_BENCHMARKING)
  set(FLOW_BENCHMARK_DIR "${CMAKE_BINARY_DIR}/flow_benchmarks")
  file(MAKE_DIRECTORY "${FLOW_BENCHMARK_DIR}")
endif()

if(HOLOHUB_BUILD_PYTHON)
  # Define and create a directory to store python operators under the holohub python module
  if(NOT CMAKE_INSTALL_LIBDIR)
    set(CMAKE_INSTALL_LIBDIR lib)
  endif()
  set(HOLOHUB_PYTHON_MODULE_OUT_DIR ${CMAKE_BINARY_DIR}/python/${CMAKE_INSTALL_LIBDIR}/holohub)
  file(MAKE_DIRECTORY ${HOLOHUB_PYTHON_MODULE_OUT_DIR})

  # Find the Python interpreter
  find_package(Python COMPONENTS Interpreter)
  set(PYTHON_EXECUTABLE ${Python_EXECUTABLE})
  # Set the Python executable for testing if not defined
  if(NOT DEFINED PYTHON_EXECUTABLE_TEST)
    set(PYTHON_EXECUTABLE_TEST ${Python_EXECUTABLE})
  endif()
endif()

# Set the default data directory
set(HOLOHUB_DATA_DIR "${CMAKE_BINARY_DIR}/data" CACHE PATH "Data Download directory")
set(CMAKE_INSTALL_RPATH
    "\$ORIGIN:\$ORIGIN/../../../lib:\$ORIGIN/../../lib:/opt/nvidia/holoscan/lib/")

# Set the default CUDA target platforms
if(NOT CMAKE_CUDA_ARCHITECTURES)
  set(CMAKE_CUDA_ARCHITECTURES "native")
endif()

# Build applications and operators
add_subdirectory(applications)
add_subdirectory(operators)
