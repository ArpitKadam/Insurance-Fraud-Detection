import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from src.Insurance_Fraud.logger.logger import logger
from src.Insurance_Fraud.entity.config_entity import ModelTrainerConfig
import os


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        """
        Train the model using Gradient Boosting Classifier.
        """
        logger.info("Loading train and test data")
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)
        
        logger.info(f"Train Data: {train_data.head()}")
        logger.info(f"Test Data: {test_data.head()}")

        logger.info("Dropping target column from train and test data")
        train_x = train_data.drop([self.config.target_column], axis=1)
        train_y = train_data[self.config.target_column]
        
        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[self.config.target_column]
        
        logger.info(f"Train X columns: {train_x.columns}")
        logger.info(f"Test X columns: {test_x.columns}")

        logger.info("Initializing Standard Scaler")
        scaler = StandardScaler()
        logger.info("Fitting Standard Scaler on train data")
        train_x_scaled = scaler.fit_transform(train_x)
        logger.info("Transforming train data using Standard Scaler")
        test_x_scaled = scaler.transform(test_x)
        logger.info("Transforming test data using Standard Scaler")

        logger.info("Scaling train and test data")
        logger.info(f"Train X Scaled: {train_x_scaled[:5]}")
        logger.info(f"Test X Scaled: {test_x_scaled[:5]}")

        logger.info("Initializing Gradient Boosting Classifier")
        model = GradientBoostingClassifier(
            learning_rate=self.config.learning_rate,
            max_depth=self.config.max_depth,
            n_estimators=self.config.n_estimators,
            subsample=self.config.subsample
        )
        
        logger.info(f"Model: {model}")

        logger.info("Fitting model on train data")
        model.fit(train_x_scaled, train_y)

        logger.info("Dumping model to disk")
        model_path = os.path.join(self.config.root_dir, self.config.model_name)
        joblib.dump(model, model_path)

        logger.info(f"Model trained and saved to {model_path}")
        logger.info(f"Model: {model}")
        
        return model
