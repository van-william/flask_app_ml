#importing the necessary libraries for deployment
from flask import Flask, request, jsonify, render_template
import random

#naming our app as app
app= Flask(__name__)

#defining the different pages of html and specifying the features required to be filled in the html form

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    return render_template("index.html", prediction_text= "flower is {}".format(random.randint(0,20)))


if __name__ == "__main__":
    app.run(debug=True)
