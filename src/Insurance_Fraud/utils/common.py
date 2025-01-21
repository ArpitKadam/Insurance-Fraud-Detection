import os
from pathlib import Path
import yaml
import sys

# Add the project root directory to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from src.Insurance_Fraud.logger.logger import logger
from src.Insurance_Fraud.exception.exception import NetworkSecurityException
from ensure import ensure_annotations
from typing import Any
import json
import joblib


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> dict:
    logger.info(f"Attempting to read YAML file from: {path_to_yaml}")
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
        return content
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Creates directories from a list of paths.
    """
    try:
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)
            if verbose:
                logger.info(f"Directory created: {path}")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e



@ensure_annotations
def save_json(path: Path, data: dict):
    # Ensure the path is a pathlib.Path object
    if isinstance(path, str):
        path = Path(path)
    # Now save the data to the file
    with open(path, 'w') as f:
        json.dump(data, f)
    logger.info(f"json file saved at: {path}")

@ensure_annotations
def load_json(path: Path) -> dict:
    with open(path) as f:
        content = json.load(f)
    logger.info(f"json file loaded successfully from: {path}")
    return content


@ensure_annotations
def save_bin(data: Any, path: Path):
    joblib.dump(data, path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    data = joblib.load(path)
    logger.info(f"binary file loaded successfully from: {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    size_in_kb = round(os.path.getsize(path)/1024)
    logger.info(f"size of the file: {path} is {size_in_kb} KB")
    return size_in_kb
    