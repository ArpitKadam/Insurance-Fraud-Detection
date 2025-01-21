from src.Insurance_Fraud.components.data_transformation import DataTransformation
from src.Insurance_Fraud.config.configuration import ConfigurationManager
from src.Insurance_Fraud.logger.logger import logger
from pathlib import Path

STAGE_NAME = "Data Transformation Stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            with open(Path("artifacts/data_validation/STATUS.txt"), "r") as f:
                status = f.read().split("****************************************************")[1].split(" ")[1]
                status = status.strip()

            if status == "True":
                try:
                    config = ConfigurationManager(config_file_path=Path("C:/Users/Arpit Kadam/Desktop/Insurance-Fraud-Detection/config/config.yaml"),
                                                params_file_path=Path("C:/Users/Arpit Kadam/Desktop/Insurance-Fraud-Detection/params.yaml"),
                                                schema_file_path=Path("C:/Users/Arpit Kadam/Desktop/Insurance-Fraud-Detection/schema.yaml"))
                    data_transformation_config = config.get_data_transformation_config()
                    data_transformation = DataTransformation(config=data_transformation_config)
                    data_transformation.initiate_data_transformation()
                except FileNotFoundError as e:
                    print(f"Error: Input data file not found. Please check the file path: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
            else:
                raise Exception("Your Data is not Validated")
        except Exception as e:
            logger.exception(e)
            raise e

if __name__ == "__main__":
    try:
        logger.info(f"*******************{STAGE_NAME}*******************")
        obj = DataTransformationTrainingPipeline()
        obj.main()
        logger.info(f"*******************{STAGE_NAME}*******************")
    except Exception as e:
        logger.exception(e)
        raise e
