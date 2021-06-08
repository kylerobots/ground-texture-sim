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
