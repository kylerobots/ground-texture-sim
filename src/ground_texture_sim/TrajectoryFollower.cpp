#include "TrajectoryFollower.h"

namespace ground_texture_sim {
	TrajectoryFollower::TrajectoryFollower() {
		// Register the topics to capture.
		data_synchronizer.registerTopic<ignition::msgs::Image>("/camera");
		data_synchronizer.registerTopic<ignition::msgs::CameraInfo>("/camera_info");
		data_synchronizer.registerTopic<ignition::msgs::Pose_V>("/world/ground_texture/dynamic_pose/info");
	}

	bool TrajectoryFollower::captureTrajectory(const std::vector<Pose2D> & trajectory) {
		for (auto && pose : trajectory) {
			std::cout << "Capturing: (" << pose.x << ", " << pose.y << ", " << pose.yaw << ")" << std::endl;
			bool success = capturePose(pose);
			if (!success) {
				std::cout << "ERROR: Failed to move to pose!" << std::endl;
				return false;
			}
			ignition::msgs::CameraInfo * camera_info_msg;
			ignition::msgs::Image * image_msg;
			ignition::msgs::Pose_V * pose_msg;
			// Now get the most up to date messages. There might be a bit of a lag in updating the values, so check
			// the pose to see if it matches approximately what we would expect.
			bool pose_updated = false;
			while (!pose_updated) {
				auto messages = data_synchronizer.getMessages();
				// Cast each message back into the expected format.
				camera_info_msg = dynamic_cast<ignition::msgs::CameraInfo *>(messages["/camera_info"].get());
				image_msg = dynamic_cast<ignition::msgs::Image *>(messages["/camera"].get());
				pose_msg = dynamic_cast<ignition::msgs::Pose_V *>(messages["/world/ground_texture/dynamic_pose/info"].get());
				// Compare values to verify updated pose. Account for floating point accuracy.
				ignition::msgs::Pose extracted_pose;
				for (int i = 0; i < pose_msg->pose_size(); ++i) {
					if (pose_msg->pose(i).name() == "camera") {
						extracted_pose = pose_msg->pose(i);
					}
				}
				// We want all pose values to be updated, so flip to false if any aren't within eps.
				pose_updated = true;
				double eps = 1e-8;
				pose_updated &= abs(extracted_pose.position().x() - pose.x) <= eps;
				pose_updated &= abs(extracted_pose.position().y() - pose.y) <= eps;
				// We have to pull out the quaternion values.
				ignition::math::Quaternion quaternion(extracted_pose.orientation().w(), extracted_pose.orientation().x(), extracted_pose.orientation().y(), extracted_pose.orientation().z());
				pose_updated &= abs(quaternion.Yaw() - pose.yaw) <= eps;
			}

			// Write them to file.
			data_writer.registerCameraInfo(*camera_info_msg);
			data_writer.registerPose(*pose_msg);
			data_writer.registerImage(*image_msg);
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
		ignition::msgs::Pose pose_request;
		pose_request.set_name("camera");
		pose_request.mutable_position()->set_x(pose.x);
		pose_request.mutable_position()->set_y(pose.y);
		pose_request.mutable_position()->set_z(getCameraHeight());
		// Convert the yaw to quaternion first. Yes, only X and W change, but this future proofs it.
		// Also, the camera is tilted down, so planar rotation is about the X-axis.
		ignition::math::Quaternion<float> quaternion(0.0, 0.0, pose.yaw);
		pose_request.mutable_orientation()->set_x(quaternion.X());
		pose_request.mutable_orientation()->set_y(quaternion.Y());
		pose_request.mutable_orientation()->set_z(quaternion.Z());
		pose_request.mutable_orientation()->set_w(quaternion.W());
		ignition::msgs::Boolean response;
		bool result;
		unsigned int timeout = 1000;
		bool executed = node.Request("/world/ground_texture/set_pose", pose_request, timeout, response, result);
		// We get three ways to check if it worked!
		return executed && result && response.data();
	}
} // namespace ground_texture_sim
