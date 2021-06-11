#include "KeyboardController.h"

#include "gtest/gtest.h"

/**
 * @brief The fixture to assist with testing KeyboardController.
 * 
 * There isn't any particular setup needed, so this just creates the class.
 */
class KeyboardControllerTest : public ::testing::Test {
	protected:
	/// The controller to use for testing.
	ground_texture_sim::KeyboardController controller;

	/**
	 * @brief A convenience function to check expected velocities.
	 * 
	 * This function calls EXPECT_DOUBLE_EQ on each of the 6 velocity components vs the expected values.
	 * 
	 * @param msg The Twist message to check.
	 * @param x The expected linear velocity along the X axis.
	 * @param y The expected linear velocity along the Y axis.
	 * @param z The expected linear velocity along the Z axis.
	 * @param r The expected angular velocity about the X axis.
	 * @param p The expected angular velocity about the Y axis.
	 * @param t The expected angular velocity about the Z axis.
	 */
	void checkVelocity(const ignition::msgs::Twist & msg, double x, double y, double z, double r, double p, double t) {
		EXPECT_DOUBLE_EQ(msg.linear().x(), x);
		EXPECT_DOUBLE_EQ(msg.linear().y(), y);
		EXPECT_DOUBLE_EQ(msg.linear().z(), z);
		EXPECT_DOUBLE_EQ(msg.angular().x(), r);
		EXPECT_DOUBLE_EQ(msg.angular().y(), p);
		EXPECT_DOUBLE_EQ(msg.angular().z(), t);
	}

	/**
	 * @brief Registers a named letter with the test object.
	 * 
	 * Since the controller accepts ignition messages, this helper method converts the data types from the equivalent
	 * char into the right message. It then logs it with the controller.
	 * 
	 * @param letter The equivalent letter of the key to press.
	 */
	void registerLetter(char letter) {
		ignition::msgs::Int32 msg;
		msg.set_data(static_cast<int>(letter));
		controller.registerKeypress(msg);
	}
};

/**
 * @brief Test that the velocity is always zero if no keys are registered.
 * 
 */
TEST_F(KeyboardControllerTest, ZeroVelocity) {
	auto msg = controller.createMessage();
	checkVelocity(msg, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0);
}

/**
 * @brief Test that the 'A' key provides a positive linear Y axis motion.
 * 
 */
TEST_F(KeyboardControllerTest, Left) {
	registerLetter('A');
	auto msg = controller.createMessage();
	checkVelocity(msg, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0);
}

/**
 * @brief Test that the 'D' key provides a negative linear Y axis motion.
 * 
 */
TEST_F(KeyboardControllerTest, Right) {
	registerLetter('D');
	auto msg = controller.createMessage();
	checkVelocity(msg, 0.0, -0.5, 0.0, 0.0, 0.0, 0.0);
}

/**
 * @brief Test that the 'W' key provides a positive linear Z axis motion.
 * 
 */
TEST_F(KeyboardControllerTest, Forward) {
	registerLetter('W');
	auto msg = controller.createMessage();
	checkVelocity(msg, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0);
}

/**
 * @brief Test that the 'S' key provides a negative linear Z axis motion.
 * 
 */
TEST_F(KeyboardControllerTest, Back) {
	registerLetter('S');
	auto msg = controller.createMessage();
	checkVelocity(msg, 0.0, 0.0, -0.5, 0.0, 0.0, 0.0);
}

/**
 * @brief Test that the 'E' key provides a positive rotation about the X axis.
 * 
 */
TEST_F(KeyboardControllerTest, CW) {
	registerLetter('E');
	auto msg = controller.createMessage();
	checkVelocity(msg, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0);
}

/**
 * @brief Test that the 'Q' key provides a negative rotation about the X axis.
 * 
 */
TEST_F(KeyboardControllerTest, CCW) {
	registerLetter('Q');
	auto msg = controller.createMessage();
	checkVelocity(msg, 0.0, 0.0, 0.0, -0.25, 0.0, 0.0);
}