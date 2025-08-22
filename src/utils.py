from src.logger import logger
from src.exceptions import CustomException
from sklearn.metrics import r2_score

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
