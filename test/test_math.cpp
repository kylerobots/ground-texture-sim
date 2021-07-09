#include "transform_math.h"

#include "gtest/gtest.h"
#include <cmath>

/**
 * @brief Helper function to compare test results.
 * 
 * This compares Quaternion objects to their expected (x, y, z, w) values. Since we are dealing with yaw only, the x and
 * y value should always be zero. Since a negative of a quaterion represents the same rotation, the signs of both z
 * values are set equal by negating the z and w values, if required. This ensures that the tests only pass if the signs
 * of the w values also match.
 * 
 * @param quat The Quaternion to compare.
 * @param z The expected z value.
 * @param w The expected w value.
 */
void compareQuaternions(const ignition::math::Quaternion<double> & quat, double z, double w) {
	// A negative of a quaternion is the same as a quaterion. So massage to the right signs. Matching w will ensure z
	// must also be matched.
	if (std::signbit(quat.Z()) != std::signbit(z)) {
		z *= -1.0;
		w *= -1.0;
	}
	ASSERT_DOUBLE_EQ(quat.X(), 0.0);
	ASSERT_DOUBLE_EQ(quat.Y(), 0.0);
	ASSERT_NEAR(quat.Z(), z, 1e-10);
	ASSERT_NEAR(quat.W(), w, 1e-10);
}

/**
 * @brief Helper function to compare test results.
 * 
 * This compares Quaternion message objects to their expected (x, y, z, w) values. Since we are dealing with yaw only,
 * the x and y value should always be zero. Since a negative of a quaterion represents the same rotation, the signs of
 * both z values are set equal by negating the z and w values, if required. This ensures that the tests only pass if the
 * signs of the w values also match.
 * 
 * @param quat The Quaternion to compare.
 * @param z The expected z value.
 * @param w The expected w value.
 */
void compareQuaternions(const ignition::msgs::Quaternion & quat, double z, double w) {
	// A negative of a quaternion is the same as a quaterion. So massage to the right signs. Matching w will ensure z
	// must also be matched.
	if (std::signbit(quat.z()) != std::signbit(z)) {
		z *= -1.0;
		w *= -1.0;
	}
	ASSERT_DOUBLE_EQ(quat.x(), 0.0);
	ASSERT_DOUBLE_EQ(quat.y(), 0.0);
	ASSERT_NEAR(quat.z(), z, 1e-10);
	ASSERT_NEAR(quat.w(), w, 1e-10);
}

/**
 * @brief Helper function to compare a Pose2D struct to a Pose message.
 * 
 * @param pose2d The struct to compare.
 * @param pose_msg The message to compare.
 */
void comparePoses(const ground_texture_sim::Pose2D & pose2d, const ignition::msgs::Pose & pose_msg) {
	ASSERT_DOUBLE_EQ(pose_msg.position().x(), pose2d.x);
	ASSERT_DOUBLE_EQ(pose_msg.position().y(), pose2d.y);
	ASSERT_DOUBLE_EQ(pose_msg.position().z(), 0.0);
	// Leverage other helper functions to test the rotation.
	compareQuaternions(pose_msg.orientation(), std::sin(pose2d.yaw), std::cos(pose2d.yaw));
}

//// @test Test that an identity yaw is converted to an identity Quaternion.
TEST(QuatFromYaw, Identity) {
	auto result = ground_texture_sim::quaternionFromYaw(0.0);
	compareQuaternions(result, 0.0, 1.0);
}

/// @test Test that a yaw of Pi produces the correct Quaternion.
TEST(QuatFromYaw, Pi) {
	auto result = ground_texture_sim::quaternionFromYaw(M_PI);
	compareQuaternions(result, 1.0, 0.0);
	result = ground_texture_sim::quaternionFromYaw(-M_PI);
	compareQuaternions(result, 1.0, 0.0);
}

/// @test Test that a yaw of +/- Pi/4 produces the correct Quaternion.
TEST(QuatFromYaw, PiOver4) {
	auto result = ground_texture_sim::quaternionFromYaw(M_PI / 4.0);
	compareQuaternions(result, std::sin(M_PI / 8.0), std::cos(M_PI / 8.0));
	result = ground_texture_sim::quaternionFromYaw(-M_PI / 4.0);
	compareQuaternions(result, std::sin(M_PI / 8.0), -1.0 * std::cos(M_PI / 8.0));
}

/// @test Test that the code correctly wraps a value of 2*Pi to 0.
TEST(QuatFromYaw, TwoPi) {
	auto result = ground_texture_sim::quaternionFromYaw(2.0 * M_PI);
	compareQuaternions(result, 0.0, 1.0);
	result = ground_texture_sim::quaternionFromYaw(-2.0 * M_PI);
	compareQuaternions(result, 0.0, 1.0);
}

//// @test Test that an identity yaw is converted to an identity Quaternion.
TEST(QuatMsgFromYaw, Identity) {
	auto result = ground_texture_sim::quaternionMsgFromYaw(0.0);
	compareQuaternions(result, 0.0, 1.0);
}

/// @test Test that a yaw of Pi produces the correct Quaternion.
TEST(QuatMsgFromYaw, Pi) {
	auto result = ground_texture_sim::quaternionMsgFromYaw(M_PI);
	compareQuaternions(result, 1.0, 0.0);
	result = ground_texture_sim::quaternionMsgFromYaw(-M_PI);
	compareQuaternions(result, 1.0, 0.0);
}

/// @test Test that a yaw of +/- Pi/4 produces the correct Quaternion.
TEST(QuatMsgFromYaw, PiOver4) {
	auto result = ground_texture_sim::quaternionMsgFromYaw(M_PI / 4.0);
	compareQuaternions(result, std::sin(M_PI / 8.0), std::cos(M_PI / 8.0));
	result = ground_texture_sim::quaternionMsgFromYaw(-M_PI / 4.0);
	compareQuaternions(result, std::sin(M_PI / 8.0), -1.0 * std::cos(M_PI / 8.0));
}

/// @test Test that the code correctly wraps a value of 2*Pi to 0.
TEST(QuatMsgFromYaw, TwoPi) {
	auto result = ground_texture_sim::quaternionMsgFromYaw(2.0 * M_PI);
	compareQuaternions(result, 0.0, 1.0);
	result = ground_texture_sim::quaternionMsgFromYaw(-2.0 * M_PI);
	compareQuaternions(result, 0.0, 1.0);
}

/// @test Test that an identity Pose2D produces the right message.
TEST(PoseFromPose2D, Identity) {
	ground_texture_sim::Pose2D pose;
	auto result = ground_texture_sim::poseMsgFromPose2D(pose);
	comparePoses(pose, result);
}

/// @test Test that an identity Pose2D produces the right message.
TEST(PoseFromPose2D, PositiveAngle) {
	ground_texture_sim::Pose2D pose;
	pose.x = 1.0;
	pose.y = 2.5;
	pose.yaw = M_PI / 2.0;
	auto result = ground_texture_sim::poseMsgFromPose2D(pose);
	comparePoses(pose, result);
}

/// @test Test that an identity Pose2D produces the right message.
TEST(PoseFromPose2D, NegativeAngle) {
	ground_texture_sim::Pose2D pose;
	pose.x = -4.5;
	pose.y = -5.6;
	pose.yaw = -M_PI / 4.0;
	auto result = ground_texture_sim::poseMsgFromPose2D(pose);
	comparePoses(pose, result);
}

/// @test Test that an identity Pose2D produces the right message.
TEST(PoseFromPose2D, AngleWrap) {
	ground_texture_sim::Pose2D pose;
	pose.x = 0.0;
	pose.y = 100.0;
	pose.yaw = 3.0 * M_PI;
	auto result = ground_texture_sim::poseMsgFromPose2D(pose);
	comparePoses(pose, result);
}