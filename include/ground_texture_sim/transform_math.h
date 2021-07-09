#ifndef _TRANSFORM_MATH_H_
#define _TRANSFORM_MATH_H_

#include <ignition/math/Quaternion.hh>

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

	double blah() {
		return 0.0;
	}

	template <typename Scalar = float>
	ignition::math::Quaternion<Scalar> quaternionFromYaw(Scalar yaw) {
		ignition::math::Quaternion<Scalar> quaternion(Scalar(0.0), Scalar(0.0), yaw);
		// static_cast<Scalar>(0.0), static_cast<Scalar>(0.0), yaw);
		return quaternion;
	}

} // namespace ground_texture_sim

#endif // _TRANSFORM_MATH_H_