#ifndef _KEYBOARD_CONTROLLER_H_
#define _KEYBOARD_CONTROLLER_H_

#include <atomic>
#include <chrono>
#include <ignition/msgs/int32.pb.h>
#include <ignition/msgs/twist.pb.h>

/**
 * @brief The namespace for any class created in this package.
 * 
 * This is mainly implemented to prevent possible collisions with similarly named entities.
 * 
 */
namespace ground_texture_sim {
	/**
	 * @brief Creates velocity commands based on registered key presses.
	 * 
	 * This class stores the last time of various keypresses. When requested, it assembles a velocity command that
	 * includes the appropriate velocity indicated by each component. Right now, they are as follows: 
	 * 
	 * | Key | X (m/s) | Y (m/s) | Theta (rad/s) |
	 * | --- | ------- | ------- | ------------- |
	 * | A   | 0.0     | -0.5    | 0.0           |
	 * | S   | -0.5    | 0.0     | 0.0           |
	 * | W   | 0.5     | 0.0     | 0.0           |
	 * | D   | 0.0     | 0.5     | 0.0           |
	 * | Q   | 0.0     | 0.0     | 0.25          |
	 * | E   | 0.0     | 0.0     | -0.25         |
	 * 
	 * Velocities from each button are added, meaning pressing two opposite buttons will net zero velocity. Only keys
	 * that have been pressed in the last 0.1 seconds are counted. Otherwise, a zero velocity is created.
	 */
	class KeyboardController {
		private:
		/// The time a reverse key was last pressed, stored as milliseconds since Epoch.
		std::atomic<std::chrono::milliseconds> back_press_time;
		/// The time a rotate clockwise key was last pressed, stored as milliseconds since Epoch.
		std::atomic<std::chrono::milliseconds> clockwise_press_time;
		/// The time a rotate counterclockwise key was last pressed, stored as milliseconds since Epoch.
		std::atomic<std::chrono::milliseconds> counterclockwise_press_time;
		/// The time a forward key was last pressed, stored as milliseconds since Epoch.
		std::atomic<std::chrono::milliseconds> forward_press_time;
		/// The time a left strafe key was last pressed, stored as milliseconds since Epoch.
		std::atomic<std::chrono::milliseconds> left_press_time;
		/// The time a right strafe key was last pressed, stored as milliseconds since Epoch.
		std::atomic<std::chrono::milliseconds> right_press_time;

		public:
		/**
		 * @brief The no-arg constructor.
		 */
		KeyboardController(/* args */);

		/**
		 * @brief Create a Twist message.
		 * 
		 * The resulting velocity will use any key press logged via registerKeypress in the last 0.1 seconds, even if
		 * opposite keys are pressed.
		 * 
		 * @return ignition::msgs::Twist The resulting message.
		 */
		ignition::msgs::Twist createMessage() const;

		/**
		 * @brief Record the time a given key is pressed.
		 * 
		 * This method will extract the key sent by the message. If it maps to a velocity command, it will record the
		 * time of arrival and appropriate key for use when creating velocity commands.
		 * 
		 * @param msg The keypress message received from Ignition's topic.
		 */
		void registerKeypress(const ignition::msgs::Int32 & msg);
	};

} // namespace ground_texture_sim

#endif // _KEYBOARD_CONTROLLER_H_