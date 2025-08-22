import os
import sys
import pandas as pd
import numpy as np
import pathlib
from src.exceptions import CustomException
from src.logger import logger
from src.utils import model_train,model_train_with_params

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

        param_grids = {
            "Linear Regression": {},
            "Decision Tree": {
                "max_depth": [3, 5, 7, None],
                "min_samples_split": [2, 5, 10]
            },
            "Random Forest": {
                "n_estimators": [50, 100],
                "max_depth": [None, 10, 20]
            },
            "AdaBoost": {
                "n_estimators": [50, 100],
                "learning_rate": [0.01, 0.1, 1.0]
            },
            "Gradient Boosting": {
                "n_estimators": [50, 100],
                "learning_rate": [0.01, 0.1, 0.2]
            },
            "KNN": {
                "n_neighbors": [3, 5, 7],
                "weights": ["uniform", "distance"]
            }
        }

        try:
            model_report = model_train_with_params(X_train,y_train,X_test,y_test,models, param_grids)
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