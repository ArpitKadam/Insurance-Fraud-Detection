from src.Insurance_Fraud.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from src.Insurance_Fraud.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from src.Insurance_Fraud.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline
from src.Insurance_Fraud.pipeline.stage_04_model_trainer import ModelTrainerPipeline
from src.Insurance_Fraud.pipeline.stage_05_model_evaluation import ModelEvaluationTrainingPipeline
from src.Insurance_Fraud.exception.exception import NetworkSecurityException
from src.Insurance_Fraud.logger.logger import logger
import sys

def run_pipeline(stage_name: str, pipeline_obj):
    try:
        logger.info(f">>>>>>>>>>>>>>>Stage {stage_name} started<<<<<<<<<<<<<<<<<<<<<<<<<")
        pipeline_obj.main()
        logger.info(f">>>>>>>>>>>>>>>Stage {stage_name} completed<<<<<<<<<<<<<<<<<<<<<<<")
    except Exception as e:
        logger.error(f"Error in stage {stage_name}: {e}")
        raise NetworkSecurityException(e, sys) from e


if __name__ == "__main__":
    # Running each stage pipeline
    run_pipeline("Data Ingestion Stage", DataIngestionTrainingPipeline())
    run_pipeline("Data Validation Stage", DataValidationTrainingPipeline())
    run_pipeline("Data Transformation Stage", DataTransformationTrainingPipeline())
    run_pipeline("Model Trainer Stage", ModelTrainerPipeline())
    run_pipeline("Model Evaluation Stage", ModelEvaluationTrainingPipeline())
