#include "transform_math.h"

namespace ground_texture_sim {
	ignition::msgs::Pose poseMsgFromPose2D(const Pose2D & pose2D) {
		ignition::msgs::Pose pose;
		pose.mutable_position()->set_x(pose2D.x);
		pose.mutable_position()->set_y(pose2D.y);
		pose.mutable_position()->set_z(0.0);
		// Use existing functions to set rotation.
		auto rotation = quaternionMsgFromYaw(pose2D.yaw);
		pose.mutable_orientation()->Swap(&rotation);
		return pose;
	}

	ignition::msgs::Quaternion quaternionMsgFromYaw(double yaw) {
		auto quaternion = quaternionFromYaw(yaw);
		ignition::msgs::Quaternion quaternion_msg;
		quaternion_msg.set_x(quaternion.X());
		quaternion_msg.set_y(quaternion.Y());
		quaternion_msg.set_z(quaternion.Z());
		quaternion_msg.set_w(quaternion.W());
		return quaternion_msg;
	}

	std::tuple<double, double, double> RPYFromQuaternionMsg(const ignition::msgs::Quaternion & quaternion) {
		ignition::math::Quaternion quaternion_math(quaternion.w(), quaternion.x(), quaternion.y(), quaternion.z());
		double roll = quaternion_math.Roll();
		double pitch = quaternion_math.Pitch();
		double yaw = quaternion_math.Yaw();
		return std::make_tuple(roll, pitch, yaw);
	}
} // namespace ground_texture_sim