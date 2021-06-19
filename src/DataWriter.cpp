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
		current_image = msg;
		writeData();
	}

	void DataWriter::registerPose(const ignition::msgs::Pose_V & msg) {
		// This is a list of poses, so find the one for the camera.
		for (int i = 0; i < msg.pose_size(); ++i) {
			if (msg.pose(i).name() == "camera") {
				current_pose = msg.pose(i);
			}
		}
	}

	void DataWriter::writeData() {
		// First, create the base filename from the image count index.
		char buffer[7];
		snprintf(buffer, 7, "%06d", image_count);
		std::string base_filename(buffer);

		// Then, write the image to file using Ignition's Image class, which already has the ability to write. The
		// types need converted though.
		ignition::common::Image image;
		// The pixel formats also need converted, even though the labels are exactly the same. The simulation only
		// outputs one type of format, so only convert that one for now.
		ignition::common::Image::PixelFormatType pixel_format;
		switch (current_image.pixel_format_type()) {
			case ignition::msgs::RGB_INT8:
				pixel_format = ignition::common::Image::RGB_INT8;
				break;
			default:
				std::cerr << "Unknown pixel type: " << current_image.pixel_format_type() << std::endl;
				return;
		}
		// The image data also needs loaded as an array of unsigned chars, so convert.
		std::vector<unsigned char> data(current_image.data().begin(), current_image.data().end());
		image.SetFromData(&data[0], current_image.width(), current_image.height(), pixel_format);
		// Write the image.
		image.SavePNG(base_filename + ".png");

		// Now write the latest pose to a file. This will require extracting the quaternion yaw value.
		double x = current_pose.position().x();
		double y = current_pose.position().y();
		double z = current_pose.position().z();
		ignition::math::Quaternion quaternion(current_pose.orientation().w(), current_pose.orientation().x(), current_pose.orientation().y(), current_pose.orientation().z());
		double roll = quaternion.Roll();
		double pitch = quaternion.Pitch();
		double yaw = quaternion.Yaw();
		// Write as a csv.
		std::ofstream pose_file;
		pose_file.open(base_filename + ".txt");
		pose_file << x << "," << y << "," << z << "," << roll << "," << pitch << "," << yaw << std::endl;
		pose_file.close();

		// Increment the image count to write new data next time.
		image_count++;
	}
} // namespace ground_texture_sim
