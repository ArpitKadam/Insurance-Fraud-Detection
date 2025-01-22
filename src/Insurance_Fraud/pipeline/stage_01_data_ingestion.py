from src.Insurance_Fraud.config.configuration import ConfigurationManager
from src.Insurance_Fraud.components.data_ingestion import DataIngestion
from src.Insurance_Fraud.logger.logger import logger
from src.Insurance_Fraud.exception.exception import NetworkSecurityException
import sys
from pathlib import Path

STAGE_NAME = "Data Ingestion Stage"


class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            # Configuration Manager for file paths
            config = ConfigurationManager(
                config_file_path=Path("config/config.yaml"),
                params_file_path=Path("params.yaml"),
                schema_file_path=Path("schema.yaml")
            )
            # Get the Data Ingestion configuration
            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            # Perform data ingestion tasks
            data_ingestion.download_file()
            data_ingestion.extract_zip_file()
        except Exception as e:
            # Catching and raising a custom exception with traceback
            logger.error(f"Error during {STAGE_NAME}: {e}")
            raise NetworkSecurityException(e, sys) from e
        
if __name__ == "__main__":
    try:
        # Logging the start of the stage
        logger.info(f">> Stage {STAGE_NAME} started <<")  
        # Create pipeline object and run main method
        obj = DataIngestionTrainingPipeline()
        obj.main()        
        # Logging the completion of the stage
        logger.info(f">> Stage {STAGE_NAME} completed <<")
    except Exception as e:
        # Log any errors at the top level
        logger.error(f"Error in stage {STAGE_NAME}: {e}")
        raise e
