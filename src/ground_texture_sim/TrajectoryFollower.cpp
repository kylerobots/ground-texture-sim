#include "TrajectoryFollower.h"

namespace ground_texture_sim {
	TrajectoryFollower::TrajectoryFollower(const Parameters & parameters) {
		// Set the camera height. This already throws the right error, so let it pass up.
		setCameraHeight(parameters.camera_height);

		// Set the output path.
		try {
			data_writer.setDataFolder(parameters.output_folder);

		} catch (const std::filesystem::filesystem_error & e) {
			throw std::invalid_argument(e.what());
		}

		// Register the topics to capture.
		if (!data_synchronizer.registerTopic<ignition::msgs::Image>(parameters.image_topic)) {
			throw std::invalid_argument("Unable to subscribe to " + parameters.image_topic);
		}
		if (!data_synchronizer.registerTopic<ignition::msgs::CameraInfo>(parameters.camera_info_topic)) {
			throw std::invalid_argument("Unable to subscribe to " + parameters.camera_info_topic);
		}
		if (!data_synchronizer.registerTopic<ignition::msgs::Pose_V>(parameters.pose_topic)) {
			throw std::invalid_argument("Unable to subscribe to " + parameters.pose_topic);
		}

		// Store the values needed later.
		camera_info_topic = parameters.camera_info_topic;
		camera_model_name = parameters.camera_model_name;
		image_topic = parameters.image_topic;
		model_move_service = parameters.model_move_service;
		poses_topic = parameters.pose_topic;
	}

	bool TrajectoryFollower::captureTrajectory(const std::vector<Pose2D> & trajectory) {
		for (auto && pose : trajectory) {
			std::cout << "Capturing: (" << pose.x << ", " << pose.y << ", " << pose.yaw << ")" << std::endl;
			// First, create a normalized angle version of the pose, as Gazebo causes issues if outside of [-Pi, Pi]
			Pose2D wrapped_pose = pose;
			wrapped_pose.yaw = ground_texture_sim::wrapAngle(pose.yaw);
			bool success = capturePose(wrapped_pose);
			if (!success) {
				std::cout << "ERROR: Failed to move to pose!" << std::endl;
				return false;
			}
			ignition::msgs::CameraInfo * camera_info_msg;
			ignition::msgs::Image * image_msg;
			ignition::msgs::Pose_V * pose_msg;
			ignition::msgs::Pose extracted_pose;
			// Now get the most up to date messages. There might be a bit of a lag in updating the values, so check
			// the pose to see if it matches approximately what we would expect.
			bool pose_updated = false;
			while (!pose_updated) {
				auto messages = data_synchronizer.getMessages();
				// Cast each message back into the expected format.
				camera_info_msg = dynamic_cast<ignition::msgs::CameraInfo *>(messages[camera_info_topic].get());
				image_msg = dynamic_cast<ignition::msgs::Image *>(messages[image_topic].get());
				pose_msg = dynamic_cast<ignition::msgs::Pose_V *>(messages[poses_topic].get());
				// Compare values to verify updated pose. Account for floating point accuracy.
				for (int i = 0; i < pose_msg->pose_size(); ++i) {
					if (pose_msg->pose(i).name() == camera_model_name) {
						extracted_pose = pose_msg->pose(i);
					}
				}
				// We want all pose values to be updated, so flip to false if any aren't within eps.
				pose_updated = true;
				double eps = 1e-6;
				pose_updated &= abs(extracted_pose.position().x() - wrapped_pose.x) <= eps;
				pose_updated &= abs(extracted_pose.position().y() - wrapped_pose.y) <= eps;
				// We have to pull out the quaternion values.
				ignition::math::Quaternion quaternion(extracted_pose.orientation().w(), extracted_pose.orientation().x(), extracted_pose.orientation().y(), extracted_pose.orientation().z());
				pose_updated &= abs(quaternion.Yaw() - wrapped_pose.yaw) <= eps;
			}

			// Write them to file.
			data_writer.writeData(*image_msg, extracted_pose, *camera_info_msg);
		}
		std::cout << "Finished capturing!" << std::endl;
		return true;
	}

	float TrajectoryFollower::getCameraHeight() const {
		return camera_height;
	}

	void TrajectoryFollower::setCameraHeight(float camera_height) {
		if (camera_height >= 0.0) {
			this->camera_height = camera_height;
		} else {
			throw std::invalid_argument("Camera height must be non-negative!");
		}
	}

	bool TrajectoryFollower::capturePose(const Pose2D & pose) {
		// This needs to first move the camera, wait for the camera to be at the position. wait for an updated image,
		// maybe wait for an updated pose?, wait for an updated camera info, then send all of them to the data writer.
		bool result = sendPose(pose);
		return result;
	}

	bool TrajectoryFollower::sendPose(const Pose2D & pose) {
		// First construct the message.
		ignition::msgs::Pose pose_request = poseMsgFromPose2D(pose);
		pose_request.set_name(camera_model_name);
		// Add the camera height.
		pose_request.mutable_position()->set_z(getCameraHeight());
		ignition::msgs::Boolean response;
		bool result;
		unsigned int timeout = 1000;
		bool executed = node.Request(model_move_service, pose_request, timeout, response, result);
		// We get three ways to check if it worked!
		return executed && result && response.data();
	}
} // namespace ground_texture_sim
