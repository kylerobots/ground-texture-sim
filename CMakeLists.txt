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

add_executable(data_writer
	src/data_writer_node.cpp
	src/DataWriter.cpp
)
target_include_directories(data_writer
	PRIVATE
		include
)
target_link_libraries(data_writer
	ignition-common${IGNITION_COMMON_VERSION}::ignition-common${IGNITION_COMMON_VERSION}-graphics
	ignition-math${IGNITION_MATH_VERSION}::core
	ignition-transport${IGNITION_TRANSPORT_VERSION}::core
)

add_executable(follow_trajectory
	src/follow_trajectory.cpp
	src/TrajectoryFollower.cpp
)
target_include_directories(follow_trajectory
	PRIVATE
		include
)
target_link_libraries(follow_trajectory)

add_executable(keyboard_controller
	src/keyboard_controller_node.cpp
	src/KeyboardController.cpp
)
target_include_directories(keyboard_controller
	PRIVATE
		include
)
target_link_libraries(keyboard_controller
	ignition-transport${IGNITION_TRANSPORT_VERSION}::core
)

# Specify installation information
install(
	TARGETS
		data_writer
		follow_trajectory
		keyboard_controller
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
	# Unit test for the keyboard
	add_executable(test_keyboard_controller
		test/test_keyboard_controller.cpp
		src/KeyboardController.cpp
	)
	target_include_directories(test_keyboard_controller
		PRIVATE
			include
	)
	target_link_libraries(test_keyboard_controller
		ignition-transport${IGNITION_TRANSPORT_VERSION}::core
		gtest_main
	)
	add_test(KeyboardController test_keyboard_controller)
		
	# Unit test for the trajectory
	add_executable(test_trajectory_follower
		test/test_trajectory_follower.cpp
		src/TrajectoryFollower.cpp
	)
	target_include_directories(test_trajectory_follower
		PRIVATE
			include
	)
	target_link_libraries(test_trajectory_follower
		gtest_main
	)
	add_test(TrajectoryFollower test_trajectory_follower)
			
endif(BUILD_TESTING)