"""!
@brief Code to generate what the names of paths and files should be.
"""
import datetime
from os import path


class NameConfigurator:
    """!
    @brief A class to assist with configuring the names of image files, folders, and list files.
    """

    def __init__(self, output_folder: str, sequence_type: str, sequence_number: int,
                 texture_number: int, camera_name: str) -> None:
        """!
        @brief Construct the class with given sequence and texture information.
        @param output_folder The root output folder under which all data resides.
        @param sequence_type A string description of which type of data collection run this is.
        @param sequence_number A unique number, relative to the date and sequence type, to identify
        this particular data collection event.
        @param texture_number An integer representing the texture type mapped.
        @param camera_name The name of the camera in Blender.
        """
        ## The absolute path of the folder containing all data.
        self._output_folder = path.abspath(output_folder)
        ## The current date data is collected
        self._current_date = datetime.date.today()
        ## A string description of which type of data collection run this is.
        self._sequence_type = sequence_type
        ## A unique number, relative to the date and sequence type, to identify this event.
        self._sequence_number = sequence_number
        ## An integer representing the texture type mapped.
        self._texture_number = texture_number
        ## The name of the camera in Blender.
        self._camera_name = camera_name
        ## The base name of the three top-level files listing images and poses.
        self._base_name = F'{self._sequence_type}_{self._current_date.strftime("%y%m%d")}'

    def create_image_path(self, index: int, absolute: bool = False) -> str:
        """!
        @brief Assemble the directory and name of a particular image to use for its path.

        From the output directory, this will go in:
        ```
        sequence_type/date_collected/sequence_number/
        HDG$VersionNumber_t$TextureNumber_$SequenceType_
        $DateOfRecording_s$SequenceNumber_c01_i$ImageNumber.png
        ```

        @param index The image number to use
        @param absolute True if the returned path should be absolute, false if it should be relative
        to *output*.
        @return A relative path to the image location, relative to the output directory.
        """
        # Create the directory relative to the output folder.
        date_folder = self._current_date.strftime('%y%m%d')
        sequence_number_folder = F'seq{self._sequence_number:04d}'
        file_directory = path.join(
            self._sequence_type, date_folder, sequence_number_folder)
        # Then the filename
        texture_name = F't{self._texture_number:03d}'
        date_name = self._current_date.strftime('%Y-%m-%d')
        sequence_number_name = F's{self._sequence_number:04d}'
        image_name = F'i{index:07d}'
        file_name = F'HDG2_{texture_name}_{self._sequence_type}_{date_name}' \
            F'_{sequence_number_name}_{self._camera_name}_{image_name}.png'
        result = path.join(file_directory, file_name)
        # Make absolute or relative, depending on the specification
        if absolute:
            result = path.join(self._output_folder, result)
        return result

    @property
    def meters_txt_file(self) -> None:
        """!
        @brief Return the absolute path of the *_meters.txt file.
        @return The absolute path for that file.
        """
        return F'{self._base_name}_meters.txt'

    @property
    def test_file(self) -> None:
        """!
        @brief Return the absolute path of the *.test file.
        @return The absolute path for that file.
        """
        return F'{self._base_name}.test'

    @property
    def txt_file(self) -> None:
        """!
        @brief Return the absolute path of the *.txt file.
        @return The absolute path for that file.
        """
        return F'{self._base_name}.txt'
