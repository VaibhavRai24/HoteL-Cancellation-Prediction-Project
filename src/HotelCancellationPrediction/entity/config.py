import os
from src.HotelCancellationPrediction.constants import *
from dataclasses import dataclass
from pathlib import Path

@dataclass
class TrainingPipelineConfig:
    pipeline_name:str = PIPELINE_NAME
    arifact_dir:str = RAW_DIR
    TIMESTAMP:str =TIMESTAMP
    
training_pipeline_config:TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir:str = Path(RAW_DIR)
    raw_file_path:str = Path(RAW_FILE_PATH)
    training_file_path:str = Path(TRAIN_FILE_PATH)
    testing_file_path:str = Path(TEST_FILE_PATH)
    config_file_path:str = Path(CONFIG_PATH)
    config_file:float = os.path.join(config_file_path, "config.yaml")
    collection_name:str = CONNECTION_NAME
    database_name:str = DB_NAME