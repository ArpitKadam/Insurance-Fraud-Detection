from src.Insurance_Fraud.config.configuration import ConfigurationManager
from src.Insurance_Fraud.components.data_ingestion import DataIngestion
from src.Insurance_Fraud.logger.logger import logger
from src.Insurance_Fraud.entity.config_entity import DataIngestionConfig
from src.Insurance_Fraud.exception.exception import NetworkSecurityException
import sys
from pathlib import Path



STAGE_NAME = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager(config_file_path=Path("C:/Users/Arpit Kadam/Desktop/Insurance-Fraud-Detection/config/config.yaml"),
                                params_file_path=Path("C:/Users/Arpit Kadam/Desktop/Insurance-Fraud-Detection/params.yaml"),
                                schema_file_path=Path("C:/Users/Arpit Kadam/Desktop/Insurance-Fraud-Detection/schema.yaml"))
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.download_file()
            data_ingestion.extract_zip_file()
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        

if __name__ == "__main__":
    try:
        logger.info(f">>>>>>>>>>>>>>>Stage {STAGE_NAME} started<<<<<<<<<<<<<<<<<<<<<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>>>>>>>>>>Stage {STAGE_NAME} completed<<<<<<<<<<<<<<<<<<<<<<<")
    except Exception as e:
        logger.info(f"Error in stage {STAGE_NAME}: {e}")
        raise e