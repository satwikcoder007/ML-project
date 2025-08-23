from src.pipeline.predict_pipeline import PredictPipeline

if __name__ == "__main__":
    data={
        'gender': 'female',
        'race_ethnicity': 'group A',
        'parental_level_of_education': 'high school',
        'lunch': 'standard',
        'test_preparation_course': 'completed',
        'reading_score': 88,
        'writing_score': 95
    }

    predict = PredictPipeline(data)
    results = predict.predict()
    print(results)