cmake_minimum_required(VERSION 3.0.0)
project(ground-texture-sim
	VERSION 1.1.0
	DESCRIPTION "A simulation to generate ground texture data for monocular SLAM."
	HOMEPAGE_URL https://github.com/kylerobots/ground-texture-sim
	LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 11)

# Specify which versions of Ignition components to load.
set(IGNITION_COMMON_VERSION 4)
set(IGNITION_MATH_VERSION 6)
set(IGNITION_TRANSPORT_VERSION 10)

find_package(ignition-common${IGNITION_COMMON_VERSION} REQUIRED COMPONENTS graphics)
find_package(ignition-math${IGNITION_MATH_VERSION} REQUIRED)
find_package(ignition-transport${IGNITION_TRANSPORT_VERSION} REQUIRED)

add_executable(keyboard_controller
	src/keyboard_controller_node.cpp
	src/KeyboardController.cpp
)
target_include_directories(keyboard_controller
	PUBLIC
	include
)
target_link_libraries(keyboard_controller
	ignition-transport${IGNITION_TRANSPORT_VERSION}::core
)

add_executable(data_writer
	src/data_writer_node.cpp
	src/DataWriter.cpp
)
target_include_directories(data_writer
	PUBLIC
	include
)
target_link_libraries(data_writer
	ignition-common${IGNITION_COMMON_VERSION}::ignition-common${IGNITION_COMMON_VERSION}-graphics
	ignition-math${IGNITION_MATH_VERSION}::core
	ignition-transport${IGNITION_TRANSPORT_VERSION}::core
)

# Specify installation information
install(
	TARGETS
		keyboard_controller
		data_writer
)

# Use Google Test for unit testing. This could probably be compiled in the image, but this was easier to implement.
include(CTest)
if(BUILD_TESTING)
	include(FetchContent)
	FetchContent_Declare(
		google_test
		GIT_REPOSITORY https://github.com/google/googletest.git
		GIT_TAG master
		GIT_SHALLOW true
		)
		FetchContent_MakeAvailable(google_test)
		add_executable(unit_tests
		test/test_keyboard_controller.cpp
		src/KeyboardController.cpp
		)
		target_include_directories(unit_tests
		PUBLIC
		include
		)
		target_link_libraries(unit_tests
		ignition-transport${IGNITION_TRANSPORT_VERSION}::core
		gtest_main
		)
	add_test(UnitTests unit_tests)
endif(BUILD_TESTING)