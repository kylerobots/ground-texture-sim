#include "KeyboardController.h"

#include <atomic>
#include <csignal>
#include <ignition/transport.hh>
#include <iostream>
#include <string>

/// A flag to indicate when the program should finish.
static std::atomic<bool> terminate(false);

/**
 * @brief Set the cancel flag when called to end.
 * 
 * The function watches for signals from the user. If they correspond to a terminate signal, then the appropriate
 * termination flag is set by the function.
 * 
 * @param signal The signal received from the system.
 */
void signalHandler(int signal) {
	if (signal == SIGINT || signal == SIGTERM) {
		terminate.store(true);
	}
}

/**
 * @brief Start up the nodes and continue to publish messages.
 * 
 * The main function instantiates a controller, connects the incoming key presses to it, then continuously asks the
 * controller for messages to send to the simulation. The continues until the terminate flag indicates the node should
 * exit.
 * 
 * @param argc 
 * @param argv 
 * @return int 
 */
int main(int argc, char ** argv) {
	// Connect the terminate signals.
	std::signal(SIGINT, signalHandler);
	std::signal(SIGTERM, signalHandler);
	// Create a controller to determine velocities.
	ground_texture_sim::KeyboardController controller;
	// Create a node to send and receive from Ignition.
	ignition::transport::Node node;
	std::string keypress_topic = "/keyboard/keypress";
	std::string twist_topic = "/camera/cmd_vel";
	// Connect the incoming key press to the appropriate controller method for logging.
	bool success = node.Subscribe(keypress_topic, &ground_texture_sim::KeyboardController::registerKeypress, &controller);
	if (!success) {
		std::cerr << "Error subscribing to topic [" << keypress_topic << "]" << std::endl;
		return -1;
	}
	// Create a publisher to send back velocity commands.
	auto publisher = node.Advertise<ignition::msgs::Twist>(twist_topic);
	if (!publisher) {
		std::cerr << "Error advertising topic [" << twist_topic << "]" << std::endl;
		return -1;
	}

	// Now just loop until killed. At each loop, ask the controller to calculate the appropriate command.
	while (!terminate) {
		ignition::msgs::Twist msg = controller.createMessage();
		bool result = publisher.Publish(msg);
		if (!result) {
			std::cerr << "Unable to send twist message. Skipping..." << std::endl;
		}
		std::this_thread::sleep_for(std::chrono::milliseconds(500));
	}
	return 0;
}