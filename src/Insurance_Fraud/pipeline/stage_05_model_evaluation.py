from src.Insurance_Fraud.config.configuration import ConfigurationManager
from src.Insurance_Fraud.components.model_evaluation import ModelEvaluation
from src.Insurance_Fraud.logger.logger import logger

STAGE_NAME = "Model Evaluation Stage"


class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            # Load the configuration
            config = ConfigurationManager()
            model_evaluation_config = config.get_model_evaluation_config()

            # Initialize the ModelEvaluation and perform logging into MLFlow
            model_evaluation = ModelEvaluation(config=model_evaluation_config)
            model_evaluation.log_into_mlflow()

            # Log successful model evaluation
            logger.info("Model evaluation completed successfully")
        except Exception as e:
            # Log error during model evaluation
            logger.error(f"Error during model evaluation: {e}")
            raise e


if __name__ == "__main__":
    try:
        # Log the start of the evaluation stage
        logger.info(f"******************* {STAGE_NAME} started *******************")
        
        # Run the pipeline
        pipeline = ModelEvaluationTrainingPipeline()
        pipeline.main()
        
        # Log the successful completion of the evaluation stage
        logger.info(f"******************* {STAGE_NAME} completed *******************")
    except Exception as e:
        # Log any exception in the pipeline
        logger.error(f"Error during model evaluation: {e}")
        raise e
