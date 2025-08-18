from src.exceptions import CustomException

def data_ingestion():

    try:
        x = 1/0
    except Exception as e:
        raise CustomException("Error occurred in data ingestion", e)


try:
    data_ingestion()
except CustomException as e:
    print(e)
    e.log()