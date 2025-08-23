import os
import sys
import pandas as pd 
import numpy as np
import pickle
from src.exceptions import CustomException
from src.logger import logger


class PredictPipeline():
    def __init__(self,data):
        self.custom_data = CustomData(data)
        self.df = self.custom_data.get_data_as_dataframe()
        self.model_path = os.path.join("artifacts","model.pkl")
        self.preprocessor_path = os.path.join("artifacts","preprocessor.pkl")

    def predict(self):
        try:
            with open(self.model_path,'rb') as f:
                model = pickle.load(f)
            logger.info("Model loaded successfully")

            with open(self.preprocessor_path,'rb') as f:
                preprocessor = pickle.load(f)
            logger.info("Preprocessor loaded successfully")
            df_transformed = preprocessor.transform(self.df)
            prediction = model.predict(df_transformed)
            logger.info("Prediction made successfully")
            
            return prediction   
            
        except Exception as e:
            raise CustomException("Error during prediction", e)

class CustomData:
    def __init__(self,fetched_data):
        self.data = fetched_data

    def get_data_as_dataframe(self):
        try:
           df = pd.DataFrame([self.data])
           logger.info("Dataframe created successfully")
           return df
        except Exception as e:
            raise CustomException("Error converting data to DataFrame",e)