import os
import sys
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from src.Insurance_Fraud.logger.logger import logger


class PredictionPipeline:
    def __init__(self):
        self.model = joblib.load(Path("artifacts/model_trainer/GradientBoostingClassifier.joblib"))
    
    def predict(self, data):
        prediction = self.model.predict(data)
        return prediction


