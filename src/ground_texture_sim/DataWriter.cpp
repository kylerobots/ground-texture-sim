#include "DataWriter.h"

namespace ground_texture_sim {
	DataWriter::DataWriter() {
		this->index = 0;
		setDataFolder("");
	}

	DataWriter::DataWriter(const std::string & data_folder) {
		this->index = 0;
		setDataFolder(data_folder);
	}

	std::string DataWriter::getDataFolder(bool relative) const {
		return data_folder;
	}

	void DataWriter::setDataFolder(const std::string & data_folder) {
		this->data_folder = data_folder;
		// If the string is empty, the current directory is assumed. This exists by default, so no need to create it.
		if (this->data_folder != "") {
			// This doesn't error if the folder exists, so create it no matter what.
			bool result = std::filesystem::create_directory(std::filesystem::path(this->data_folder));
		}
	}

	bool DataWriter::writeData(const ignition::msgs::Image & image, const ignition::msgs::Pose & pose, ignition::msgs::CameraInfo & camera_info) {
		// Write each data individually and increment the index.
		bool result = true;
		result &= writeImage(image);
		result &= writePose(pose);
		result &= writeCameraInfo(camera_info);
		this->index++;
		return result;
	}

	std::string DataWriter::getBaseFilename() const {
		char buffer[20];
		snprintf(buffer, 20, "%06d", index);
		std::string file_name(buffer);
		return data_folder + "/" + file_name;
	}

	bool DataWriter::writeCameraInfo(const ignition::msgs::CameraInfo & camera_info) {
		std::ofstream calibration_file;
		calibration_file.open(getBaseFilename() + "_calib.txt");
		calibration_file << camera_info.DebugString() << std::endl;
		calibration_file.close();
		return calibration_file.good();
	}

	bool DataWriter::writeImage(const ignition::msgs::Image & image) {
		// Use Ignition's built in class that has this ability. The types need converted though.
		ignition::common::Image image_out;
		ignition::common::Image::PixelFormatType pixel_format;
		// I believe the simulation only provides a single pixel type. Leave the structure here for future expansions
		// though.
		switch (image.pixel_format_type()) {
			case ignition::msgs::RGB_INT8:
				pixel_format = ignition::common::Image::RGB_INT8;
				break;
			default:
				std::cerr << "Unknown pixel type: " << image.pixel_format_type() << std::endl;
				return false;
		}
		// The image data also needs loaded as an array of unsigned chars, so convert.
		std::vector<unsigned char> data(image.data().begin(), image.data().end());
		image_out.SetFromData(&data[0], image.width(), image.height(), pixel_format);
		// Write the image.
		image_out.SavePNG(getBaseFilename() + ".png");
		return true;
	}

	bool DataWriter::writePose(const ignition::msgs::Pose & pose) {
		// Get each value for convenience.
		double x = pose.position().x();
		double y = pose.position().y();
		double z = pose.position().z();
		// Get the RPY too.
		double roll, pitch, yaw;
		std::tie(roll, pitch, yaw) = RPYFromQuaternionMsg(pose.orientation());
		std::ofstream pose_file;
		pose_file.open(getBaseFilename() + ".txt");
		pose_file << x << "," << y << "," << z << "," << roll << "," << pitch << "," << yaw << std::endl;
		pose_file.close();
		return pose_file.good();
	}
} // namespace ground_texture_sim
