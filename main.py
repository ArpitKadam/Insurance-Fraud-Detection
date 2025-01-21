from src.Insurance_Fraud.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from src.Insurance_Fraud.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from src.Insurance_Fraud.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline
from src.Insurance_Fraud.exception.exception import NetworkSecurityException
from src.Insurance_Fraud.logger.logger import logger
import sys
STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f">>>>>>>>>>>>>>>Stage {STAGE_NAME} started<<<<<<<<<<<<<<<<<<<<<<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>>>>>>>>>>>>>Stage {STAGE_NAME} completed<<<<<<<<<<<<<<<<<<<<<<<")
except Exception as e:
    logger.info(f"Error in stage {STAGE_NAME}: {e}")
    raise NetworkSecurityException(e, sys) from e


STAGE_NAME = "Data Validation Stage"
try:
    logger.info(f">>>>>>>>>>>>>>>Stage {STAGE_NAME} started<<<<<<<<<<<<<<<<<<<<<<<<<")
    obj = DataValidationTrainingPipeline()
    obj.main()
    logger.info(f">>>>>>>>>>>>>>>Stage {STAGE_NAME} completed<<<<<<<<<<<<<<<<<<<<<<<")
except Exception as e:
    logger.info(f"Error in stage {STAGE_NAME}: {e}")
    raise NetworkSecurityException(e, sys) from e

STAGE_NAME = "Data Transformation Stage"
try:
    logger.info(f">>>>>>>>>>>>>>>Stage {STAGE_NAME} started<<<<<<<<<<<<<<<<<<<<<<<<<")
    obj = DataTransformationTrainingPipeline()
    obj.main()
    logger.info(f">>>>>>>>>>>>>>>Stage {STAGE_NAME} completed<<<<<<<<<<<<<<<<<<<<<<<")
except Exception as e:
    logger.info(f"Error in stage {STAGE_NAME}: {e}")
    raise NetworkSecurityException(e, sys) from e
