cmake_minimum_required(VERSION 2.8)
project(KT C)

set(GKLIB_PATH "GKlib" CACHE PATH "path to GKlib")
set(SHARED FALSE CACHE BOOL "build a shared library")

if(MSVC)
  set(KT_INSTALL FALSE)
else()
  set(KT_INSTALL TRUE)
endif()

# Add GKlib's cmake settings
include(${GKLIB_PATH}/GKlibSystem.cmake)

# -restrict with Intel compiler
if(${CMAKE_C_COMPILER_ID} STREQUAL "Intel")
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -restrict")
endif()

# Source files
file(GLOB kt_sources src/*.c)

# Include directories
include_directories(${GKLIB_PATH})

# Build
add_executable(ktruss ${GKlib_sources} ${kt_sources})

# Install
if(KT_INSTALL)
  install(TARGETS ktruss
    RUNTIME DESTINATION bin)
endif()
