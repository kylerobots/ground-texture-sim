#ifndef _TRAJECTORY_FOLLOWER_H_
#define _TRAJECTORY_FOLLOWER_H_

#include <stdexcept>

/**
 * @brief The namespace for any class created in this package.
 * 
 * This is mainly implemented to prevent possible collisions with similarly named entities.
 * 
 */
namespace ground_texture_sim {
	/**
	 * @brief A class to walk the camera through a predefined trajectory.
	 * 
	 * This class uses a predefined list of camera poses to move the camera about the simulation environment. It reads
	 * in each pose, moves the camera to that spot, captures the image, and writes the data to file. This continues for
	 * every pose. Poses are simply given as a CSV file of 2D poses:
	 * ```
	 * x1(meters),y1(meters),yaw1(radians)
	 * x2(meters),y2(meters),yaw2(radians)
	 * ...
	 * ```
	 * No interpolation is done between the poses, so ensure they have sufficient overlap. Data is written to the
	 * specified directory in the same format as DataWriter.
	 * 
	 * Because this has to wait for the camera to move and refresh its data, this may take some time to process on slow
	 * systems.
	 * 
	 */
	class TrajectoryFollower {
		public:
		/**
		 * @brief Construct a new Trajectory Follower object
		 * 
		 */
		TrajectoryFollower();

		/**
		 * @brief Get the height of the camera.
		 * 
		 * @return float The height of the camera above the ground, in meters.
		 */
		float getCameraHeight() const;

		/**
		 * @brief Set the height of the camera.
		 * 
		 * @param camera_height The new height of the camera above the ground, in meters. This should be non-negative.
		 * @throws std::invalid_argument Thrown if the height is negative, as that is not physically possible.`
		 */
		void setCameraHeight(float camera_height);

		private:
		/// The height at which to keep the camera.
		float camera_height;
	};
} // namespace ground_texture_sim

#endif // _TRAJECTORY_FOLLOWER_H_