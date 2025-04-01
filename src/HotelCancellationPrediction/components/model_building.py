import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from Exceptions import MyException
from logger import logging
from src.HotelCancellationPrediction.constants import *
from src.HotelCancellationPrediction.utils.common import read_yaml_file, load_data
from Configs.params import *
from scipy.stats import randint
import mlflow
import mlflow.sklearn
import sys

class ModelTrainerClass():
    """
    THIS CLASS IS GOING TO BE THE BASE CLASS FOR THE MODEL TRAINER PART 
    IN THIS CLASS WE WILL BE DEFINING SEVRRAL THING RELEATED TO MODEL TRAINING
    
    """
    def __init__(self, train_path, test_path, model_trained_output_path):
        self.training_data_path = train_path
        self.testing_data_path = test_path
        self.model_outputs_path = model_trained_output_path
        
        self.params_distritbutions = LIGHTGBM_PARAMS
        self.random_search_cv_params = RANDOM_SEARCH_PARAMS
        
    
    def load_and_split_data(self):
        """
        In this part we are going to load the train and test data from the artifacts processed dir
        then we are going to split each dataset into training and testing
        
        """
        try:
            logging.info(f"Loading the train data from the {self.training_data_path}")
            train_df = load_data(self.training_data_path)
            
            logging.info(f"Loading the test data from {self.testing_data_path}")
            test_df = load_data(self.testing_data_path)
            
            logging.info("Now we are going to split the data_---------------------------------------------->")
            X_train = train_df.drop(columns= ['booking status'])
            y_train  = train_df[['booking status']]
            
            
            X_test = test_df.drop(columns=['booking status'])
            y_test = test_df[['booking status']]
            
            logging.info("Data has been splitted out successfully in the load and split functions")
            
            return X_train, X_test, y_train, y_test
        
        except Exception as e:
            logging.error("Error has taken place in the load and split function at model building.py file")
            raise MyException(e, sys)
        
        
    def train_lgbm_model(self, X_train, y_train):
        """
        We are going to train our model using the light gradient boosting machine algo
        And also we are going to use the random search Cv for the params hypertunning
        
        """
        try:
            logging.info(" Initializing the model building part - LGBM MODEL ")
            lgbm_model_params = {
                "random_state": self.random_search_cv_params['random_state'],
                "num_threads":1,
                "force_col_wise": True
            }
        
            lgbm = lgb.LGBMClassifier(**lgbm_model_params)
            
            logging.info("Started the hyperparamter tunning using the randome search CV")
            random_search = RandomizedSearchCV(
                estimator= lgbm,
                param_distributions= self.params_distritbutions,
                n_iter= self.random_search_cv_params['n_iter'],
                cv= self.random_search_cv_params['cv'],
                n_jobs=self.random_search_cv_params['n_jobs'],
                verbose= self.random_search_cv_params['verbose'],
                random_state= self.random_search_cv_params['random_state'],
                scoring=self.random_search_cv_params['scoring']
            )
            
            logging.info("Starting the hyperparamter tunnig-------------------------------------.")
            random_search.fit(X_train, y_train)
            
            logging.info("Fine Tunning has been done ----------------------.")
            best_paramter = random_search.best_params_
            best_lgm_model_formed  = random_search.best_estimator_
            
            logging.info(f"Best Parameters are the {best_paramter}")
            return best_lgm_model_formed
    
        except Exception as e:
            logging.error("Error has taken place in the model building part")
            raise MyException(e, sys)
        
        
    def evaluating_model(self, model, X_test, y_test):
        """
        This is the model evaluation part , here we basically evaluate the model , how it is working on the test data
        Looking into the diffrent matrices
        
        """
        try:
            logging.info("Evaluating the model using the diffrent metrices")
            y_preds = model.predict(X_test)
            
            
            accuracy = accuracy_score(y_test, y_pred= y_preds)
            precision = precision_score(y_test, y_preds)
            recall = recall_score(y_test, y_preds)
            f1 = f1_score(y_test, y_preds)
            
            logging.info(f"The metrices we get are {accuracy}, {precision}, {recall}, {f1}")
            
            return {
                "accuracy_score is :": accuracy,
                "precision score is": precision,
                "recall score is ": recall,
                "f1 score is ": f1
            }
            
        except Exception as e:
            logging.error(" Error has taken place in the calculating the mdoel evaluation part")
            raise MyException(e, sys)
        
        
        
    def saving_the_model(self, model):
        """
        This function is used to save the model basically in the pkl from at the specified file path
        
        """
        try:
            os.makedirs(os.path.dirname(self.model_outputs_path), exist_ok= True)
            logging.info("Saving the model")
            joblib.dump(model, self.model_outputs_path)
            logging.info(f"Model has been saved to {self.model_outputs_path}")
            
        except Exception as e:
            logging.error(f"Error has taken place while saving the model {e}")
            raise MyException(e,sys)
        
    
    def run(self):
        """
        Basically we are going to run this on the mlflow ui so that we can analysis it in a more better way 
        
        """
        try:
            X_train, X_test, y_train, y_test = self.load_and_split_data()
            best_lgbm_model = self.train_lgbm_model(X_train, y_train)
            metrices = self.evaluating_model(best_lgbm_model, X_test, y_test)
            self.saving_the_model(best_lgbm_model)
            
            logging.info("Everyting has been executed till not and the model has been saved to specified loc")
            logging.info("Model_training succcessful ")
            
        except Exception as e:
            logging.error("Error has taken place into the while runnig the model building part")
            raise MyException(e, sys)
        
        
        finally:
            logging.info("Model training has been done")
            
    
if __name__ == "__main__":
    trainer  = ModelTrainerClass(train_path= PROCESSED_TRAIN_DATA_PATH,
                                 test_path= PROCESSED_TEST_DATA_PATH,
                                 model_trained_output_path= MODEL_OUTPUT_PATH)
    
    
    
    trainer.run()