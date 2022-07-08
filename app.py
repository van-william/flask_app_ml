#importing the necessary libraries for deployment
from flask import Flask, request, render_template
import os
from ml_api import predict_azure, predict_sk
import joblib

ML_APP_KEY = os.getenv('ML_APP_KEY')
TEST_ENV = os.getenv('WEBSITE_SITE_NAME')
ml_url = 'http://3cbc4439-5001-4b6d-b704-adbfd1c79dd0.eastus.azurecontainer.io/score'
sk_model_dir='static/models/sk_model/model.pkl'
sk_scaler_dir='static/models/sk_model/scaler.pkl'

clf = joblib.load(sk_model_dir)
scaler = joblib.load(sk_scaler_dir)

#naming our app as app
app= Flask(__name__)

#defining the different pages of html and specifying the features required to be filled in the html form

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/azure_pipeline")
def azure_pipeline():
    return render_template("azure-pipeline.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/model_overview")
def machine_learning():
    return render_template("machine-learning.html")

@app.route("/deep_learning")
def deep_learning_overview():
    return render_template("deep-learning.html")

@app.route("/exploratory_data_analysis")
def eda():
    return render_template("EDA.html")


@app.route("/predict", methods=["POST"])
def predict():
    diagnosis = predict_sk(request, model = clf, scaler = scaler)
    #diagnosis = predict_azure(request, url = ml_url, api_key =  ML_APP_KEY)
    #Originally, an Azure Machine Learning Environment was used to serve the model
    return render_template("index.html", prediction_text= "Diagnosis is {}".format(diagnosis))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)
