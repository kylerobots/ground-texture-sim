#include "DataWriter.h"

#include "gtest/gtest.h"
#include <filesystem>
#include <fstream>

/**
 * @brief Helper function to write simple messages to file.
 * 
 * This uses the provided write and writes empty messages to file.
 * 
 * @param writer The writer to use for writing.
 * @return true if the write was successful.
 * @return false otherwise.
 */
bool writeData(ground_texture_sim::DataWriter & writer) {
	ignition::msgs::Image image;
	image.set_pixel_format_type(ignition::msgs::PixelFormatType::RGB_INT8);
	ignition::msgs::Pose pose;
	pose.mutable_position()->set_x(1.1);
	pose.mutable_position()->set_y(2.2);
	pose.mutable_position()->set_z(3.3);
	ignition::msgs::CameraInfo camera_info;
	bool result = writer.writeData(image, pose, camera_info);
	return result;
}

/// @test Make sure the system can work when given no specific path.
TEST(DataWriter, Empty) {
	ground_texture_sim::DataWriter writer;
	EXPECT_TRUE(writeData(writer));
	// Verify the file exists.
	EXPECT_TRUE(std::filesystem::exists("000000.txt"));
	EXPECT_TRUE(std::filesystem::exists("000000.png"));
	EXPECT_TRUE(std::filesystem::exists("000000_calib.txt"));
	// Delete everything
	std::filesystem::remove("000000.txt");
	std::filesystem::remove("000000.png");
	std::filesystem::remove("000000_calib.txt");
}

/// @test Test that the system writes correctly when given relative path that exists.
TEST(DataWriter, RelativeExists) {
	// Create the directory first.
	std::string subfolder = "relative_exists";
	std::filesystem::create_directory(subfolder);
	ground_texture_sim::DataWriter writer(subfolder);
	EXPECT_TRUE(writeData(writer));
	// Verify the file exists.
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000000.txt"));
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000000.png"));
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000000_calib.txt"));
	// Delete everything
	std::filesystem::remove_all(subfolder);
}

/// @test Test that the system writes correctly when given a relative path that doesn't exist for multiple levels.
TEST(DataWriter, RelativeNew) {
	std::string subfolder = "relative_new/output";
	ground_texture_sim::DataWriter writer;
	writer.setDataFolder(subfolder);
	EXPECT_TRUE(writeData(writer));
	// Verify the file exists.
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000000.txt"));
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000000.png"));
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000000_calib.txt"));
	// Delete everything
	std::filesystem::remove_all(subfolder);
}

/// @test Test that the system writes correctly when given an absolute path.
TEST(DataWriter, Absolute) {
	std::string current = std::filesystem::current_path();
	std::string subfolder = current + "/absolute/output";
	ground_texture_sim::DataWriter writer;
	writer.setDataFolder(subfolder);
	EXPECT_TRUE(writeData(writer));
	// Verify the file exists.
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000000.txt"));
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000000.png"));
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000000_calib.txt"));
	// Delete everything
	std::filesystem::remove_all(subfolder);
}

/// @test Test that the system indexes correctly when writing multiple times.
TEST(DataWriter, Index) {
	std::string subfolder = "multiple";
	ground_texture_sim::DataWriter writer;
	writer.setDataFolder(subfolder);
	EXPECT_TRUE(writeData(writer));
	EXPECT_TRUE(writeData(writer));
	// Verify the file exists.
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000000.txt"));
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000000.png"));
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000000_calib.txt"));
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000001.txt"));
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000001.png"));
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000001_calib.txt"));
	// Delete everything
	std::filesystem::remove_all(subfolder);
}

/// @test Test that the pose data is written correctly.
TEST(DataWriter, PoseFormat) {
	std::string subfolder = "format";
	ground_texture_sim::DataWriter writer(subfolder);
	EXPECT_TRUE(writeData(writer));
	EXPECT_TRUE(std::filesystem::exists(subfolder + "/000000.txt"));
	// Read in the file.
	std::ifstream file;
	file.open(subfolder + "/000000.txt");
	EXPECT_TRUE(file.is_open());
	std::string line;
	std::getline(file, line);
	// For some reason, the RPY likes pitch to be negative zero.
	EXPECT_STRCASEEQ(line.c_str(), "1.1,2.2,3.3,0,-0,0");
	// There shouldn't be anything else in the file.
	std::getline(file, line);
	EXPECT_STRCASEEQ(line.c_str(), "");
	EXPECT_TRUE(file.eof());
	file.close();
	std::filesystem::remove_all(subfolder);
}

/// @test Test the writer can return relative or absolute paths.
TEST(DataWriter, getDataFolder) {
	std::filesystem::path current_path = std::filesystem::current_path();
	std::filesystem::path relative_path1 = "../output";
	ground_texture_sim::DataWriter writer;
	writer.setDataFolder(current_path / relative_path1);
	auto result = writer.getDataFolder();
	EXPECT_STRCASEEQ(result.c_str(), (current_path / relative_path1).c_str());
	result = writer.getDataFolder(true);
	EXPECT_STRCASEEQ(result.c_str(), relative_path1.c_str());
}