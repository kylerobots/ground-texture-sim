#include "KeyboardController.h"

namespace ground_texture_sim {
	KeyboardController::KeyboardController() {
		// Set all times to Epoch so they don't accidentally cause it to start driving at boot.
		back_press_time = std::chrono::milliseconds::zero();
		clockwise_press_time = std::chrono::milliseconds::zero();
		counterclockwise_press_time = std::chrono::milliseconds::zero();
		forward_press_time = std::chrono::milliseconds::zero();
		left_press_time = std::chrono::milliseconds::zero();
		right_press_time = std::chrono::milliseconds::zero();
	}

	ignition::msgs::Twist KeyboardController::createMessage() const {
		// Record the time to compare how long ago keys were pressed.
		auto current_time = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch());
		double current_x = 0.0;
		double current_y = 0.0;
		double current_t = 0.0;
		ignition::msgs::Twist msg;
		auto threshold = std::chrono::milliseconds(100);
		double linear_speed = 0.5;
		double angular_speed = 0.25;
		// Look at each key and see if it was pressed less than 0.1 seconds. If it has, add it's velocity contribution
		// to the right part of the message.
		if ((current_time - left_press_time.load()) <= threshold) {
			current_y += linear_speed;
		}
		if ((current_time - right_press_time.load()) <= threshold) {
			current_y -= linear_speed;
		}
		if ((current_time - forward_press_time.load()) <= threshold) {
			current_x += linear_speed;
		}
		if ((current_time - back_press_time.load()) <= threshold) {
			current_x -= linear_speed;
		}
		if ((current_time - clockwise_press_time.load()) <= threshold) {
			current_t += linear_speed;
		}
		if ((current_time - counterclockwise_press_time.load()) <= threshold) {
			current_t -= linear_speed;
		}
		// The camera is rotated down 90 degrees, so positive x drives straight into the ground. Adjust the actual
		// message values.
		msg.mutable_linear()->set_z(current_x);
		msg.mutable_linear()->set_y(current_y);
		msg.mutable_angular()->set_x(current_t);
		return msg;
	}

	void KeyboardController::registerKeypress(const ignition::msgs::Int32 & msg) {
		// Check which key is pressed. Right now, only ASWD and QE are used. The incoming data is the decimal
		// representation of the ascii character, so convert to that.
		char command = static_cast<char>(msg.data());
		// Determine the time of the keypress.
		auto current_time = std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch());
		switch (command) {
			case 'A':
				left_press_time.store(current_time);
				break;
			case 'S':
				back_press_time.store(current_time);
				break;
			case 'W':
				forward_press_time.store(current_time);
				break;
			case 'D':
				right_press_time.store(current_time);
				break;
			case 'Q':
				counterclockwise_press_time.store(current_time);
				break;
			case 'E':
				clockwise_press_time.store(current_time);
				break;
			default:
				// Right now, we don't care about any other character.
				break;
		}
	}
} // namespace ground_texture_sim
