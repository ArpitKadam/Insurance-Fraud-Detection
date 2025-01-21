from src.Insurance_Fraud.constants import *
from src.Insurance_Fraud.utils.common import read_yaml, create_directories
from pathlib import Path
from src.Insurance_Fraud.entity.config_entity import DataIngestionConfig
from src.Insurance_Fraud.logger.logger import logger
from src.Insurance_Fraud.entity.config_entity import DataValidationConfig

class ConfigurationManager:
    def __init__(
        self,
        config_file_path = Path(CONFIG_FILE_PATH),
        params_file_path = Path(PARAMS_FILE_PATH),
        schema_file_path = Path(SCHEMA_FILE_PATH)
    ):
        
        self.config = read_yaml(Path(config_file_path))
        self.params = read_yaml(Path(params_file_path))
        self.schema = read_yaml(Path(schema_file_path))

        logger.info(f"Config: {self.config}")
        logger.info(f"Params: {self.params}")
        logger.info(f"Schema: {self.schema}")
        logger.info(f"Artifacts Root: {self.config['artifacts_root']}")
        create_directories([self.config['artifacts_root']])

    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config['data_ingestion']
        logger.info(f"Config: {config}")
        create_directories([config['root_dir']])
        logger.info(f"Root Dir: {config['root_dir']}")
        data_ingestion_config = DataIngestionConfig(
            root_dir=config['root_dir'],
            source_url=config['source_url'],
            local_data_file=config['local_data_file'],
            unzip_dir=config['unzip_dir']
        )
        logger.info(f"Data Ingestion Config: {data_ingestion_config}")
        logger.info(f"Data Ingestion Config Root Dir: {data_ingestion_config.root_dir}")
        logger.info(f"Data Ingestion Config Source URL: {data_ingestion_config.source_url}")
        logger.info(f"Data Ingestion Config Local Data File: {data_ingestion_config.local_data_file}")
        logger.info(f"Data Ingestion Config Unzip Dir: {data_ingestion_config.unzip_dir}")
        if 'data_ingestion' not in self.config:
            raise ValueError("'data_ingestion' section missing in config file")

        return data_ingestion_config


    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config['data_validation']
        schema = self.schema['COLUMNS']

        create_directories([config['root_dir']])

        data_validation_config = DataValidationConfig(
            root_dir=config['root_dir'],
            unzip_data_dir=config['unzip_data_dir'],
            STATUS_FILE=config['STATUS_FILE'],
            all_schema=schema
        )

        return data_validation_config