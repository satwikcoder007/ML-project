from src.logger import logger
from src.exceptions import CustomException
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def model_train(X_train,y_train,X_test,y_test,models):
    model_report={}
    
    for model_name,model in models.items():

        model.fit(X_train,y_train)
        logger.info(f"{model_name} model trained successfully.")

        y_pred = model.predict(X_test)
        score = r2_score(y_true=y_test,y_pred=y_pred)

        model_report[model_name] = {
            "model":model,
            "score":score
        }

        logger.info(f"model report for {model_name} is created successfully.")
        
    return model_report

def model_train_with_params(X_train,y_train,X_test,y_test,models,param_grids):

    model_report={}
    for model_name,model in models.items():

        grid = GridSearchCV(estimator=model,param_grid=param_grids[model_name],cv=5, n_jobs=-1, verbose=0)
        grid.fit(X_train,y_train)
        logger.info(f"{model_name} model trained successfully with hyperparameter tuning.")

        y_pred = grid.predict(X_test)
        score = r2_score(y_true=y_test,y_pred=y_pred)

        model_report[model_name] = {
            "model":grid.best_estimator_,
            "score":score
        }

    return model_report