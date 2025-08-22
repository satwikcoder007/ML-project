from flask import Flask,request,jsonify,render_template
from src.pipeline.predict_pipeline import CustomData,PredictPipeline
from src.logger import logger
from src.exceptions import CustomException

app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
   return render_template("index.html")

@app.route('/home',methods=["GET"])
def home():
   return render_template("home.html")

@app.route('/predict',methods=["POST"])
def predict_input_data(): 
    try:
        data={
            'gender': request.form.get('gender'),
            'race_ethnicity': request.form.get('ethnicity'),
            'parental_level_of_education': request.form.get('parental_level_of_education'),
            'lunch': request.form.get('lunch'),
            'test_preparation_course': request.form.get('test_preparation_course'),
            'reading_score': float(request.form.get('reading_score')),
            'writing_score': float(request.form.get('writing_score'))
        }

        custom_data = CustomData(data)
        data_df = custom_data.get_data_as_dataframe()
        predict = PredictPipeline(data_df)
        results = predict.predict()
        result = results[0]
        return render_template("home.html", prediction=result)

    except CustomException as e:
        e.log()
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True,port=8000,host="::")
