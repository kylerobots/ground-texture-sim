#include "math.h"

#include "gtest/gtest.h"

TEST(QuatMath, QuatFromYaw) {
	auto result = ground_texture_sim::quaternionFromYaw(0.0);
	EXPECT_DOUBLE_EQ(result.W(), 1.0);
	EXPECT_DOUBLE_EQ(result.X(), 0.0);
	EXPECT_DOUBLE_EQ(result.Y(), 0.0);
	EXPECT_DOUBLE_EQ(result.Z(), 0.0);
}