cmake_minimum_required(VERSION 3.0.0)
project(ground-texture-sim
	VERSION 2.0.0
	DESCRIPTION "A simulation to generate ground texture data for monocular SLAM."
	HOMEPAGE_URL https://github.com/kylerobots/ground-texture-sim
	LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)

# Specify which versions of Ignition components to load.
set(IGNITION_COMMON_VERSION 4)
set(IGNITION_MATH_VERSION 6)
set(IGNITION_MSGS_VERSION 7)
set(IGNITION_TRANSPORT_VERSION 10)

find_package(ignition-common${IGNITION_COMMON_VERSION} REQUIRED COMPONENTS graphics)
find_package(ignition-math${IGNITION_MATH_VERSION} REQUIRED)
find_package(ignition-msgs${IGNITION_MSGS_VERSION} REQUIRED)
find_package(ignition-transport${IGNITION_TRANSPORT_VERSION} REQUIRED)

add_library(ground_texture_sim
	src/ground_texture_sim/DataWriter.cpp
)
target_include_directories(ground_texture_sim
	PRIVATE
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include/ground_texture_sim>
  		$<INSTALL_INTERFACE:include/ground_texture_sim>
)
target_link_libraries(ground_texture_sim
	ignition-common${IGNITION_COMMON_VERSION}::ignition-common${IGNITION_COMMON_VERSION}-graphics
	ignition-math${IGNITION_MATH_VERSION}::core
	ignition-msgs${IGNITION_MSGS_VERSION}::core
)

# add_executable(data_writer
# 	src/data_writer_node.cpp
# 	src/ground_texture_sim/DataWriter.cpp
# )
# target_include_directories(data_writer
# 	PRIVATE
# 		include/ground_texture_sim
# )
# target_link_libraries(data_writer
# 	ignition-common${IGNITION_COMMON_VERSION}::ignition-common${IGNITION_COMMON_VERSION}-graphics
# 	ignition-math${IGNITION_MATH_VERSION}::core
# 	ignition-transport${IGNITION_TRANSPORT_VERSION}::core
# )

# add_executable(follow_trajectory
# 	src/follow_trajectory.cpp
# 	src/ground_texture_sim/DataSynchronizer.cpp
# 	src/ground_texture_sim/DataWriter.cpp
# 	src/ground_texture_sim/TrajectoryFollower.cpp
# )
# target_include_directories(follow_trajectory
# 	PRIVATE
# 		include/ground_texture_sim
# )
# target_link_libraries(follow_trajectory
# 	ignition-common${IGNITION_COMMON_VERSION}::ignition-common${IGNITION_COMMON_VERSION}-graphics
# 	ignition-math${IGNITION_MATH_VERSION}::core
# 	ignition-msgs${IGNITION_MSGS_VERSION}::core
# 	ignition-transport${IGNITION_TRANSPORT_VERSION}::core
# )

# add_executable(keyboard_controller
# 	src/keyboard_controller_node.cpp
# 	src/ground_texture_sim/KeyboardController.cpp
# )
# target_include_directories(keyboard_controller
# 	PRIVATE
# 		include/ground_texture_sim
# )
# target_link_libraries(keyboard_controller
# 	ignition-transport${IGNITION_TRANSPORT_VERSION}::core
# )

# Specify installation information
# install(
# 	TARGETS
# 		data_writer
# 		follow_trajectory
# 		keyboard_controller
# )

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
	# add_executable(test_keyboard_controller
	# 	test/test_keyboard_controller.cpp
	# 	src/ground_texture_sim/KeyboardController.cpp
	# )
	# target_include_directories(test_keyboard_controller
	# 	PRIVATE
	# 		include/ground_texture_sim
	# )
	# target_link_libraries(test_keyboard_controller
	# 	ignition-transport${IGNITION_TRANSPORT_VERSION}::core
	# 	gtest_main
	# )
	# add_test(KeyboardController test_keyboard_controller)
		
	# # Unit test for the trajectory
	# add_executable(test_trajectory_follower
	# 	test/test_trajectory_follower.cpp
	# 	src/ground_texture_sim/DataSynchronizer.cpp
	# 	src/ground_texture_sim/DataWriter.cpp
	# 	src/ground_texture_sim/TrajectoryFollower.cpp
	# )
	# target_include_directories(test_trajectory_follower
	# 	PRIVATE
	# 		include/ground_texture_sim
	# )
	# target_link_libraries(test_trajectory_follower
	# 	gtest_main
	# 	ignition-common${IGNITION_COMMON_VERSION}::ignition-common${IGNITION_COMMON_VERSION}-graphics
	# 	ignition-math${IGNITION_MATH_VERSION}::core
	# 	ignition-msgs${IGNITION_MSGS_VERSION}::core
	# 	ignition-transport${IGNITION_TRANSPORT_VERSION}::core
	# )
	# add_test(TrajectoryFollower test_trajectory_follower)

	# add_executable(test_data_synchronizer
	# 	test/test_data_synchronizer.cpp
	# 	src/ground_texture_sim/DataSynchronizer.cpp
	# )
	# target_include_directories(test_data_synchronizer
	# 	PRIVATE
	# 		include/ground_texture_sim
	# )
	# target_link_libraries(test_data_synchronizer
	# 	gtest_main
	# 	ignition-msgs${IGNITION_MSGS_VERSION}::core
	# 	ignition-transport${IGNITION_TRANSPORT_VERSION}::core
	# )
	# add_test(DataSynchronizer test_data_synchronizer)

	add_executable(test_data_writer
		test/test_data_writer.cpp
	)
	target_include_directories(test_data_writer
		PRIVATE
			include/ground_texture_sim
	)
	target_link_libraries(test_data_writer
		gtest_main
		ground_texture_sim
	)
	add_test(DataWriter test_data_writer)

	add_executable(test_transform_math
		test/test_transform_math.cpp
	)
	target_include_directories(test_transform_math
		PRIVATE
			include/ground_texture_sim
	)
	target_link_libraries(test_transform_math
		gtest_main
		ground_texture_sim
	)
	add_test(TransformMath test_transform_math)
			
endif(BUILD_TESTING)