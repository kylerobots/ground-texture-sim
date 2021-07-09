#ifndef _TRANSFORM_MATH_H_
#define _TRANSFORM_MATH_H_

#include <ignition/math/Quaternion.hh>
#include <ignition/msgs/pose.pb.h>
#include <ignition/msgs/quaternion.pb.h>
#include <tuple>

/**
 * @brief The namespace for any class created in this package.
 * 
 * This is mainly implemented to prevent possible collisions with similarly named entities.
 * 
 */
namespace ground_texture_sim {
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

	/**
	 * @brief Convert a yaw value into a Quaternion.
	 * 
	 * This returns the Quaternion representation of a single yaw about the Z-axis. It is templated to accept any
	 * Scalar value, which will most often be double or float.
	 * 
	 * @param yaw The yaw to convert.
	 * @return ignition::math::Quaternion<Scalar> The resulting Quaternion object.
	 */
	template <typename Scalar = float>
	ignition::math::Quaternion<Scalar> quaternionFromYaw(Scalar yaw) {
		ignition::math::Quaternion<Scalar> quaternion(Scalar(0.0), Scalar(0.0), yaw);
		return quaternion;
	}

	/**
	 * @brief Convert a yaw value into a Quaternion message.
	 * 
	 * This returns the Quaternion Message representation of a single yaw about the Z-axis.
	 * 
	 * @param yaw The yaw to convert.
	 * @return ignition::msgs::Quaternion The resulting Quaternion Message object.
	 */
	ignition::msgs::Quaternion quaternionMsgFromYaw(double yaw) {
		auto quaternion = quaternionFromYaw(yaw);
		ignition::msgs::Quaternion quaternion_msg;
		quaternion_msg.set_x(quaternion.X());
		quaternion_msg.set_y(quaternion.Y());
		quaternion_msg.set_z(quaternion.Z());
		quaternion_msg.set_w(quaternion.W());
		return quaternion_msg;
	}

	/**
	 * @brief Convert a Pose2D struct into a Pose message.
	 * 
	 * @param pose2D The struct to convert.
	 * @return ignition::msgs::Pose The resulting Pose message object.
	 */
	ignition::msgs::Pose poseMsgFromPose2D(const Pose2D & pose2D) {
		ignition::msgs::Pose pose;
		return pose;
	}

	/**
	 * @brief Extract the roll, pitch, and yaw from a Quaternion.
	 * 
	 * I believe these are calculate in RPY order.
	 * 
	 * @param quaternion The Quaternion object to extract from.
	 * @return std::tuple<Scalar, Scalar, Scalar> A tuple containing the roll, pitch, and yaw.
	 */
	template <typename Scalar>
	std::tuple<Scalar, Scalar, Scalar> RPYFromQuaternion(const ignition::math::Quaternion<Scalar> & quaternion) {
		Scalar roll;
		Scalar pitch;
		Scalar yaw;
		return std::make_tuple(roll, pitch, yaw);
	}

	/**
	 * @brief Extract the roll, pitch, and yaw from a Quaternion message.
	 * 
	 * I believe these are calculated in RPY order.
	 * 
	 * @param quaternion The Quaternion message object to extract from.
	 * @return std::tuple<double, double, double> A tuple containing the roll, pitch, and yaw.
	 */
	std::tuple<double, double, double> RPYFromQuaternionMsg(const ignition::msgs::Quaternion & quaternion) {
		return std::make_tuple<double, double, double>(0.0, 0.0, 0.0);
	}

} // namespace ground_texture_sim

#endif // _TRANSFORM_MATH_H_