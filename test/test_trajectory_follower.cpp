#include "TrajectoryFollower.h"

#include "gtest/gtest.h"

TEST(TrajectoryFollower, SetHeight) {
	ground_texture_sim::TrajectoryFollower follower;
	// Non-negative heights are allowed.
	follower.setCameraHeight(0.25);
	EXPECT_EQ(follower.getCameraHeight(), 0.25);
	follower.setCameraHeight(0.0);
	EXPECT_EQ(follower.getCameraHeight(), 0.0);
	// Negative heights throw an error.
	EXPECT_THROW(follower.setCameraHeight(-1.0), std::invalid_argument);
}