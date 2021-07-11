#include "TrajectoryFollower.h"

#include "gtest/gtest.h"

/// @test Verify that the camera height can be set correctly.
TEST(TrajectoryFollower, SetHeight) {
	// We don't care about parametrs, so use the defaults.
	ground_texture_sim::TrajectoryFollower::Parameters params;
	ground_texture_sim::TrajectoryFollower follower(params);
	// Non-negative heights are allowed.
	follower.setCameraHeight(0.25);
	EXPECT_EQ(follower.getCameraHeight(), 0.25);
	follower.setCameraHeight(0.0);
	EXPECT_EQ(follower.getCameraHeight(), 0.0);
	// Negative heights throw an error.
	EXPECT_THROW(follower.setCameraHeight(-1.0), std::invalid_argument);
}