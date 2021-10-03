cmake_minimum_required(VERSION 3.1)
project(boringssl CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if (CMAKE_SYSTEM_NAME STREQUAL "iOS")

if (NOT CONAN_SETTINGS_OS_SDK STREQUAL "iphonesimulator")
set(ENABLE_IOS_BITCODE TRUE)
endif()

if(ENABLE_IOS_BITCODE)
# enable bitcode
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fembed-bitcode")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fembed-bitcode")
set(CMAKE_ASM_FLAGS "${CMAKE_ASM_FLAGS} ${CMAKE_C_FLAGS}")
endif()

endif()

add_subdirectory(boringssl)
