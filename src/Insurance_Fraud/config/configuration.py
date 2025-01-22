from src.Insurance_Fraud.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.Insurance_Fraud.utils.common import read_yaml, create_directories
from pathlib import Path
from src.Insurance_Fraud.entity.config_entity import (DataIngestionConfig,
                                                      DataValidationConfig,
                                                      DataTransformationConfig,
                                                      ModelTrainerConfig,
                                                      ModelEvaluationConfig
                                                    )
from src.Insurance_Fraud.logger.logger import logger


class ConfigurationManager:
    def __init__(
        self,
        config_file_path=Path(CONFIG_FILE_PATH),
        params_file_path=Path(PARAMS_FILE_PATH),
        schema_file_path=Path(SCHEMA_FILE_PATH)
    ): 
        self.config=read_yaml(Path(config_file_path))
        self.params=read_yaml(Path(params_file_path))
        self.schema=read_yaml(Path(schema_file_path))
        ## Log config, params, and schema
        logger.info(f"Config: {self.config}")
        logger.info(f"Params: {self.params}")
        logger.info(f"Schema: {self.schema}")
        logger.info(f"Artifacts Root: {self.config['artifacts_root']}")
        create_directories([self.config['artifacts_root']])

    ## Get data ingestion config
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config['data_ingestion']
        logger.info(f"Config: {config}")
        create_directories([config['root_dir']])
        logger.info(f"Root Dir: {config['root_dir']}")
        data_ingestion_config=DataIngestionConfig(
            root_dir=config['root_dir'],
            source_url=config['source_url'],
            local_data_file=config['local_data_file'],
            unzip_dir=config['unzip_dir']
        )
        logger.info("Data Ingestion Config:")
        logger.info(data_ingestion_config)
        logger.info("Data Ingestion Config Root Dir:")
        logger.info(data_ingestion_config.root_dir)
        logger.info("Data Ingestion Config Source URL:")
        logger.info(data_ingestion_config.source_url)
        logger.info("Data Ingestion Config Local Data File:")
        logger.info(data_ingestion_config.local_data_file)
        logger.info("Data Ingestion Config Unzip Dir:")
        logger.info(data_ingestion_config.unzip_dir)
        if 'data_ingestion' not in self.config:
            raise ValueError("'data_ingestion' missing in config file")
        return data_ingestion_config

    ## Get into data validation config
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config['data_validation']
        schema = self.schema['COLUMNS']
        logger.info(f"Config: {config}")
        logger.info(f"Schema: {schema}")
        create_directories([config['root_dir']])
        ## Create data validation config
        data_validation_config = DataValidationConfig(
            root_dir=config['root_dir'],
            unzip_data_dir=config['unzip_data_dir'],
            STATUS_FILE=config['STATUS_FILE'],
            all_schema=schema
        )
        logger.info("Data Validation Config:")
        logger.info(data_validation_config)
        logger.info("Data Validation Config Root Dir:")
        logger.info(data_validation_config.root_dir)
        logger.info("Data Validation Config Unzip Data Dir:")
        logger.info(data_validation_config.unzip_data_dir)
        logger.info("Data Validation Config Status File:")
        logger.info(data_validation_config.STATUS_FILE)
        logger.info("Data Validation Config All Schema:")
        logger.info(data_validation_config.all_schema)
        return data_validation_config
    
    ## Get into data transformation config
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config['data_transformation']
        create_directories([config['root_dir']])
        logger.info(f"Config: {config}")
        ## Create data transformation config
        data_transformation_config=DataTransformationConfig(
            root_dir=config['root_dir'],
            data_path=config['data_path']
        )    
        logger.info("Data Transformation Config:")
        logger.info(data_transformation_config)
        logger.info("Data Transformation Config Root Dir:")
        logger.info(data_transformation_config.root_dir)
        logger.info("Data Transformation Config Data Path:")
        logger.info(data_transformation_config.data_path)
        return data_transformation_config
    
    ## Get into model trainer config
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config['model_trainer']
        params = self.params['GradientBoostingClassifier']
        logger.info(f"Config: {config}")
        logger.info(f"Params: {params}")
        ## Check if 'TARGET_COLUMN' exists in schema
        target_column_info=self.schema['TARGET_COLUMN']
        if not isinstance(target_column_info, dict) or len(target_column_info) != 1:
            logger.error("Invalid TARGET_COLUMN format in schema")
            raise ValueError("TARGET_COLUMN should have exactly one key-value pair in schema")
        ## Extract the key (e.g., 'fraud_reported')
        target_column=list(target_column_info.keys())[0] 
        logger.info(f"Target Column: {target_column}")
        ## Create model trainer config
        create_directories([config['root_dir']])
        logger.info(f"Root Dir: {config['root_dir']}")
        ## Create model trainer config
        model_trainer_config=ModelTrainerConfig(
            root_dir=config['root_dir'],
            train_data_path=config['train_data_path'],
            test_data_path=config['test_data_path'],
            model_name=config['model_name'],
            learning_rate=params['learning_rate'],
            max_depth=params['max_depth'],
            n_estimators=params['n_estimators'],
            subsample=params['subsample'],
            target_column=target_column
        )
        logger.info("Model Trainer Config:")
        logger.info(model_trainer_config)
        logger.info("Model Trainer Config Root Dir:")
        logger.info(model_trainer_config.root_dir)
        logger.info("Model Trainer Config Train Data Path:")
        logger.info(model_trainer_config.train_data_path)
        logger.info("Model Trainer Config Test Data Path:")
        logger.info(model_trainer_config.test_data_path)
        logger.info("Model Trainer Config Model Name:")
        logger.info(model_trainer_config.model_name)
        logger.info("Model Trainer Config Learning Rate:")
        logger.info(model_trainer_config.learning_rate)
        logger.info("Model Trainer Config Max Depth:")
        logger.info(model_trainer_config.max_depth)
        logger.info("Model Trainer Config N Estimators:")
        logger.info(model_trainer_config.n_estimators)
        logger.info("Model Trainer Config Subsample:")
        logger.info(model_trainer_config.subsample)
        logger.info("Model Trainer Config Target Column:")
        logger.info(model_trainer_config.target_column)
        return model_trainer_config
    
    ## Get into model evaluation config
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config=self.config["model_evaluation"]
        params=self.params["GradientBoostingClassifier"]
        ## Get target column from schema
        schema_target=self.schema["TARGET_COLUMN"]
        target_column=list(schema_target.keys())[0]
        create_directories([config["root_dir"]])
        ## Create model evaluation config
        model_evaluation_config=ModelEvaluationConfig(
            root_dir=config["root_dir"],
            test_data_path=config["test_data_path"],
            model_path=config["model_path"],
            all_params=params,
            metric_file_name=config["metric_file_name"],
            target_column=target_column,
            artifact_dir=config["artifact_dir"],
            mlflow_uri="https://dagshub.com/ArpitKadam/Insurance-Fraud-Detection.mlflow",
            mlflow_experiment_name="insurance_fraud_experiment",
            mlflow_run_name="run_4",
            mlflow_model_name="GradientBoostingClassifier"
        )
        logger.info("Model Evaluation Config:")
        logger.info(model_evaluation_config)
        logger.info("Model Evaluation Config Root Dir:")
        logger.info(model_evaluation_config.root_dir)
        logger.info("Model Evaluation Config Test Data Path:")
        logger.info(model_evaluation_config.test_data_path)
        logger.info("Model Evaluation Config Model Path:")
        logger.info(model_evaluation_config.model_path)
        logger.info("Model Evaluation Config All Params:")
        logger.info(model_evaluation_config.all_params)
        logger.info("Model Evaluation Config Metric File Name:")
        logger.info(model_evaluation_config.metric_file_name)
        logger.info("Model Evaluation Config Target Column:")
        logger.info(model_evaluation_config.target_column)
        logger.info("Model Evaluation Config Artifact Dir:")
        logger.info(model_evaluation_config.artifact_dir)
        logger.info("Model Evaluation Config Mlflow Uri:")
        logger.info(model_evaluation_config.mlflow_uri)
        logger.info("Model Evaluation Config Mlflow Experiment Name:")
        logger.info(model_evaluation_config.mlflow_experiment_name)
        logger.info("Model Evaluation Config Mlflow Run Name:")
        logger.info(model_evaluation_config.mlflow_run_name)
        return model_evaluation_config
