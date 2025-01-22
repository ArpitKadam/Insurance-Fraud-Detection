from src.Insurance_Fraud.components.model_trainer import ModelTrainer
from src.Insurance_Fraud.config.configuration import ConfigurationManager
from src.Insurance_Fraud.logger.logger import logger

STAGE_NAME = "Model Trainer Stage"


class ModelTrainerPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            # Load configuration files
            config = ConfigurationManager(
                config_file_path="config/config.yaml",
                params_file_path="params.yaml",
                schema_file_path="schema.yaml"
            )

            # Get model trainer config
            model_trainer_config = config.get_model_trainer_config()

            # Initialize ModelTrainer and train the model
            model_trainer = ModelTrainer(config=model_trainer_config)
            model_trainer.train()

            # Log the successful model training
            logger.info("Model training completed successfully")
        except Exception as e:
            # Log error in model training
            logger.error(f"Error in model training: {e}")
            raise e


if __name__ == "__main__":
    try:
        # Log the start of the stage
        logger.info(f"******************* {STAGE_NAME} *******************")
        
        # Run the pipeline
        pipeline = ModelTrainerPipeline()
        pipeline.main()
        
        # Log the completion of the stage
        logger.info(f"******************* {STAGE_NAME} completed *******************")
    except Exception as e:
        # Log any exception in the pipeline
        logger.error(f"Error in model training: {e}")
        raise e
