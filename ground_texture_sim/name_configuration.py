"""!
Code to generate what the names of paths and files should be.
"""
import datetime
from os import path
from typing import Dict


def create_image_path(index: int, configs: Dict) -> str:
    """!
    Assemble the directory and name of the particular image to use for the filename.

    From the output directory, this will go in:
    ```
    sequence_type/date_collected/sequence_number/
    HDG$VersionNumber_t$TextureNumber_$SequenceType_
    $DateOfRecording_s$SequenceNumber_c01_i$ImageNumber.png
    ```

    @param index The image number to use
    @param configs The well-formatted Dict containing the necessary sequence settings
    @return An absolute path to the image location.
    """
    current_date = datetime.date.today()
    # First, assemble the directory
    sequence_type_folder = configs['sequence']['sequence_type']
    date_folder = current_date.strftime('%y%m%d')
    sequence_number_folder = F'seq{configs["sequence"]["sequence_number"]:04d}'
    file_directory = path.join(
        configs['output'], sequence_type_folder, date_folder, sequence_number_folder)
    # Then the filename
    texture_name = F't{configs["sequence"]["texture_number"]:03d}'
    sequence_type_name = F'{configs["sequence"]["sequence_type"]}'
    date_name = current_date.strftime('%Y-%m-%d')
    sequence_number_name = F's{configs["sequence"]["sequence_number"]:04d}'
    camera_name = F'{configs["camera"]["name"]}'
    image_name = F'i{index:07d}'
    file_name = F'HDG2_{texture_name}_{sequence_type_name}_{date_name}' \
        F'_{sequence_number_name}_{camera_name}_{image_name}.png'
    full_path = path.abspath(path.join(file_directory, file_name))
    return full_path


def create_file_list_base(configs: Dict) -> str:
    """!
    Create the base name of the three top level files that list images and poses.

    @param configs The well-formatted Dict containing the necessary sequence settings
    @return The base name of the files, without the extensions, path, or "_meters" suffix.
    """
    current_date = datetime.date.today()
    base_name = F'{configs["sequence"]["sequence_type"]}_{current_date.strftime("%y%m%d")}'
    return base_name
