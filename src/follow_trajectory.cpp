#include "TrajectoryFollower.h"

#include <CLI/CLI.hpp>
#include <boost/tokenizer.hpp>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

/**
 * @brief Parse a CSV file containing poses.
 * 
 * This reads in a CSV file and converts it to a series of poses ready to use in TrajectoryFollower. Each line of the
 * file should represent one pose in the trajectory. The form should be:
 * ```
 * x1, y1, yaw1
 * x2, y2, yaw2
 * ...
 * ```
 * 
 * @param filename The file to read in for poses.
 * @return std::vector<ground_texture_sim::Pose2D> A resulting collection of poses. If an error occurs, this vector is
 * empty.
 */
std::vector<ground_texture_sim::Pose2D> parseFile(const std::string & filename) {
	std::vector<ground_texture_sim::Pose2D> trajectory;
	std::string line;
	std::ifstream file(filename);
	if (!file.is_open()) {
		std::cout << "ERROR: Unable to read " << filename << std::endl;
	} else {
		while (getline(file, line)) {
			// Parse each line into the component values.
			boost::tokenizer<boost::escaped_list_separator<char>> tokenizer(line);
			std::vector<std::string> tokens;
			tokens.assign(tokenizer.begin(), tokenizer.end());
			if (tokens.size() < 3) {
				std::cout << "ERROR: Line does not have enough values: " << line << std::endl;
				return std::vector<ground_texture_sim::Pose2D>();
			} else if (tokens.size() > 3) {
				std::cout << "WARNING: Line contains extra values. They will be ignored: " << line << std::endl;
			}

			ground_texture_sim::Pose2D pose;
			try {
				pose.x = stof(tokens[0]);
				pose.y = stof(tokens[1]);
				pose.yaw = stof(tokens[2]);

			} catch (const std::invalid_argument & e) {
				std::cout << "ERROR: Unable to parse line: " << line << std::endl;
				return std::vector<ground_texture_sim::Pose2D>();
			} catch (const std::out_of_range & e) {
				std::cout << "ERROR: Number in line is not convertible: " << line << std::endl;
				return std::vector<ground_texture_sim::Pose2D>();
			}
			trajectory.push_back(pose);
		}
	}
	return trajectory;
}

int main(int argc, char ** argv) {
	CLI::App option_parser("Ground Texture Simulator", "follow_trajectory");
	// Set customization parameters.
	option_parser.set_config("--config", "", "Set configurations via a TOML file");
	option_parser.allow_config_extras(true);
	ground_texture_sim::TrajectoryFollower::Parameters parameters;
	std::string trajectory_file;
	option_parser.add_option("trajectory_file", trajectory_file, "The CSV of trajectories")->required()->check(CLI::ExistingFile);
	option_parser.add_option("--camera_topic", parameters.camera_info_topic, "The topic publishing camera parameters", true);
	option_parser.add_option("--height", parameters.camera_height, "The height of the camera", true);
	option_parser.add_option("--image_topic", parameters.image_topic, "The topic publishing images", true);
	option_parser.add_option("--move_service", parameters.model_move_service, "The service to move the camera", true);
	option_parser.add_option("--pose_topic", parameters.pose_topic, "The topic publishing poses", true);
	option_parser.add_option("-m,--model", parameters.camera_model_name, "The model name of the camera in simulation", true);
	option_parser.add_option("-o,--output", parameters.output_folder, "Where the data should be written", true);
	CLI11_PARSE(option_parser, argc, argv);
	auto trajectory = parseFile(trajectory_file);
	// Set up the follower and go.
	bool success = false;
	try {
		ground_texture_sim::TrajectoryFollower follower(parameters);
		success = follower.captureTrajectory(trajectory);
	} catch (const std::exception & e) {
		std::cerr << e.what() << '\n';
	}
	if (success) {
		return 0;
	} else {
		std::cerr << "Unable to capture full trajectory. Results may be incomplete or corrupted." << std::endl;
		return -1;
	}
}
