import os
import sys

import pandas as pd
import numpy as np

from src.logger import logger
from src.exceptions import CustomException   

from src.components.data_transformation import DataTransformation
from pathlib import Path

from sklearn.model_selection import train_test_split

class DataIngestionConfig:  ## This will declare where to store different data

    def __init__(self):
        self.raw_data_path = os.path.join('artifacts', 'data.csv')  
        self.train_data_path = os.path.join('artifacts', 'train.csv')
        self.test_data_path = os.path.join('artifacts', 'test.csv')
        self.data_path = Path(__file__).resolve().parent.parent.parent / 'notebooks/data/stud.csv'

class DataIngestion:
    def __init__(self):

        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):

       logger.info("Entered the Data Ingestion method")
       try:
            df = pd.read_csv(self.ingestion_config.data_path)
            logger.info("Read the data from source in form of a DataFrame")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logger.info("Saved the data in the artifacts folder")

            train_set,test_set = train_test_split(df, test_size=0.2, random_state=42)

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            logger.info("Saved the Training data in the artifacts folder") 

            os.makedirs(os.path.dirname(self.ingestion_config.test_data_path), exist_ok=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logger.info("Saved the Testing data in the artifacts folder")
            logger.info("Data Ingestion is completed successfully")

            return self.ingestion_config

       except Exception as e:  ## used the super class so that it can catch any type of exception
            raise CustomException("Error occurred during data ingestion", e)    
       

if __name__ == "__main__":  ## this __name__ == "__main__" means that this part of the code will be executed only if this script is run directly
                            ## this is like main function

    data_ingestion = DataIngestion()
    data_transformation = DataTransformation()

    try:
        config = data_ingestion.initiate_data_ingestion()
        data_transformation.initiate_data_transformation(config.train_data_path, config.test_data_path)
        
    except CustomException as e:
        e.log()