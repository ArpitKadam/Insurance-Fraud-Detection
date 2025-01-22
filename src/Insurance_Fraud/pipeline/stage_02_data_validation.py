from src.Insurance_Fraud.config.configuration import ConfigurationManager
from src.Insurance_Fraud.components.data_validation import DataValidation
from src.Insurance_Fraud.logger.logger import logger
from pathlib import Path

STAGE_NAME = "Data Validation Stage"


class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            # Initialize Configuration Manager
            config = ConfigurationManager(
                config_file_path=Path("config/config.yaml"),
                params_file_path=Path("params.yaml"),
                schema_file_path=Path("schema.yaml")
            )           
            # Retrieve Data Validation configuration
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValidation(config=data_validation_config)          
            # Perform data validation
            logger.info("Starting data validation process...")
            data_validation.validate_all_columns()
            logger.info("Data validation completed successfully.")     
        except Exception as e:
            # Catch and log any exceptions raised during the process
            logger.error(f"Error in {STAGE_NAME}: {e}")
            raise e

if __name__ == "__main__":
    try:
        # Log the start of the Data Validation stage
        logger.info(f">> Stage {STAGE_NAME} started <<")
        # Run the Data Validation pipeline
        obj = DataValidationTrainingPipeline()
        obj.main()
        # Log the successful completion of the stage
        logger.info(f">> Stage {STAGE_NAME} completed <<")
    except Exception as e:
        # Log any unhandled exceptions and re-raise them
        logger.exception(f"Error during {STAGE_NAME}: {e}")
        raise e
