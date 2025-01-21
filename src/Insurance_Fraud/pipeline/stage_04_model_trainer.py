from src.Insurance_Fraud.components.model_trainer import ModelTrainer
from src.Insurance_Fraud.config.configuration import ConfigurationManager
from src.Insurance_Fraud.logger.logger import logger
from pathlib import Path

STAGE_NAME = "Model Trainer Stage"

class ModelTrainerPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager(config_file_path=Path("C:/Users/Arpit Kadam/Desktop/Insurance-Fraud-Detection/config/config.yaml"),
                                            params_file_path=Path("C:/Users/Arpit Kadam/Desktop/Insurance-Fraud-Detection/params.yaml"),
                                            schema_file_path=Path("C:/Users/Arpit Kadam/Desktop/Insurance-Fraud-Detection/schema.yaml"))
            model_trainer_config = config.get_model_trainer_config()
            model_trainer = ModelTrainer(config=model_trainer_config)
            model = model_trainer.train()
            logger.info(f"Model training completed successfully")
        except Exception as e:
            logger.info(f"Error in model training: {e}")
            raise e

if __name__ == "__main__":
    try:
        logger.info(f"******************* {STAGE_NAME} *******************")
        obj = ModelTrainerPipeline()
        obj.main()
        logger.info(f"******************* {STAGE_NAME} completed *******************")
    except Exception as e:
        logger.info(f"Error in model training: {e}")
        raise e
