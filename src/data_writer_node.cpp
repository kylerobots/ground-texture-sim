#include "DataWriter.h"

#include <ignition/transport.hh>

int main(int argc, char ** argv) {
	ground_texture_sim::DataWriter writer;
	// Create a node for managing subscriptions.
	ignition::transport::Node node;
	std::string camera_topic = "/camera_info";
	std::string image_topic = "/camera";
	std::string pose_topic = "/world/ground_texture/dynamic_pose/info";
	// Connect each topic to the correct method in the writer.
	bool success = node.Subscribe(camera_topic, &ground_texture_sim::DataWriter::registerCameraInfo, &writer);
	if (!success) {
		std::cerr << "Error subscribing to topic [" << camera_topic << "]" << std::endl;
		return -1;
	}
	success = node.Subscribe(image_topic, &ground_texture_sim::DataWriter::registerImage, &writer);
	if (!success) {
		std::cerr << "Error subscribing to topic [" << image_topic << "]" << std::endl;
		return -1;
	}
	success = node.Subscribe(pose_topic, &ground_texture_sim::DataWriter::registerPose, &writer);
	if (!success) {
		std::cerr << "Error subscribing to topic [" << pose_topic << "]" << std::endl;
		return -1;
	}
	// The object handles everything, so just wait.
	ignition::transport::waitForShutdown();
	return 0;
}