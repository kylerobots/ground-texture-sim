#include <ignition/msgs.hh>
#include <ignition/transport.hh>
#include <iostream>
#include <string>

void keypressCallback(const ignition::msgs::Int32 & msg) {
	std::cout << "Heard: " << msg.data() << std::endl;
}

int main(int argc, char ** argv) {
	ignition::transport::Node node;
	std::string topic = "/keyboard/keypress";
	bool result = node.Subscribe(topic, keypressCallback);
	if (!result) {
		std::cerr << "Error subscribing to topic [" << topic << "]" << std::endl;
		return -1;
	}

	ignition::transport::waitForShutdown();

	return 0;
}