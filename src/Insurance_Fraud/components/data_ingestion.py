import os
import zipfile
import urllib.request as request
from pathlib import Path
from src.Insurance_Fraud.constants import *
from src.Insurance_Fraud.utils.common import *
from src.Insurance_Fraud.logger.logger import logger
from src.Insurance_Fraud.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        logger.info(f"Downloading data from {self.config.source_url}")
        if not os.path.exists(self.config.local_data_file):
            logger.info(f"Downloading data from {self.config.source_url}")
            filename, headers = request.urlretrieve(
                url = self.config.source_url,
                filename = self.config.local_data_file
            )
            logger.info(f"Downloaded data from {self.config.source_url} to {self.config.local_data_file}")
            
    def extract_zip_file(self):
        logger.info(f"Extracting data from {self.config.local_data_file}")
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        logger.info(f"Extracted data from {self.config.local_data_file} to {self.config.unzip_dir}")

    def __del__(self):
        logger.info(f"Data ingestion completed successfully. Files are saved in {self.config.unzip_dir}")