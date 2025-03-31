import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.HotelCancellationPrediction.configurations.mongodb_connection import MongoDbClient
from src.HotelCancellationPrediction.constants import DB_NAME
from Exceptions import MyException


class mongodbData:
    """
    It is a class to export MONGODB data to a pandas dataframe.
    
    
    Initializes the MongoDB client connections"""
    
    
    def __init__(self) -> None:
        try: 
            self.mongo_client = MongoDbClient(database_name=DB_NAME)
        except Exception as e:
            raise MyException(e, sys)
        
    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str]= None) ->pd.DataFrame:
        """
        Exports an entire MongoDB collection as a pandas DataFrame.

        Parameters:
        ----------
        collection_name : str
            The name of the MongoDB collection to export.
        database_name : Optional[str]
            Name of the database (optional). Defaults to DB_NAME.

        Returns:
        -------
        pd.DataFrame
            DataFrame containing the collection data, with '_id' column removed and 'na' values replaced with NaN.
        """
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]
            
            print("Fetching data from MongoDB...")
            df = pd.DataFrame(list(collection.find()))
            print(f"Data fetched with len: {len(df)}")
            if "Booking_ID" in df.columns.to_list():
                df = df.drop(columns=["Booking_ID"], axis=1)
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis= 1)
            df.replace({"na":np.nan},inplace=True)
            return df

        except Exception as e:
            raise MyException(e, sys)
        