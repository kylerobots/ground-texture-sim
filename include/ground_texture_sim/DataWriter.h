#ifndef _DATA_WRITER_H_
#define _DATA_WRITER_H_

#include <ignition/common/Image.hh>
#include <ignition/math/Quaternion.hh>
#include <ignition/msgs.hh>
#include <ostream>

/**
 * @brief The namespace for any class created in this package.
 * 
 * This is mainly implemented to prevent possible collisions with similarly named entities.
 * 
 */
namespace ground_texture_sim {
	/**
	 * @brief Captures images and locations from Ignition and writes them to file.
	 * 
	 * This class is designed to receive measurements from the simulation environment in order to generate data. In
	 * particular, it receives images from the camera, camara parameters, and the pose of the camera. Because each my
	 * come in asynchronously, it uses the last updated pose whenever each camera image is received. This might lead to
	 * some errors, but is probably close enough for data collection.
	 * 
	 * The current iteration will just write to file wherever the code is run. This is not ideal, but is a minimum
	 * viable product.
	 * 
	 */
	class DataWriter {
		private:
		/// The count of how many images have been written to file.
		int image_count;
		/// The most recent camera parameters received from the simulation.
		ignition::msgs::CameraInfo current_camera_info;
		/// The most recent image received from the simulation.
		ignition::msgs::Image current_image;
		/// The most recent pose received from the simulation.
		ignition::msgs::Pose current_pose;

		/**
		 * @brief Performs the actual data writing.
		 * 
		 * Before writing to file, this first does some quick data conversions from msg datatypes in order to leverage
		 * Ignition's built in image saving and quaternion conversion functionality.
		 * 
		 */
		void writeData();

		public:
		/**
		 * @brief Construct a new DataWriter object.
		 * 
		 */
		DataWriter();

		/**
		 * @brief Record the camera info published by the simulation.
		 * 
		 * While the info should be unchanging, it will record it each time to make sure.
		 * 
		 */
		void registerCameraInfo(const ignition::msgs::CameraInfo & msg);

		/**
		 * @brief Record the latest image with associated camera info and pose.
		 * 
		 * When an image is received, it records the image, then triggers the write to file actions.
		 * 
		 * @param msg The published Image message.
		 */
		void registerImage(const ignition::msgs::Image & msg);

		/**
		 * @brief Record the latest pose of the camera each time it is published.
		 * 
		 * When received, it will extract the camera's pose and update the member variable. Since this is the only
		 * spot where that variable is written to, no mutex is used.
		 * 
		 * @param msg The published Pose message.
		 */
		void registerPose(const ignition::msgs::Pose_V & msg);
	};

} // namespace ground_texture_sim

#endif // _DATA_WRITER_H_