#include "KeyboardController.h"

#include <ignition/transport.hh>
#include <iostream>
#include <string>

int main(int argc, char ** argv) {
	ground_texture_sim::KeyboardController controller;
	ignition::transport::Node node;
	std::string topic = "/keyboard/keypress";
	bool success = node.Subscribe("/keyboard/keypress", &ground_texture_sim::KeyboardController::registerKeypress, &controller);
	if (!success) {
		std::cerr << "Error subscribing to topic [" << topic << "]" << std::endl;
		return -1;
	}
	ignition::transport::waitForShutdown();
	return 0;
}