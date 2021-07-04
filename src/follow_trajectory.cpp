#include "TrajectoryFollower.h"

#include <boost/tokenizer.hpp>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

std::vector<ground_texture_sim::TrajectoryFollower::Pose2D> parseFile(const std::string & filename) {
	std::vector<ground_texture_sim::TrajectoryFollower::Pose2D> trajectory;
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
				return std::vector<ground_texture_sim::TrajectoryFollower::Pose2D>();
			} else if (tokens.size() > 3) {
				std::cout << "WARNING: Line contains extra values. They will be ignored: " << line << std::endl;
			}

			ground_texture_sim::TrajectoryFollower::Pose2D pose;
			try {
				pose.x = stof(tokens[0]);
				pose.y = stof(tokens[1]);
				pose.yaw = stof(tokens[2]);

			} catch (const std::invalid_argument & e) {
				std::cout << "ERROR: Unable to parse line: " << line << std::endl;
				return std::vector<ground_texture_sim::TrajectoryFollower::Pose2D>();
			} catch (const std::out_of_range & e) {
				std::cout << "ERROR: Number in line is not convertible: " << line << std::endl;
				return std::vector<ground_texture_sim::TrajectoryFollower::Pose2D>();
			}
			trajectory.push_back(pose);
		}
	}
	return trajectory;
}

int main(int argc, char ** argv) {
	ground_texture_sim::TrajectoryFollower follower;
	follower.setCameraHeight(0.25);
	auto trajectory = parseFile("/workspaces/ground-texture-sim/data/trajectory.txt");
	follower.captureTrajectory(trajectory);
	return 0;
}
