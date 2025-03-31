import os
from datetime import date

DB_NAME = 'hotel'
CONNECTION_NAME = "hotel-cancellation-data"
CONNECTION_URL = "mongodb+srv://VaibhavRai:Vaibhav1212@cluster0.kq7ntil.mongodb.net/hotel?retryWrites=true&w=majority&appName=Cluster0"

PIPELINE_NAME: str = "Hotel-Cancellation-Prediction"
TIMESTAMP = date.today().strftime("%m_%d_%Y_%H_%M_%S")

RAW_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

CONFIG_PATH = "Configs/config.yaml"

PROCESSED_DIR = "artifacts/processed"
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv")
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv")