import os 
import sys
import pandas as pd
import numpy as np
from logger import logging
from Exceptions import MyException
from src.HotelCancellationPrediction.constants import *
from src.HotelCancellationPrediction.utils.common import read_yaml_file, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from pathlib import Path


class DataPreprocessing():
    def __init__(self, train_path:str, test_path:str, processed_data_path:str, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_data_path
        self.config = read_yaml_file(config_path)
        """
        Basically this fun is like intialization of the data preprocessing main fun 
        
        """
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir, exist_ok= True)
            
    
    def preprocess_data(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        Using this function we are going to preprocess the dataframe and 
        in return it will give the processed data 
        
        """
        try:
            logging.info("Starting the Data Preprocessing Step ------------------------------->")
            logging.info(" Dropping the unwanted columns ")
            
            df.drop(columns= ['Unnamed: 0', 'Booking_ID'], inplace= True)
            df.drop_duplicates(inplace= True)
            
            categorical_cols = self.config["data_processing"]["categorical_columns"]
            numerical_cols = self.config["data_processing"]["numerical_columns"]
            
            logging.info("Fetched the categorical and numerical columns")
            encoder = LabelEncoder()
            mappings = {}
            
            for col in categorical_cols:
                df[col] = encoder.fit_transform(df[col])
                mappings[col] = {label:code for label, code in zip(encoder.classes_, encoder.transform(encoder.classes_))}
            
            logging.info("Categorical columns are Encoded with labels")
            logging.info(" Time to handle skewness of the data")
            
            skewness_threshodl  = self.config["data_processing"]["skewness_threshold"]
            skewness  =df[numerical_cols].apply(lambda x: x.skew())
            
            for col in skewness[skewness>skewness_threshodl].index:
                df[col] = np.log1p(df[col])
                
            logging.info("Returing the dataframe after droping and sknewss step")
            return df
        
        except Exception as e:
            logging.error(f" Some error has taken place in preprocess function {e}")
            raise MyException(e, sys)
                
                
    def balance_the_data(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        This fucntion is going on tp return the data frame which will be balanced which means
        
        there will be no imbalance into it, it has been done with the help of sampling using the SMOTE
        """
        try:
            logging.info("Balancing the imbalanced data .................................")
            X = df.drop(columns= "booking_status")
            y = df['booking_status']
            
            smote = SMOTE(random_state= 42)
            X_after_resampled, y_after_Resampled = smote.fit_resample(X, y)
            
            balanced_df_after_Smote=  pd.DataFrame(X_after_resampled, columns= X.columns)
            balanced_df_after_Smote['booking_status'] = y_after_Resampled
            
            logging.info("Data has been balanced successfully ")

            return balanced_df_after_Smote
        
        except Exception as e:
            logging.error("Some error has been taken place into the balance the data fun ")
            raise MyException(e, sys)
        
    def feature_Selection(self, df:pd.DataFrame):
        """
        In this step we are going to select the feature which is the one of the most importatn step in the Machine Learning
        
        """    
        try:
            logging.info(" Starting of the step - feature selections")
            
            X = df.drop(columns= 'booking_status')
            y = df['booking_status']
            
            model = RandomForestClassifier(random_state= 42)
            model.fit(X, y)
            
            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                'feature': X.columns,
                'importance': feature_importance
            })
            
            top_features_from_df = feature_importance_df.sort_values(by= 'importance', ascending= False)
            num_of_features_to_select = self.config['data_processing']['no_of_features']
            top_n_selected_features = top_features_from_df['feature'].head(num_of_features_to_select).values
            
            logging.info(f" The top features are :{ top_n_selected_features}")
            
            top_n_features_selected_df = df[top_n_selected_features.tolist() + ['booking_status']]
            
            logging.info(" Features Selection has been done successfully")
            return top_n_features_selected_df
        
        except Exception as e:
            logging.error(" Some error has taken place in the features selection step")
            
            
    def save_data(self, df:pd.DataFrame, file_path:str) -> None:
        """
        We are making out this fun to save the data in the form of csv at the given file path
        
        """
        try:
            df.to_csv(file_path, index= False)
            logging.info(f" Saved the file at the given place successfully{file_path}")
            
        except Exception as e:
            logging.info(" Some error has taken place while saving the file")
            raise MyException(e, sys)

    def final_process_step(self):
        """
        This is final function in which we have used all the earlier fun which have made 
        
        """            
        try:
            logging.info(" Starting the Data Preprocssing step now--------------------------------------->>")
            logging.info(f"Loading the data from {RAW_DIR}")
            
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)
            
            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)
            
            train_df = self.balance_the_data(train_df)
            test_df = self.balance_the_data(test_df)
            
            train_df = self.feature_Selection(train_df)
            test_df = test_df[train_df.columns]
            
            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)
            
            logging.info("Data preprocessing successful")
            
        except Exception as e:
            logging.error(" Error has taken place in the final process step")
            
        finally:
            
            logging.info(" Data Preprocessing Completed")
            
            
if __name__ =="__main__":
    processor = DataPreprocessing(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.final_process_step()