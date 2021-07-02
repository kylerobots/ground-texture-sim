#include "TrajectoryFollower.h"

int main(int argc, char ** argv) {
	ground_texture_sim::TrajectoryFollower follower;
	follower.setCameraHeight(0.25);
	// Assemble some poses.
	ground_texture_sim::TrajectoryFollower::Pose2D pose;
	std::vector<ground_texture_sim::TrajectoryFollower::Pose2D> pose_vector;
	pose.x = 0.5;
	pose.y = 0.5;
	pose.yaw = 0.0;
	pose_vector.push_back(pose);
	pose.x = 0.5;
	pose.y = -0.5;
	pose.yaw = 0.0;
	pose_vector.push_back(pose);
	pose.x = -0.5;
	pose.y = -0.5;
	pose.yaw = 0.0;
	pose_vector.push_back(pose);
	pose.x = -0.5;
	pose.y = 0.5;
	pose.yaw = 0.0;
	pose_vector.push_back(pose);
	pose.x = 0.0;
	pose.y = 0.0;
	pose.yaw = 3.14159;
	pose_vector.push_back(pose);
	follower.captureTrajectory(pose_vector);
	return 0;
}
