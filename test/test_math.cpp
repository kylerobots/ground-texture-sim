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