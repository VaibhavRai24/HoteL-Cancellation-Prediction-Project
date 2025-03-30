import os
import sys
import yaml
from pandas import DataFrame
from Exceptions import MyException
from logger import logging
import pandas as pd


def read_yaml_file(file_path: str) -> dict:
    try:
        if not os.path.exists(file_path):
            logging.info(f"File path {file_path} does not exist.")
            return None
        
        with open(file_path, 'r') as yaml_file_to_be_read:
                return yaml.safe_load(yaml_file_to_be_read)
        
    except Exception as e:
            raise MyException(e, sys) from e
    
    
def load_data(file_path:str) ->DataFrame:
    """
    Basically this function will load the data from the given file path.
    file_path: str location of file to load
    
    """
    try:
        if not os.path.exists(file_path):
            logging.info(f"File path {file_path} does not exist or found")
            return None
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        raise MyException(e, sys) from e
    
def save_data(file_path:str, data:DataFrame) -> None:
    """
    Basically this function will save the data to the given file path.
    file_path: str location of file to save
    data: DataFrame data to save
    
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        data.to_csv(file_path, index=False)
    except Exception as e:
        raise MyException(e, sys) from e