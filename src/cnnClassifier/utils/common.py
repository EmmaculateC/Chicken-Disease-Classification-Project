import os  
from box.exceptions import BoxValueError  
import yaml 
from cnnClassifier import logger  
import json  
import joblib  
from ensure import ensure_annotations  
from box import ConfigBox  
from pathlib import Path  
from typing import Any  
import base64


# Reads YAML files and converts them into a ConfigBox object
@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its content in a ConfigBox format.

    Args:
        path_to_yaml (Path): Path to the YAML file.

    Raises:
        ValueError: If the YAML file is empty.
        Exception: For other file-related errors.

    Returns:
        ConfigBox: Data in ConfigBox format, which allows accessing content like attributes.
    """
    try:
        with open(path_to_yaml) as yaml_file:  # Open YAML file in read mode
            content = yaml.safe_load(yaml_file)  # Load YAML content safely
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")  # Log success
            return ConfigBox(content)  # Return content in ConfigBox format
    except BoxValueError:  # Handles empty YAML files
        raise ValueError("yaml file is empty")
    except Exception as e:  # Handles other exceptions
        raise e


# Creates multiple directories if they don't exist
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Creates a list of directories.

    Args:
        path_to_directories (list): List of directory paths.
        verbose (bool): Logs directory creation if True (default).
    """
    for path in path_to_directories:  # Iterate through each directory path
        os.makedirs(path, exist_ok=True)  # Create directory if it doesn't exist
        if verbose:  # Log the directory creation if verbose is enabled
            logger.info(f"created directory at: {path}")


# Saves data as a JSON file
@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Saves data to a JSON file.

    Args:
        path (Path): Path to the JSON file.
        data (dict): Data to save in JSON format.
    """
    with open(path, "w") as f:  # Open JSON file in write mode
        json.dump(data, f, indent=4)  # Write data with 4-space indentation
    logger.info(f"json file saved at: {path}")  # Log success


# Loads data from a JSON file
@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Loads JSON data from a file.

    Args:
        path (Path): Path to the JSON file.

    Returns:
        ConfigBox: Data as class attributes instead of a dictionary.
    """
    with open(path) as f:  # Open JSON file in read mode
        content = json.load(f)  # Load JSON content
    logger.info(f"json file loaded successfully from: {path}")  # Log success
    return ConfigBox(content)  # Return content in ConfigBox format


# Saves data as a binary file
@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Saves data to a binary file.

    Args:
        data (Any): Data to save as binary.
        path (Path): Path to the binary file.
    """
    joblib.dump(value=data, filename=path)  # Save binary data
    logger.info(f"binary file saved at: {path}")  # Log success


# Loads binary data from a file
@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Loads binary data from a file.

    Args:
        path (Path): Path to the binary file.

    Returns:
        Any: Object stored in the file.
    """
    data = joblib.load(path)  # Load binary data
    logger.info(f"binary file loaded from: {path}")  # Log success
    return data  # Return loaded data


# Gets the size of a file in kilobytes (KB)
@ensure_annotations
def get_size(path: Path) -> str:
    """
    Returns the size of a file in KB.

    Args:
        path (Path): Path to the file.

    Returns:
        str: Size of the file in KB (rounded).
    """
    size_in_kb = round(os.path.getsize(path) / 1024)  # Calculate size in KB
    return f"~ {size_in_kb} KB"  # Return formatted size

def decodeImage(imgstring, filename):
    imgdata = base64.b64decode(imgstring)
    with open(filename, 'wb') as f:
        f.write(imgdata)
        f.close()
    
def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, 'rb') as f:
        return base64.b64encode(f.read())
        