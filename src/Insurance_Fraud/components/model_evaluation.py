import os
import joblib
import mlflow
import pandas as pd
from pathlib import Path
from mlflow.models.signature import infer_signature
from sklearn.metrics import (
    f1_score,
    roc_auc_score,
    accuracy_score,
    precision_score,
    recall_score,
    confusion_matrix,
    classification_report,
)
from sklearn.preprocessing import StandardScaler
from src.Insurance_Fraud.logger.logger import logger
from src.Insurance_Fraud.entity.config_entity import ModelEvaluationConfig
from src.Insurance_Fraud.utils.common import save_json
import dagshub

dagshub.init(repo_owner='ArpitKadam', repo_name='Insurance-Fraud-Detection', mlflow=True)

# Set environment variables for MLflow tracking
os.environ['MLFLOW_TRACKING_URI'] = 'https://dagshub.com/ArpitKadam/Insurance-Fraud-Detection.mlflow'
os.environ['MLFLOW_TRACKING_USERNAME'] = 'ArpitKadam'
os.environ['MLFLOW_TRACKING_PASSWORD'] = '5989d6b56c4eec6ea090d927851d1fb5297a42a8'


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    @staticmethod
    def eval_metrics(actual, pred):
        """
        Evaluate key metrics for model evaluation.
        Returns a dictionary with all metrics and reports.
        """
        metrics = {
            "f1_score": f1_score(actual, pred),
            "roc_auc_score": roc_auc_score(actual, pred),
            "accuracy_score": accuracy_score(actual, pred),
            "precision_score": precision_score(actual, pred),
            "recall_score": recall_score(actual, pred),
            "confusion_matrix": confusion_matrix(actual, pred).tolist(),  # Convert to list for JSON serialization
            "classification_report": classification_report(actual, pred, output_dict=True),  # Dict for better logging
        }
        return metrics

    def log_into_mlflow(self):
        """
        Log metrics and the trained model into MLflow.
        """
        try:
            # Load the test data and trained model
            logger.info("Loading test data and trained model.")
            test_data = pd.read_csv(self.config.test_data_path)
            model = joblib.load(self.config.model_path)
            logger.info(f"Model loaded successfully: {model}")

            # Preprocess test data
            logger.info("Preparing test data for evaluation.")
            test_x = test_data.drop([self.config.target_column], axis=1)
            test_y = test_data[self.config.target_column]
            logger.info(f"Test data shape: {test_x.shape}, Target data shape: {test_y.shape}")

            scaler = StandardScaler()
            test_x_scaled = scaler.fit_transform(test_x)  # Use fit_transform to ensure compatibility
            logger.info("Test data scaled successfully")

            # Set up MLflow tracking
            mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
            logger.info("Starting MLflow run.")
            with mlflow.start_run():
                # Predict and evaluate metrics
                logger.info("Making predictions and evaluating metrics.")
                predicted_qualities = model.predict(test_x_scaled)
                metrics = self.eval_metrics(test_y, predicted_qualities)
                logger.info(f"Metrics: {metrics}")
                save_json(path=Path(self.config.metric_file_name), data=metrics)
                logger.info(f"Metrics saved to {self.config.metric_file_name}")

                # Log metrics to MLflow
                logger.info("Logging metrics to MLflow.")
                for metric_name, metric_value in metrics.items():
                    if isinstance(metric_value, (list, dict)):  # Skip complex objects for metrics
                        continue
                    mlflow.log_metric(metric_name, metric_value)
                logger.info("Metrics logged to MLflow.")

                # Log all model parameters
                logger.info("Logging parameters to MLflow.")
                mlflow.log_params(self.config.all_params)
                logger.info("Parameters logged to MLflow.")

                # Log model with signature
                logger.info("Logging model with signature.")
                signature = infer_signature(test_x_scaled, predicted_qualities)
                mlflow.sklearn.log_model(
                    sk_model=model,
                    artifact_path="model",
                    registered_model_name="GradientBoostingClassifier",
                    signature=signature,
                )
                logger.info("Model logged with signature.")

                # Convert classification report and confusion matrix to strings
                logger.info("Logging classification report and confusion matrix.")
                clf_report = classification_report(test_y, predicted_qualities)
                conf_matrix = confusion_matrix(test_y, predicted_qualities)
                logger.info(f"Classification report: {clf_report}")
                logger.info(f"Confusion matrix: {conf_matrix}")

                # Save them as text files and log as artifacts in MLflow
                logger.info("Saving classification report and confusion matrix as text files.")
                report_path = Path(self.config.artifact_dir) / "classification_report.txt"
                matrix_path = Path(self.config.artifact_dir) / "confusion_matrix.txt"
                logger.info(f"Classification report path: {report_path}")
                logger.info(f"Confusion matrix path: {matrix_path}")

                with open(report_path, "w") as f:
                    f.write(clf_report)
                with open(matrix_path, "w") as f:
                    f.write(str(conf_matrix))
                logger.info("Classification report and confusion matrix saved as text files.")

                mlflow.log_artifact(str(report_path))
                mlflow.log_artifact(str(matrix_path))
                logger.info("Classification report and confusion matrix logged as artifacts in MLflow.")

                logger.info("Model and metrics logged successfully.")

        except Exception as e:
            logger.error(f"Error during model evaluation: {e}")
            raise e
