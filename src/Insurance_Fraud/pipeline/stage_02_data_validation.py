from src.Insurance_Fraud.config.configuration import ConfigurationManager
from src.Insurance_Fraud.components.data_validation import DataValidation
from src.Insurance_Fraud.logger.logger import logger
from pathlib import Path

STAGE_NAME = "Data Validation Stage"


class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager(config_file_path=Path("C:/Users/Arpit Kadam/Desktop/Insurance-Fraud-Detection/config/config.yaml"),
                                params_file_path=Path("C:/Users/Arpit Kadam/Desktop/Insurance-Fraud-Detection/params.yaml"),
                                schema_file_path=Path("C:/Users/Arpit Kadam/Desktop/Insurance-Fraud-Detection/schema.yaml"))
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_all_columns()

if __name__ == "__main__":
    try:
        logger.info(f"*******************{STAGE_NAME}*******************")
        obj = DataValidationTrainingPipeline()
        obj.main()
        logger.info(f"*******************{STAGE_NAME}*******************")
    except Exception as e:
        logger.exception(e)
        raise e
