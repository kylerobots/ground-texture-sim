#include "TrajectoryFollower.h"

namespace ground_texture_sim {
	TrajectoryFollower::TrajectoryFollower() {
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
} // namespace ground_texture_sim
