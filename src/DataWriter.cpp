#include "DataWriter.h"

namespace ground_texture_sim {
	DataWriter::DataWriter() {
		image_count = 0;
	}

	void DataWriter::registerCameraInfo(const ignition::msgs::CameraInfo & msg) {
		// This is a straightforward write.
		current_camera_info = msg;
	}

	void DataWriter::registerImage(const ignition::msgs::Image & msg) {
		// Use Ignition's Image class from the Common package to handle writing.
		ignition::common::Image image;
		// The pixel formats use the exact same options, but they are different enums, so convert manually.
		ignition::common::Image::PixelFormatType pixel_format;
		switch (msg.pixel_format_type()) {
			case ignition::msgs::RGB_INT8:
				pixel_format = ignition::common::Image::RGB_INT8;
				break;
			default:
				std::cerr << "Unknown pixel type: " << msg.pixel_format_type() << std::endl;
				return;
		}
		// Convert the data from signed char to unsigned.
		std::vector<unsigned char> data(msg.data().begin(), msg.data().end());
		// Load the data into the image.
		image.SetFromData(&data[0], msg.width(), msg.height(), pixel_format);
		// Create the right filename.
		char buffer[11];
		snprintf(buffer, 11, "%06d.png", image_count);
		std::string filename = std::string(buffer);
		std::cout << "Saving: " << filename << std::endl;
		// Write it to file.
		image.SavePNG(filename);
		image_count++;
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
