import os
import sys
import yaml
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from src.HotelCancellationPrediction.entity.config import DataIngestionConfig
from src.HotelCancellationPrediction.entity.artifact import DataIngestionArtifact
from Exceptions import MyException
from logger import logging
from src.HotelCancellationPrediction.DataFetch.data_mongodb import mongodbData

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig=DataIngestionConfig(), config:float = DataIngestionConfig.config_file_path):
        """:param data_ingestion_config: configuration for data ingestion
        """
        try: 
            self.data_ingestion_config = data_ingestion_config
            self.config = config
        except Exception as e:
            raise MyException(e, sys)
        
        
    def export_data_from_mongoDB(self) ->DataFrame:
        """
        Method Name :   export_data_into_feature_store
        Description :   This method exports data from mongodb to csv file
        
        Output      :   data is returned as artifact of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info("Exporting data into feature store in the CSV file from MongoDB")
            my_data = mongodbData()
            dataframe = my_data.export_collection_as_dataframe(collection_name= self.data_ingestion_config.collection_name,database_name= self.data_ingestion_config.database_name )
            logging.info(f" Dataframe shape is {dataframe.shape}")
            feature_store_file_path = self.data_ingestion_config.raw_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok= True)
            logging.info(f" Exporting the data to {feature_store_file_path} if any error occurs then probably it is before the importing of the data , something related to file paths")
            dataframe.to_csv(feature_store_file_path, index= False, header= True)
            return dataframe
        except Exception as e:
            logging.info(" Some error has taken place in the exporting of tha data from mongoDB")
            raise MyException(e, sys)
        
    
    def split_the_train_test_data(self, dataframe: DataFrame) -> None:
        """
        THIS METHOD BASICALLY SPLIT THE DATA INTO THR TRAINING ND THE TESTING PART.
        FOLDER IS CREATED IN THE GIVEN DIR FOR THEM
        
        """
        logging.info("Starting the splitting of the data into train test")
        try:
            with open(self.config) as file:
                config = yaml.safe_load(file)
                train_test_split_ratio = config['data_ingestion']['train_test_split_ratio']
            train_set, test_set = train_test_split(dataframe, test_size= train_test_split_ratio, random_state= 42)
            logging.info("Performed the train test split")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok= True)
            
            train_set.to_csv(self.data_ingestion_config.training_file_path, index = False, header = True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index =  False, header = True)

            logging.info("Exported the train and test files successfully")
            
        except Exception as e:
            raise MyException(e, sys)
        
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Basically this function is going to inttiate the data ingestion step in which all the above defined fun will
        run in a one go
        
        """
        try:
            dataframe = self.export_data_from_mongoDB()
            logging.info("Got the data from the MongoDB successfull ")
            self.split_the_train_test_data(dataframe= dataframe)
            logging.info("Splitting the data into the training and testing data")
            logging.info("Finished the process and Exiting ")
            
            data_ingestion_artifact = DataIngestionArtifact(train_file_path= self.data_ingestion_config.training_file_path, test_file_path= self.data_ingestion_config.testing_file_path)
            logging.info("DataIngestionArtifact has been created successfully ")
            return data_ingestion_artifact
        
        except Exception as e:
            raise MyException(e, sys)
        