import os
import pymongo
import sys
import certifi
from Exceptions import MyException
from logger import logging
from src.HotelCancellationPrediction.constants import DB_NAME, CONNECTION_URL


ca = certifi.where()
class MongoDbClient:
    """
    MongoDbClient is responsible for establishing a connection to the MongoDB database.

    Attributes:
    ----------
    client : MongoClient
        A shared MongoClient instance for the class.
    database : Database
        The specific database instance that MongoDbClient connects to.

    Methods:
    -------
    __init__(database_name: str) -> None
        Initializes the MongoDB connection using the given database name.
    """
    client = None
    
    def __init__(self, database_name:str = DB_NAME) ->str:
        """
        Initializes a connection to the MongoDB database. If no existing connection is found, it establishes a new one.

        Parameters:
        ----------
        database_name : str, optional
            Name of the MongoDB database to connect to. Default is set by DB_NAME constant.

        Raises:
        ------
        MyException
            If there is an issue connecting to MongoDB or if the environment variable for the MongoDB URL is not set.
        """
        
        try:
            if MongoDbClient.client is None:
                mongo_db_url = CONNECTION_URL
                if mongo_db_url is None:
                    raise MyException(f"Environment variable '{CONNECTION_URL}' is not set.")
                
                MongoDbClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
                
            self.client = MongoDbClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info(f"Connected to MongoDB database: {database_name}")
            
        except Exception as e:
            raise MyException(e, sys)