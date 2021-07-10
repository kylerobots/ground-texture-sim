#ifndef _DATA_WRITER_H_
#define _DATA_WRITER_H_

#include "transform_math.h"

#include <filesystem>
#include <ignition/common/Image.hh>
#include <ignition/msgs.hh>
#include <ostream>
#include <string>
#include <vector>

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
	 * particular, it receives images from the camera, camara parameters, and the pose of the camera. Each are then
	 * written out to numerically labeled, monotonically increasing file names. (e.g. 000000.txt, 000001.txt, etc.)
	 * 
	 */
	class DataWriter {
		public:
		/**
		 * @brief Construct a new DataWriter object.
		 * 
		 * By default, the writer writes to the working directory.
		 * 
		 */
		DataWriter();

		/**
		 * @brief Construct a new Data Writer object.
		 * 
		 * The data will be written to the data_folder, which can be an absolute path or relative to the working
		 * directory. If the folder does not exist, it will be created.
		 * 
		 * @param data_folder Folder where the data should go. Can be absolute or relative. This folder will be created
		 * if it does not already exist.
		 */
		DataWriter(const std::string & data_folder);

		/**
		 * @brief Get where the data should be written.
		 * 
		 * @param relative True if the returned string should be relative to the current directory, false if absolute.
		 * @return std::string The folder for the data. This will be absolute or relative, depending on the value of
		 * relative.
		 */
		std::string getDataFolder(bool relative = false) const;

		/**
		 * @brief Set where the data should be written.
		 * 
		 * This can be absolute or relative to the current working directory. If the folder does not exist, it will
		 * be created. Calling this again will not remove previously created directories.
		 * 
		 * @param data_folder Folder where the data should go. Can be absolute or relative. This folder will be created
		 * if it does not already exist.
		 * @throws boost::filesystem::filesystem_error is thrown if the object cannot create the requested directory.
		 */
		void setDataFolder(const std::string & data_folder);

		/**
		 * @brief Write the data to files.
		 * 
		 * When called, it will write the data to a series of indexed files of the following formats:
		 * 
		 * | data type | file format |
		 * | --- | --- |
		 * | image | 000000.png |
		 * | pose | 000000.txt |
		 * | camera_info | 000000_calib.txt |
		 * 
		 * The index of the file name will be incremented by one each time. If there are more than 1,000,000 images,
		 * any value over 999999 will be used as the file name without leading zeros. In other words, earlier files
		 * will still have 6 digits including leading zeros while latter will have no leading zeros and just the index
		 * number.
		 * 
		 * @param image The Image message to write.
		 * @param pose The Pose message to write.
		 * @param camera_info The CameraInfo message to write.
		 * @return true if everything was written successfully.
		 * @return false if there was a problem writing. The index will still increase to avoid issues.
		 */
		bool writeData(const ignition::msgs::Image & image, const ignition::msgs::Pose & pose, ignition::msgs::CameraInfo & camera_info);

		protected:
		/**
		 * @brief Returns a string of the write format based on the current index.
		 * 
		 * This string is the 6 digit leading zero format, without any file extensions or modifiers. It als includes the
		 * directory of the file.
		 * 
		 * @return std::string The path and base name for the current iteration of files.
		 */
		std::string getBaseFilename() const;

		/**
		 * @brief Write the given camera info to the file with index for the filename.
		 * 
		 * File names are of the form 000000_calib.txt, 000001_calib.txt, etc. File format is exactly the same as
		 * the DebugString of the message.
		 * 
		 * @param camera_info The camera info to write.
		 * @return true if the write was successful.
		 * @return false otherwise.
		 */
		bool writeCameraInfo(const ignition::msgs::CameraInfo & camera_info);

		/**
		 * @brief Write the given image to the file with index for the filename.
		 * 
		 * File names are of the form 000000.png, 000001.png, etc.
		 * 
		 * @param image The image to write.
		 * @return true if the write was successful.
		 * @return false otherwise.
		 */
		bool writeImage(const ignition::msgs::Image & image);

		/**
		 * @brief Write the given pose to the file with index for the filename.
		 * 
		 * File names are of the form 000000.txt, 000001.txt, etc. File format is:
		 * 
		 * x,y,z,roll,pitch,yaw
		 * 
		 * @param pose The pose to write.
		 * @return true if the write was successful.
		 * @return false otherwise.
		 */
		bool writePose(const ignition::msgs::Pose & pose);

		protected:
		/// The directory to place the written files.
		std::filesystem::path data_folder;
		/// The count of how many images have been written to file.
		unsigned int index;
	};

} // namespace ground_texture_sim

#endif // _DATA_WRITER_H_