#ifndef _TRAJECTORY_FOLLOWER_H_
#define _TRAJECTORY_FOLLOWER_H_

#include "DataWriter.h"

#include <ignition/math/Quaternion.hh>
#include <ignition/msgs/boolean.pb.h>
#include <ignition/msgs/pose.pb.h>
#include <ignition/transport.hh>
#include <stdexcept>
#include <vector>

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
		 * @brief A simple representation of different poses along the trajectory.
		 * 
		 */
		struct Pose2D {
			/// The location along the X-axis, in meters.
			float x;
			/// The location along the Y-axis, in meters.
			float y;
			/// The rotation about the Z-axis, in radians.
			float yaw;
		};

		public:
		/**
		 * @brief Construct a new Trajectory Follower object
		 * 
		 */
		TrajectoryFollower();

		/**
		 * @brief Record data along each pose of the given series of poses.
		 * 
		 * This will iterate through each pose, put the camera at that pose, and capture the data.
		 * 
		 * @param trajectory A vector of each 2D pose the camera should take.
		 * @return true If the capture was completely successful.
		 * @return false If the system was unable to capture each pose.
		 */
		bool captureTrajectory(const std::vector<Pose2D> & trajectory);

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

		protected:
		/**
		 * @brief Capture a single pose from a trajectory.
		 * 
		 * This performs the camera manipulation and data collecting for a single pose.
		 * 
		 * @param pose The pose at which to place the camera.
		 * @return true If the capture was successful.
		 * @return false If the capture was unsuccessful.
		 */
		bool capturePose(const Pose2D & pose);

		/**
		 * @brief Send the new pose to the simulation.
		 * 
		 * It transforms it into a Pose message first.
		 * 
		 * @param pose The pose to send.
		 * @return true If the simulation accepted the new pose.
		 * @return false If there is some sort of error.
		 */
		bool sendPose(const Pose2D & pose);

		protected:
		/// The height at which to keep the camera.
		float camera_height;
		/// The object to output all data in the correct format.
		DataWriter data_writer;
		/// The transport node for interacting with the simulation.
		ignition::transport::Node node;
	};
} // namespace ground_texture_sim

#endif // _TRAJECTORY_FOLLOWER_H_