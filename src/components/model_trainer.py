import os
import sys
import pandas as pd
import numpy as np
import pathlib
from src.exceptions import CustomException
from src.logger import logger
from src.utils import model_train

from sklearn.linear_model import LinearRegression 
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor,GradientBoostingRegressor,RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
import pickle



class ModelTrainerConfig:
    def __init__(self):
        self.model_path = os.path.join('artifacts', 'model.pkl')

    def save_model(self,model):
        try:
            with open(self.model_path, "wb") as f:
                pickle.dump(model, f)
            logger.info(f"Model object saved to {self.model_path}")
        except Exception as e:
            raise CustomException("Error occurred while saving the model object", e)


class ModelTrainer:
    def __init__(self):
        self.config = ModelTrainerConfig()

    def initiate_training(self,X_train,y_train,X_test,y_test):
        models = {
            "Linear Regression": LinearRegression(),
            "Decision Tree": DecisionTreeRegressor(),
            "Random Forest": RandomForestRegressor(),
            "AdaBoost": AdaBoostRegressor(),
            "Gradient Boosting": GradientBoostingRegressor(),
            "KNN": KNeighborsRegressor()
        }

        try:
            model_report = model_train(X_train,y_train,X_test,y_test,models)
            best_model_name = max(model_report, key= lambda name: model_report[name]["score"])

            best_model = model_report[best_model_name]["model"]
            best_score = model_report[best_model_name]["score"]

            if best_score < 0.6:
                raise CustomException("No model is able to give sufficient accuracy")

            logger.info(f"Best model found: {best_model_name} with score: {best_score}")

            self.config.save_model(best_model)

        except Exception as e:
            if str(e).strip(): 
                raise CustomException(str(e).strip(),e)
            else:
                raise CustomException("Error occurred while training models", e)    