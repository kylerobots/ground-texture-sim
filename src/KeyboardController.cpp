#include "KeyboardController.h"

namespace ground_texture_sim {
	KeyboardController::KeyboardController() {
	}

	void KeyboardController::registerKeypress(const ignition::msgs::Int32 & msg) {
		std::cout << "I heard: " << msg.data() << std::endl;
	}
} // namespace ground_texture_sim
