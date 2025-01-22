from src.Insurance_Fraud.logger.logger import logger
from src.Insurance_Fraud.entity.config_entity import DataValidationConfig
import pandas as pd
import os


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            logger.info("Validating all columns")
            logger.info(f"Files are saved in {self.config.unzip_data_dir}")
            # Check if the file exists before reading
            if not os.path.exists(self.config.unzip_data_dir):
                raise FileNotFoundError(f"not found: {self.config.unzip_data_dir}")
            df = pd.read_csv(self.config.unzip_data_dir)
            validation_status = True
            logger.info("Reading data from path")
            logger.info(f"{self.config.unzip_data_dir}")
            with open(self.config.STATUS_FILE, 'w') as f:
                for column, expected_dtype in self.config.all_schema.items():
                    if column in df.columns:
                        actual_dtype = df[column].dtype
                        logger.info(f"Checking column: {column}")
                        logger.info(f"Expected: {expected_dtype}")
                        logger.info(f"Found: {actual_dtype}")
                        f.write(f"Checking column: {column}\n")
                        f.write(f"Expected: {expected_dtype}\n")
                        f.write(f"Found: {actual_dtype}\n")
                        if actual_dtype != expected_dtype:
                            validation_status = False
                            logger.info(f"Column {column} has incorrect dtype")
                            f.write(f"Column {column} has incorrect dtype\n")
                    else:
                        validation_status = False
                        logger.info(f"{column} is missing in the data.")
                        f.write(f"{column} is missing in the data.\n")
                ## Write success message
                if validation_status:
                    f.write("All columns are valid")
                    f.write("And have correct data types.\n")
                    logger.info("All columns are valid")
                    logger.info("And have correct data types.")
            # Writing validation status and data details
            logger.info("Writing validation status to path")
            logger.info(f"{self.config.STATUS_FILE}")
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write('Status: ' + str(validation_status) + '\n')
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
            ## Write success message
            logger.info("Validation completed successfully")
            logger.info(f"Status file saved to {self.config.STATUS_FILE}")
            logger.info(f"Validation status: {validation_status}")
            return validation_status
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise e
