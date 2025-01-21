from src.Insurance_Fraud.logger.logger import logger
from src.Insurance_Fraud.entity.config_entity import DataValidationConfig
import pandas as pd
from src.Insurance_Fraud.entity.config_entity import DataValidationConfig
import os


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            df = pd.read_csv(self.config.unzip_data_dir)
            if not os.path.exists(self.config.unzip_data_dir):
                raise FileNotFoundError(f"Expected file not found: {self.config.unzip_data_dir}")
            validation_status = True
            with open(self.config.STATUS_FILE, 'w') as f:
                for column, expected_dtype in self.config.all_schema.items():
                    if column in df.columns:
                        actual_dtype = df[column].dtype
                        ##print(f"Checking column: {column}, Expected: {expected_dtype}, Found: {actual_dtype}")
                        f.write(f"Checking column: {column}, Expected: {expected_dtype}, Found: {actual_dtype}\n")
                        if actual_dtype != expected_dtype:
                            validation_status = False
                            f.write(f"Column {column} has incorrect dtype. Expected: {expected_dtype}, Found: {actual_dtype}\n")
                    else:
                        validation_status = False
                        f.write(f"Column {column} is missing in the data.\n")
                
                if validation_status:
                    f.write("All columns are valid and have correct data types.\n")  # Write success message

            with open(self.config.STATUS_FILE, 'w') as f:
                f.write("Validation Status\n")
                f.write("****************************************************\n")
                f.write(str(validation_status) + '\n')
                f.write("****************************************************\n")
                f.write('Data Description\n')
                f.write("****************************************************\n")
                f.write(str(df.head()) + '\n')
                f.write("****************************************************\n")
                f.write('Data Info\n')
                f.write("****************************************************\n")
                f.write(str(df.info()) + '\n')
                f.write("****************************************************\n")
                f.write('Data Describe\n')
                f.write("****************************************************\n")
                f.write(str(df.describe()) + '\n')
                f.write("****************************************************\n")
                f.write('Data Shape\n')
                f.write("****************************************************\n")
                f.write(str(df.shape) + '\n')
                f.write("****************************************************\n")

            return validation_status
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
  
