import sys
from Exceptions import MyException
from logger import logging
from src.HotelCancellationPrediction.constants import *

# from src.HotelCancellationPrediction.components.data_ingestion import DataIngestion
# from src.HotelCancellationPrediction.components.data_Processing import DataPreprocessing
from src.HotelCancellationPrediction.components.model_building import ModelTrainerClass
# from src.HotelCancellationPrediction.entity.config import DataIngestionConfig
# from src.HotelCancellationPrediction.entity.artifact import DataIngestionArtifact


class TrainingPipeline:
    def __init__(self):
        # self.data_ingestion_config = DataIngestionConfig()
        pass
        
        
        
    # def start_data_ingestion_step(self) -> DataIngestionArtifact:
    #     """
    #     This method of training pipeline is for starting the data ingestion step 
    #     from the component part
        
    #     """
    #     try:
    #         logging.info(" Entered the training pipeline of data ingestion part ")
    #         logging.info("Going to get the data from the mongo db")
            
    #         data_ingestion  = DataIngestion(data_ingestion_config= self.data_ingestion_config)
    #         data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    #         logging.info("Got the train and test split on the MONGODB dataset")
    #         logging.info(" Now comming back from the data ingestion method")
        
    #     except Exception as e:
    #         raise MyException(e, sys)
        
    # def start_data_preprocessing_step(self):
    #     try:
    #         logging.info(" Entered the training pipeline of the data preprocessing ")
    #         data_preprocess = DataPreprocessing(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    #         data_preprocess.final_process_step()
            
    #         logging.info("Done with the steps involved into the data processing ")
            
    #     except Exception as e:
    #         raise MyException(e, "error has taken place in the start data preprocess step")
        
        
    def start_model_building_and_evaluation_part(self):
        try:
            logging.info("Enterted the model building and evaluation part")
            model_build_eval  = ModelTrainerClass(TRAIN_FILE_PATH, TEST_FILE_PATH, MODEL_OUTPUT_PATH)
            model_build_eval.run()
            
            logging.info("Done with the mdoel building and eval part succcessfully")
            
        except Exception as e:
            logging.error("Some error has taken place in the model building part")
            raise MyException(e, sys)
        
        
    def run_pipeline(self) -> None:
        """
        This method is basically responsible for the running of the pipeine
        
        """
        try:
            # data_ingestion_artifact = self.start_data_ingestion_step()
            # data_preprocess_step = self.start_data_preprocessing_step()
            model_building_eval_step = self.start_model_building_and_evaluation_part()
        except Exception as e:
            raise MyException(e, sys)
        