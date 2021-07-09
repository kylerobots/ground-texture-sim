#ifndef _TRAJECTORY_FOLLOWER_H_
#define _TRAJECTORY_FOLLOWER_H_

#include "DataSynchronizer.h"
#include "DataWriter.h"
#include "transform_math.h"

// #include <ignition/math/Quaternion.hh>
// #include <ignition/msgs/boolean.pb.h>
// #include <ignition/msgs/pose.pb.h>
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
	 * This is the primary class to use this library. It receives a vector of 2D poses, moves the camera to each pose,
	 * captures the data, writes it to file, then moves to the next pose in the vector.
	 * 
	 * No interpolation is done between the poses, so ensure they have sufficient overlap. Data is written to the
	 * specified directory in the format described in DataWriter.
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
		/// The object to get updates messages from each topic.
		DataSynchronizer data_synchronizer;
		/// The object to output all data in the correct format.
		DataWriter data_writer;
		/// The transport node for interacting with the simulation.
		ignition::transport::Node node;
	};
} // namespace ground_texture_sim

#endif // _TRAJECTORY_FOLLOWER_H_