from src.Insurance_Fraud.config.configuration import ConfigurationManager
from src.Insurance_Fraud.components.model_evaluation import ModelEvaluation
from src.Insurance_Fraud.logger.logger import logger

STAGE_NAME = "Model Evaluation Stage"

class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            model_evaluation_config = config.get_model_evaluation_config()
            model_evaluation = ModelEvaluation(config=model_evaluation_config)
            model_evaluation.log_into_mlflow()
            logger.info("Model evaluation completed successfully")
        except Exception as e:
            logger.info(f"Error during model evaluation: {e}")
            raise e
    

if __name__ == "__main__":
    try:
        logger.info(f"******************* {STAGE_NAME} started *******************")
        obj = ModelEvaluationTrainingPipeline()
        obj.main()
        logger.info(f"******************* {STAGE_NAME} completed *******************")
    except Exception as e:
        logger.info(f"Error during model evaluation: {e}")
        raise e