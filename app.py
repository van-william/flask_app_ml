#importing the necessary libraries for deployment
from flask import Flask, jsonify, request, render_template
import os
import pickle
from ml_api import predict_ml, predict_tf


ML_APP_KEY = os.getenv('ML_APP_KEY')
TEST_ENV = os.getenv('WEBSITE_SITE_NAME')
ml_url = 'http://3cbc4439-5001-4b6d-b704-adbfd1c79dd0.eastus.azurecontainer.io/score'



#naming our app as app
app= Flask(__name__)

#defining the different pages of html and specifying the features required to be filled in the html form

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/jupyter")
def jupyter():
    return render_template("jupyter.html")

@app.route("/deep_learning")
def deep_learning_overview():
    return render_template("deep-learning.html")

@app.route("/data_context")
def data_context():
    return render_template("data_overview.html")


@app.route("/predict", methods=["POST"])
def predict():
    form_input = dict(request.form)
    diagnosis = predict_ml(ortho_dict = form_input, url = ml_url, api_key =  ML_APP_KEY)
    return render_template("index.html", prediction_text= "Diagnosis is {}".format(diagnosis))

@app.route('/predict_deep')
def deep_learning_pred():
    return render_template("deep-learning-pred.html")

@app.route('/predict_deep_output',methods=['POST'])
def deep_learning_pred_output():
    diagnosis = predict_tf(request)
    return render_template("deep-learning-pred.html", prediction_text= "Diagnosis is {}".format(diagnosis))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)
