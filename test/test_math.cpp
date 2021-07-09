#include "math.h"

#include "gtest/gtest.h"
#include <cmath>

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

TEST(QuatFromYaw, Identity) {
	auto result = ground_texture_sim::quaternionFromYaw(0.0);
	compareQuaternions(result, 0.0, 1.0);
}

TEST(QuatFromYaw, Pi) {
	auto result = ground_texture_sim::quaternionFromYaw(M_PI);
	compareQuaternions(result, 1.0, 0.0);
	result = ground_texture_sim::quaternionFromYaw(-M_PI);
	compareQuaternions(result, 1.0, 0.0);
}

TEST(QuatFromYaw, PiOver4) {
	auto result = ground_texture_sim::quaternionFromYaw(M_PI / 4.0);
	compareQuaternions(result, std::sin(M_PI / 8.0), std::cos(M_PI / 8.0));
	result = ground_texture_sim::quaternionFromYaw(-M_PI / 4.0);
	compareQuaternions(result, std::sin(M_PI / 8.0), -1.0 * std::cos(M_PI / 8.0));
}