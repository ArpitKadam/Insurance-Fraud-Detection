import os
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from src.Insurance_Fraud.logger.logger import logger
from src.Insurance_Fraud.exception.exception import NetworkSecurityException


class PredictionPipeline:
    def __init__(self):
        self.model_path = os.path.join(
            "artifacts", "model_trainer", "GradientBoostingClassifier.joblib"
    )
        self.encoder_dict = os.path.join(
            "artifacts", "data_transformation", "encoders.pkl"
    )

    def preprocess_data(self, input_data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the input data before making predictions
        """
        try:
            # Create a copy of input data
            df = input_data.copy()
            print(df.columns)

            # Drop unused columns
            columns_to_drop = [
                'policy_number',
                'insured_hobbies',
                'insured_zip',
                'incident_location'
            ]
            df = df.drop(
                [col for col in columns_to_drop if col in df.columns],
                axis=1
            )
            logger.info(f"Columns dropped: {columns_to_drop}")

            df['total_claim_amount'] = pd.to_numeric(
                df['total_claim_amount'],
                errors='coerce'
            )
            df['policy_annual_premium'] = pd.to_numeric(
                df['policy_annual_premium'],
                errors='coerce'
            )
            logger.info("Policy annual premium converted to numeric")

            # Handle dates
            if 'incident_date' in df.columns:
                df['incident_date'] = pd.to_datetime(
                    df['incident_date'],
                    errors='coerce'
                )
                df['incident_year'] = df['incident_date'].dt.year
                df['incident_month'] = df['incident_date'].dt.month
                df['incident_day'] = df['incident_date'].dt.day
                df = df.drop('incident_date', axis=1)

            if 'policy_bind_date' in df.columns:
                df['policy_bind_date'] = pd.to_datetime(
                    df['policy_bind_date'],
                    errors='coerce'
                )
                df['policy_bind_year'] = df['policy_bind_date'].dt.year
                df['policy_bind_month'] = df['policy_bind_date'].dt.month
                df['policy_bind_day'] = df['policy_bind_date'].dt.day
                df = df.drop('policy_bind_date', axis=1)
                logger.info("Policy bind date processed")

            # Calculate vehicle age
            if 'auto_year' in df.columns:
                df['auto_year'] = pd.to_numeric(df['auto_year'], errors='coerce')
                df['vehicle_age'] = 2025 - df['auto_year']
                df = df.drop('auto_year', axis=1)
                logger.info("Vehicle age calculated")

            # Calculate financial ratios
            if all(col in df.columns for col in ['total_claim_amount','policy_annual_premium']):
                df['loss_ratio']=df['total_claim_amount']/(df['policy_annual_premium']*12)
                df['profitability']=(df['policy_annual_premium']*12)-df['total_claim_amount']
                logger.info("Financial ratios calculated")

            # One-hot encoding for categorical variables
            categorical_columns = [
                'incident_type', 'collision_type', 'authorities_contacted',
                'incident_severity', 'policy_csl'
            ]
            
            for col in categorical_columns:
                if col in df.columns:
                    df = pd.concat(
                        [df, pd.get_dummies(df[col], prefix=col, drop_first=True)],
                        axis=1
                    )
                    df = df.drop(col, axis=1)
                    logger.info(f"One-hot encoded {col}")

            # Age grouping
            if 'age' in df.columns:
                df['age'] = pd.to_numeric(df['age'], errors='coerce')
                df['age_group'] = pd.cut(
                    df['age'],
                    bins=[0, 25, 35, 45, 55, 100],
                    labels=['18-25', '26-35', '36-45', '46-55', '55+']
                ).astype(object)
                df.drop('age', axis=1, inplace=True)
                logger.info("Age grouped")
            # Handle remaining categorical columns
            encoder = joblib.load(self.encoder_dict)
            for col, encoder in encoder.items():
                if col in df.columns:
                    df[col] = df[col].apply(
                        lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1
                    )
                    logger.info(f"Encoded {col}")
                    logger.info(df[col])
            logger.info(df.columns)

            # Standard scaling
            scaler = StandardScaler()
            numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
            df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
            logger.info("Numeric columns scaled")
            model_features = [
                'months_as_customer', 'policy_state',
                'policy_deductable', 'policy_annual_premium',
                'umbrella_limit', 'insured_sex', 'insured_education_level',
                'insured_occupation', 'insured_relationship',
                'capital_gains', 'capital_loss', 'incident_city',
                'incident_state', 'incident_hour_of_the_day',
                'number_of_vehicles_involved', 'property_damage', 
                'bodily_injuries', 'witnesses', 'police_report_available',
                'total_claim_amount', 'injury_claim', 'property_claim', 
                'vehicle_claim', 'auto_make', 'auto_model',
                'loss_ratio', 'profitability', 'vehicle_age', 'incident_year',
                'incident_month', 'incident_day', 'policy_bind_year',
                'policy_bind_month', 'policy_bind_day', 'Parked Car',
                'Single Vehicle Collision', 'Vehicle Theft', 'Rear Collision',
                'Side Collision', 'Fire', 'None', 'Other', 'Police', 'Minor Damage',
                'Total Loss', 'Trivial Damage', '250/500', '500/1000', 'age_group'
            ]
            for col in model_features:
                if col not in df.columns:
                    df[col] = 0 
            logger.info("Model features selected")
            df = df[model_features]
            logger.info(df.columns)
            return df

        except Exception as e:
            logger.info(f"Error in preprocessing: {e}")
            raise NetworkSecurityException(e)

    def predict(self, features: pd.DataFrame) -> dict:
        try:
            # Load model
            model = joblib.load(self.model_path)
            logger.info("Model loaded successfully")

            # Preprocess features
            processed_features = self.preprocess_data(features)
            logger.info("Features preprocessed successfully")

            # Make prediction
            prediction = model.predict(processed_features)
            probability = model.predict_proba(processed_features)
            
            return {
                'prediction': bool(prediction[0]),
                'probability': float(probability[0][1]),
                'prediction_text': (
                    'Fraud Detected' if prediction[0] == 1 else 'No Fraud Detected'
                )            
            }

        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            raise NetworkSecurityException(e)
