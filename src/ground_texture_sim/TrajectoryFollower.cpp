#include "TrajectoryFollower.h"

namespace ground_texture_sim {
	TrajectoryFollower::TrajectoryFollower() {
	}

	bool TrajectoryFollower::captureTrajectory(const std::vector<Pose2D> & trajectory) const {
		for (auto && pose : trajectory) {
			bool success = capturePose(pose);
			if (!success) {
				return false;
			}
		}
		return true;
	}

	float TrajectoryFollower::getCameraHeight() const {
		return camera_height;
	}

	void TrajectoryFollower::setCameraHeight(float camera_height) {
		if (camera_height >= 0.0) {
			this->camera_height = camera_height;
		} else {
			throw std::invalid_argument("Camera height must be non-negative!");
		}
	}

	bool TrajectoryFollower::capturePose(const Pose2D & pose) const {
		// This needs to first move the camera, wait for the camera to be at the position. wait for an updated image,
		// maybe wait for an updated pose?, wait for an updated camera info, then send all of them to the data writer.
		return false;
	}
} // namespace ground_texture_sim
