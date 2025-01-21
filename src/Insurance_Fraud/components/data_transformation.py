from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
import pandas as pd
from src.Insurance_Fraud.entity.config_entity import DataTransformationConfig
import os
from src.Insurance_Fraud.logger.logger import logger
import numpy as np

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def initiate_data_transformation(self):
        logger.info(f"Reading data from {self.config.data_path}")
        df = pd.read_csv(self.config.data_path)
        logger.info(f"Data read successfully from {self.config.data_path}")

        numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
        logger.info(f"Numerical columns: {numerical_columns}")

        categorical_columns = df.select_dtypes(include=['object']).columns
        logger.info(f"Categorical columns: {categorical_columns}")

        df.replace('?', np.nan, inplace=True)
        logger.info(f"Replacing '?' with NaN in categorical columns")

        for col in categorical_columns:
            df[col].fillna(df[col].mode()[0], inplace=True)
            logger.info(f"Filling NaN values in {col} with mode of {col}")

        for col in numerical_columns:
            df[col].fillna(df[col].median(), inplace=True)
            logger.info(f"Filling NaN values in {col} with median of {col}")

        df['loss_ratio'] = df['total_claim_amount'] / (df['policy_annual_premium'] * 12)
        logger.info(f"Calculating loss ratio")

        df['profitability'] = (df['policy_annual_premium'] * 12) - df['total_claim_amount']
        logger.info(f"Calculating profitability")

        df['vehicle_age'] = 2025 - df['auto_year']
        logger.info(f"Calculating vehicle age")

        df.drop('auto_year', axis=1, inplace=True)
        logger.info(f"Dropping auto_year column")

        df['incident_date'] = pd.to_datetime(df['incident_date'])
        df['incident_year'] = df['incident_date'].dt.year
        df['incident_month'] = df['incident_date'].dt.month
        df['incident_day'] = df['incident_date'].dt.day
        df.drop('incident_date',axis=1,inplace=True)
        logger.info(f"Dropping incident_date column")

        df['policy_bind_date'] = pd.to_datetime(df['policy_bind_date'], errors='coerce')
        df['policy_bind_year'] = df['policy_bind_date'].dt.year
        df['policy_bind_month'] = df['policy_bind_date'].dt.month
        df['policy_bind_day'] = df['policy_bind_date'].dt.day
        df.drop('policy_bind_date',axis=1,inplace=True)        
        logger.info(f"Dropping policy_bind_date column")

        df = pd.concat([df,pd.get_dummies(df['incident_type'],drop_first=True).astype(int)],axis=1)
        df.drop('incident_type',axis=1,inplace=True)
        logger.info(f"One-hot encoding incident_type column")

        df = pd.concat([df,pd.get_dummies(df['collision_type'],drop_first=True).astype(int)],axis=1)
        df.drop('collision_type',axis=1,inplace=True)
        logger.info(f"One-hot encoding collision_type column")

        df = pd.concat([df,pd.get_dummies(df['authorities_contacted'],drop_first=True).astype(int)],axis=1)
        df.drop('authorities_contacted',axis=1,inplace=True)
        logger.info(f"One-hot encoding authorities_contacted column")

        df = pd.concat([df,pd.get_dummies(df['incident_severity'],drop_first=True).astype(int)],axis=1)
        df.drop('incident_severity',axis=1,inplace=True)
        logger.info(f"One-hot encoding incident_severity column")

        df = pd.concat([df,pd.get_dummies(df['policy_csl'],drop_first=True).astype(int)],axis=1)
        df.drop('policy_csl',axis=1,inplace=True)
        logger.info(f"One-hot encoding policy_csl column")

        df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 45, 55, 100], labels=['18-25', '26-35', '36-45', '46-55', '55+'])
        logger.info(f"Creating age_group column")

        encoder = LabelEncoder()
        df[df.select_dtypes(include=['object']).columns] = df[df.select_dtypes(include=['object']).columns].apply(encoder.fit_transform)
        df['age_group'] = encoder.fit_transform(df['age_group'])
        logger.info(f"Encoding categorical columns")

        # Separate the majority and minority classes
        logger.info(f"Separating majority and minority classes")
        majority_class = df[df['fraud_reported'] == 0]
        minority_class = df[df['fraud_reported'] == 1]
        logger.info(f"Successfully separated majority and minority classes")

        # Perform undersampling on the majority class
        logger.info(f"Performing undersampling on the majority class")
        majority_downsampled = resample(majority_class, 
                                        replace=False, 
                                        n_samples=500,  # Reduce to 500 samples
                                        random_state=42)

        # Perform oversampling on the minority class
        logger.info(f"Performing oversampling on the minority class")
        minority_oversampled = resample(minority_class, 
                                        replace=True, 
                                        n_samples=500,  # Increase to 500 samples
                                        random_state=42)

        # Combine the balanced classes
        balanced_df = pd.concat([majority_downsampled, minority_oversampled])
        logger.info(f"Successfully combined balanced classes")

        # Shuffle the dataset
        logger.info(f"Shuffling the dataset")
        balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)
        logger.info(f"Successfully shuffled the dataset")

        train, test = train_test_split(balanced_df, test_size=0.25, random_state=42)
        logger.info(f"Successfully split the dataset into train and test")

        train.to_csv(os.path.join(self.config.root_dir, "train.csv"), index=False)
        logger.info(f"Successfully saved train data to {os.path.join(self.config.root_dir, 'train.csv')}")

        test.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=False)
        logger.info(f"Successfully saved test data to {os.path.join(self.config.root_dir, 'test.csv')}")

        logger.info(f"Data transformation completed successfully and saved to {self.config.root_dir}")
        logger.info(f"Train data shape: {train.shape}")
        logger.info(f"Test data shape: {test.shape}")