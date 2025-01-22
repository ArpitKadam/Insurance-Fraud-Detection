from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
import pandas as pd
from src.Insurance_Fraud.entity.config_entity import DataTransformationConfig
import os
from src.Insurance_Fraud.logger.logger import logger
import numpy as np
import joblib


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def initiate_data_transformation(self):
        logger.info(f"Reading data from {self.config.data_path}")
        df = pd.read_csv(self.config.data_path)
        logger.info(f"Data read successfully from {self.config.data_path}")

        # Removing unnecessary columns
        df.drop("policy_number", axis=1, inplace=True)
        df.drop("insured_hobbies", axis=1, inplace=True)
        df.drop("insured_zip", axis=1, inplace=True)
        df.drop("incident_location", axis=1, inplace=True)
        logger.info("Removed meaningless columns")

        # Replacing '?' with NaN in categorical columns
        df.replace('?', np.nan, inplace=True)
        logger.info("Replaced '?' with NaN in categorical columns")

        # Separate numerical and categorical columns
        numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
        logger.info(f"Numerical columns: {numerical_columns}")

        categorical_columns = df.select_dtypes(include=['object']).columns
        logger.info(f"Categorical columns: {categorical_columns}")

        # Fill NaN values for categorical columns with mode 
        #   and for numerical columns with median
        for col in categorical_columns:
            df[col].fillna(df[col].mode()[0], inplace=True)
            logger.info(f"Filling NaN values in {col} with mode of {col}")

        for col in numerical_columns:
            df[col].fillna(df[col].median(), inplace=True)
            logger.info(f"Filling NaN values in {col} with median of {col}")

        # Feature engineering: Calculate new columns
        df['loss_ratio']=df['total_claim_amount']/(df['policy_annual_premium']*12)
        logger.info("Calculating loss ratio")

        df['profitability']=(df['policy_annual_premium']*12)-df['total_claim_amount']
        logger.info("Calculating profitability")

        df['vehicle_age'] = 2025 - df['auto_year']
        logger.info("Calculating vehicle age")

        df.drop('auto_year', axis=1, inplace=True)
        logger.info("Dropped auto_year column")

        # Convert 'incident_date' to datetime and extract year, month, day
        df['incident_date'] = pd.to_datetime(df['incident_date'])
        df['incident_year'] = df['incident_date'].dt.year
        df['incident_month'] = df['incident_date'].dt.month
        df['incident_day'] = df['incident_date'].dt.day
        df.drop('incident_date', axis=1, inplace=True)
        logger.info("Dropped incident_date column")

        # Convert 'policy_bind_date' to datetime and extract year, month, day
        df['policy_bind_date'] = pd.to_datetime(df['policy_bind_date'], errors='coerce')
        df['policy_bind_year'] = df['policy_bind_date'].dt.year
        df['policy_bind_month'] = df['policy_bind_date'].dt.month
        df['policy_bind_day'] = df['policy_bind_date'].dt.day
        df.drop('policy_bind_date', axis=1, inplace=True)
        logger.info("Dropped policy_bind_date column")

        # One-hot encoding categorical variables
        incident_type_dummies=pd.get_dummies(df['incident_type'],drop_first=True).astype(int)
        df = pd.concat([df, incident_type_dummies], axis=1)
        df.drop('incident_type', axis=1, inplace=True)
        logger.info("One-hot encoding incident_type column")

        collision_type_dummies=pd.get_dummies(df['collision_type'],drop_first=True).astype(int)
        df = pd.concat([df, collision_type_dummies], axis=1)
        df.drop('collision_type', axis=1, inplace=True)
        logger.info("One-hot encoding collision_type column")

        authorities_contacted_dummies=pd.get_dummies(df['authorities_contacted'],drop_first=True).astype(int)
        df = pd.concat([df, authorities_contacted_dummies], axis=1)
        df.drop('authorities_contacted', axis=1, inplace=True)
        logger.info("One-hot encoding authorities_contacted column")

        incident_severity_dummies=pd.get_dummies(df['incident_severity'],drop_first=True).astype(int)
        df = pd.concat([df, incident_severity_dummies], axis=1)
        df.drop('incident_severity', axis=1, inplace=True)
        logger.info("One-hot encoding incident_severity column")

        policy_csl_dummies=pd.get_dummies(df['policy_csl'],drop_first=True).astype(int)
        df = pd.concat([df, policy_csl_dummies], axis=1)
        df.drop('policy_csl', axis=1, inplace=True)
        logger.info("One-hot encoding policy_csl column")

        # Convert 'age' column to numeric and create 'age_group' column
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
        logger.info("Converting age column to numeric")

        # Create age groups and drop the original 'age' column
        age_bins = [0, 25, 35, 45, 55, 100]
        age_labels = ['18-25', '26-35', '36-45', '46-55', '55+']
        df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels).astype(object)
        logger.info("Created 'age_group' column")
        df.drop('age', axis=1, inplace=True)
        logger.info("Dropped age column")

        # Encoding categorical columns
        encoder_dict = {}
        encoder = LabelEncoder()
        categorical_columns = df.select_dtypes(include=['object']).columns
        logger.info(f"Encoding categorical columns: {categorical_columns}")

        for col in categorical_columns:
            df[col] = encoder.fit_transform(df[col]).astype(int)
            encoder_dict[col] = encoder
        logger.info("Completed encoding categorical columns")

        # Save encoders
        save_dir = os.path.join("artifacts", "data_transformation")
        file_name = "encoders.pkl"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
            logger.info(f"Created directory {save_dir}")

        file_path = os.path.join(save_dir, file_name)
        joblib.dump(encoder_dict, file_path)
        logger.info(f"Saved encoders to {file_path}")

        # Balancing the dataset using resampling
        logger.info("Separating majority and minority classes")
        majority_class = df[df['fraud_reported'] == 0]
        minority_class = df[df['fraud_reported'] == 1]
        logger.info("Successfully separated majority and minority classes")

        # Perform undersampling on the majority class
        logger.info("Performing undersampling on the majority class")
        majority_downsampled = resample(majority_class,
                                        replace=False,
                                        n_samples=500,  # Reduce to 500 samples
                                        random_state=42)

        # Perform oversampling on the minority class
        logger.info("Performing oversampling on the minority class")
        minority_oversampled = resample(minority_class,
                                        replace=True,
                                        n_samples=500,  # Increase to 500 samples
                                        random_state=42)

        # Combine the balanced classes
        balanced_df = pd.concat([majority_downsampled, minority_oversampled])
        logger.info("Successfully combined balanced classes")

        # Shuffle the dataset
        logger.info("Shuffling the dataset")
        balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
        logger.info("Successfully shuffled the dataset")

        # Split the dataset into train and test sets
        train, test = train_test_split(balanced_df, test_size=0.25, random_state=42)
        logger.info("Successfully split the dataset into train and test")

        # Save the train and test datasets
        train.to_csv(os.path.join(self.config.root_dir, "train.csv"), index=False)
        logger.info("Successfully saved train data to path")
        logger.info(f"{os.path.join(self.config.root_dir, 'train.csv')}")
        logger.info(f"Train data shape: {train.shape}")

        test.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=False)
        logger.info("Successfully saved test data to path")
        logger.info(f"{os.path.join(self.config.root_dir, 'test.csv')}")
        logger.info(f"Test data shape: {test.shape}")

        logger.info("Data transformation completed successfully")
        logger.info(f"Train data shape: {train.shape}")
        logger.info(f"Test data shape: {test.shape}")
        logger.info(f"Files are saved in {self.config.root_dir}")
