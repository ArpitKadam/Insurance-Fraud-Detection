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
            # Read status file for data validation status
            status_file_path = Path("artifacts/data_validation/STATUS.txt")
            if status_file_path.exists():
                with open(status_file_path, "r") as f:
                    content = f.read()
                    status = content.split(
                        "****************************************************"
                    )[0].split(" ")[1].strip()
                    logger.info(status)
                    print(status)

                if status == "True":
                    try:
                        # Load configurations
                        config = ConfigurationManager(
                            config_file_path=Path("config/config.yaml"),
                            params_file_path=Path("params.yaml"),
                            schema_file_path=Path("schema.yaml")
                        )

                        # Get data transformation config and start transformation
                        data_trans_config = config.get_data_transformation_config()
                        data_transformation = DataTransformation(
                            config=data_trans_config
                        )
                        data_transformation.initiate_data_transformation()
                    
                    except FileNotFoundError as e:
                        logger.error(f"Error: Please check the file path: {e}")
                        raise e
                    
                    except Exception as e:
                        logger.error(f"An unexpected error occurred : {e}")
                        raise e
                else:
                    raise Exception("Your Data is not Validated")
            else:
                raise FileNotFoundError(
                    "Validation status file not found",
                    f"Please check the file path: {status_file_path}"
                )
        except Exception as e:
            logger.exception(f"Error during {STAGE_NAME}: {e}")
            raise e

if __name__ == "__main__":
    try:
        logger.info(f">> Stage {STAGE_NAME} started <<")       
        # Run the Data Transformation pipeline
        obj = DataTransformationTrainingPipeline()
        obj.main()
        logger.info(f">> Stage {STAGE_NAME} completed <<")
    except Exception as e:
        logger.exception(f"Error during {STAGE_NAME}: {e}")
        raise e
