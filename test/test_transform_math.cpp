#include "transform_math.h"

#include "gtest/gtest.h"
#include <cmath>

/**
 * @brief Helper function to compare test results.
 * 
 * This compares Quaternion objects to their expected (x, y, z, w) values. Since we are dealing with yaw only, the x and
 * y value should always be zero. Since a negative of a quaterion represents the same rotation, both possibilities must
 * be tested for.
 * 
 * @param quat The Quaternion to compare.
 * @param z The expected z value.
 * @param w The expected w value.
 */
void compareQuaternions(const ignition::math::Quaternion<double> & quat, double z, double w) {
	ASSERT_DOUBLE_EQ(quat.X(), 0.0);
	ASSERT_DOUBLE_EQ(quat.Y(), 0.0);
	// Compare to the original and negative values. Slight computation differences are larger than double precision, so
	// use a higher tolerance to compare.
	bool original_z = abs(quat.Z() - z) <= 1e-10;
	bool original_w = abs(quat.W() - w) <= 1e-10;
	bool original = original_z && original_w;
	bool negative_z = abs(quat.Z() + z) <= 1e-10;
	bool negative_w = abs(quat.W() + w) <= 1e-10;
	bool negative = negative_z && negative_w;
	// One of the two must match, otherwise, they represent different rotations.
	ASSERT_TRUE(original || negative);
}

/**
 * @brief Helper function to compare test results.
 * 
 * This compares Quaternion message objects to their expected (x, y, z, w) values. Since we are dealing with yaw only,
 * the x and y value should always be zero. Since a negative of a quaterion represents the same rotation, both
 * possibilities must be tested for.
 * 
 * @param quat The Quaternion to compare.
 * @param z The expected z value.
 * @param w The expected w value.
 */
void compareQuaternions(const ignition::msgs::Quaternion & quat, double z, double w) {
	ASSERT_DOUBLE_EQ(quat.x(), 0.0);
	ASSERT_DOUBLE_EQ(quat.y(), 0.0);
	// Compare to the original and negative values. Slight computation differences are larger than double precision, so
	// use a higher tolerance to compare.
	bool original_z = abs(quat.z() - z) <= 1e-10;
	bool original_w = abs(quat.w() - w) <= 1e-10;
	bool original = original_z && original_w;
	bool negative_z = abs(quat.z() + z) <= 1e-10;
	bool negative_w = abs(quat.w() + w) <= 1e-10;
	bool negative = negative_z && negative_w;
	// One of the two must match, otherwise, they represent different rotations.
	ASSERT_TRUE(original || negative);
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
	compareQuaternions(pose_msg.orientation(), std::sin(pose2d.yaw / 2.0), std::cos(pose2d.yaw / 2.0));
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
	double yaw = M_PI / 4.0;
	auto result = ground_texture_sim::quaternionFromYaw(yaw);
	compareQuaternions(result, std::sin(yaw / 2.0), std::cos(yaw / 2.0));
	result = ground_texture_sim::quaternionFromYaw(-1.0 * yaw);
	compareQuaternions(result, std::sin(-1.0 * yaw / 2.0), std::cos(-1.0 * yaw / 2.0));
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
	double yaw = M_PI / 4.0;
	auto result = ground_texture_sim::quaternionMsgFromYaw(yaw);
	compareQuaternions(result, std::sin(yaw / 2.0), std::cos(yaw / 2.0));
	result = ground_texture_sim::quaternionMsgFromYaw(-1.0 * yaw);
	compareQuaternions(result, std::sin(-1.0 * yaw / 2.0), std::cos(-1.0 * yaw / 2.0));
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

/// @test Test that the RPY is zero for an identity quaternion.
TEST(RPYFromQuaternion, Identity) {
	double input_yaw = 0.0;
	auto quaternion = ground_texture_sim::quaternionFromYaw(input_yaw);
	double roll, pitch, yaw;
	std::tie(roll, pitch, yaw) = ground_texture_sim::RPYFromQuaternion(quaternion);
	ASSERT_DOUBLE_EQ(roll, 0.0);
	ASSERT_DOUBLE_EQ(pitch, 0.0);
	ASSERT_DOUBLE_EQ(yaw, input_yaw);
}

/// @test Test that the RPY is correct for a positive yaw.
TEST(RPYFromQuaternion, PositiveYaw) {
	double input_yaw = M_PI / 2.0;
	auto quaternion = ground_texture_sim::quaternionFromYaw(input_yaw);
	double roll, pitch, yaw;
	std::tie(roll, pitch, yaw) = ground_texture_sim::RPYFromQuaternion(quaternion);
	ASSERT_DOUBLE_EQ(roll, 0.0);
	ASSERT_DOUBLE_EQ(pitch, 0.0);
	ASSERT_DOUBLE_EQ(yaw, input_yaw);
}

/// @test Test that the RPY is correct for a wrapped yaw
TEST(RPYFromQuaternion, WrappedYaw) {
	double input_yaw = 3.0 * M_PI;
	auto quaternion = ground_texture_sim::quaternionFromYaw(input_yaw);
	double roll, pitch, yaw;
	std::tie(roll, pitch, yaw) = ground_texture_sim::RPYFromQuaternion(quaternion);
	ASSERT_DOUBLE_EQ(roll, 0.0);
	ASSERT_DOUBLE_EQ(pitch, 0.0);
	ASSERT_DOUBLE_EQ(yaw, M_PI);
}

/// @test Test that the RPY is zero for an identity quaternion.
TEST(RPYFromQuaternionMsg, Identity) {
	double input_yaw = M_PI / 2.0;
	auto quaternion = ground_texture_sim::quaternionMsgFromYaw(input_yaw);
	double roll, pitch, yaw;
	std::tie(roll, pitch, yaw) = ground_texture_sim::RPYFromQuaternionMsg(quaternion);
	ASSERT_DOUBLE_EQ(roll, 0.0);
	ASSERT_DOUBLE_EQ(pitch, 0.0);
	ASSERT_DOUBLE_EQ(yaw, input_yaw);
}

/// @test Test that the RPY is correct for a positive yaw.
TEST(RPYFromQuaternionMsg, PositiveYaw) {
	double input_yaw = M_PI / 2.0;
	auto quaternion = ground_texture_sim::quaternionMsgFromYaw(input_yaw);
	double roll, pitch, yaw;
	std::tie(roll, pitch, yaw) = ground_texture_sim::RPYFromQuaternionMsg(quaternion);
	ASSERT_DOUBLE_EQ(roll, 0.0);
	ASSERT_DOUBLE_EQ(pitch, 0.0);
	ASSERT_DOUBLE_EQ(yaw, input_yaw);
}

/// @test Test that the RPY is correct for a wrapped yaw
TEST(RPYFromQuaternionMsg, WrappedYaw) {
	double input_yaw = 3.0 * M_PI;
	auto quaternion = ground_texture_sim::quaternionMsgFromYaw(input_yaw);
	double roll, pitch, yaw;
	std::tie(roll, pitch, yaw) = ground_texture_sim::RPYFromQuaternionMsg(quaternion);
	ASSERT_DOUBLE_EQ(roll, 0.0);
	ASSERT_DOUBLE_EQ(pitch, 0.0);
	ASSERT_DOUBLE_EQ(yaw, M_PI);
}