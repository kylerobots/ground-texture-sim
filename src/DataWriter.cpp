#include "DataWriter.h"

namespace ground_texture_sim {
	DataWriter::DataWriter() {
	}

	void DataWriter::registerCameraInfo(const ignition::msgs::CameraInfo & msg) {
		// This is a straightforward write.
		current_camera_info = msg;
	}

	void DataWriter::registerImage(const ignition::msgs::Image & msg) {
		// First, convert the image to something writeable.
	}

	void DataWriter::registerPose(const ignition::msgs::Pose_V & msg) {
		// This is a list of poses, so find the one for the camera.
		for (int i = 0; i < msg.pose_size(); ++i) {
			if (msg.pose(i).name() == "camera") {
				current_pose = msg.pose(i);
			}
		}
	}
} // namespace ground_texture_sim
