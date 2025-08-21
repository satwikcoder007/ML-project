import os
import sys
import pandas as pd
import numpy as np
import  pathlib

from src.exceptions import CustomException
from src.logger import logger
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.compose import ColumnTransformer   
from sklearn.pipeline import Pipeline   
import pickle

class DataTransformationConfig:

    def __init__(self):  ## we store the instance of the tranformation object at this binary file
        self.preprocessor_obj_file_path = pathlib.Path("artifacts/preprocessor.pkl")
    
    def save_transform_object(self, transform_object):  ## In this function we save the  object as a file
        try:
            with open(self.preprocessor_obj_file_path, "wb") as f:
                pickle.dump(transform_object, f)
            logger.info(f"Transformation object saved to {self.preprocessor_obj_file_path}")
        except Exception as e:
            raise CustomException("Error occurred while saving the transformation object", e)

class DataTransformation:

    def __init__(self):
        self.config = DataTransformationConfig()

    def get_data_transformation_object(self):  ## This function returns the data transformation object that is the column transformer

        try:
            numeric_features = ['reading_score', 'writing_score']
            categorical_features = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            coloumn_transform = ColumnTransformer(
                transformers=[
                    ("num", StandardScaler(), numeric_features),
                    ("cat", OneHotEncoder(handle_unknown='ignore'), categorical_features)
                ]
            )
            logger.info(f"Column transformers are created for both categorical and numerical data")

            return coloumn_transform
        
        except Exception as e:
            raise CustomException("Error occured while creating column transformers",e)

    def initiate_data_transformation(self, train_data_path, test_data_path):

        """
            This function initiates the data transformation process.
            import data form artifacts and then transfrom them
        """

        try:
            
            train_data = pd.read_csv(train_data_path)
            logger.info(f"Train data is read from {train_data_path}")
            test_data = pd.read_csv(test_data_path)
            logger.info(f"Test data is read from {test_data_path}")

            transform_object = self.get_data_transformation_object()
            logger.info(f"Data transformation object is created")

            target_field = "math_score"
            X_train = train_data.drop(columns=[target_field],axis=1)
            y_train = train_data[target_field]
            X_test = test_data.drop(columns=[target_field],axis=1)
            y_test = test_data[target_field]

            transform_object.fit(X_train)
            X_train = transform_object.transform(X_train)
            X_test = transform_object.transform(X_test)
            logger.info(f"Data transformation is applied on train and test data")


            self.config.save_transform_object(transform_object)

            return X_train, y_train, X_test, y_test

        except Exception as e:
            raise CustomException("Error occured while initiating data transformation",e)
