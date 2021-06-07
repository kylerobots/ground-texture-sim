cmake_minimum_required(VERSION 3.0.0)
project(ground-texture-sim
	VERSION 1.0.0
	DESCRIPTION "A simulation to generate ground texture data for monocular SLAM."
	HOMEPAGE_URL https://github.com/kylerobots/ground-texture-sim
	LANGUAGES CXX
)

find_package(ignition-transport10 REQUIRED)
set(IGN_TRANSPORT_VER ${ignition-transport10_VERSION_MAJOR})

add_executable(keyboard_controller
	src/keyboard_controller.cpp
)
target_link_libraries(keyboard_controller
	ignition-transport${IGN_TRANSPORT_VER}::core
)