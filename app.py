#importing the necessary libraries for deployment
from flask import Flask, jsonify, request, render_template
import urllib.request
import json
import os
import ssl
from numpy import diag
ML_APP_KEY = os.environ['ML_APP_KEY']
print(ML_APP_KEY)
print(json.dumps({**{}, **os.environ}, indent=2))
def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.


#naming our app as app
app= Flask(__name__)

#defining the different pages of html and specifying the features required to be filled in the html form

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    form_input = dict(request.form)
    # Request data goes here
    # The example below assumes JSON formatting which may be updated
    # depending on the format your endpoint expects.
    # More information can be found here:
    # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
    data =  {
    "Inputs": {
        "data": [
        {
            "pelvic_incidence": form_input['pelvic_incidence'],
            "pelvic_tilt": form_input['pelvic_tilt'],
            "lumbar_lordosis_angle": form_input['lumbar_lordosis_angle'],
            "sacral_slope": form_input['sacral_slope'],
            "pelvic_radius": form_input['pelvic_radius'],
            "degree_spondylolisthesis": form_input['degree_spondylolisthesis']
        }
        ]
    },
    "GlobalParameters": {
        "method": "predict"
    }
    }

    body = str.encode(json.dumps(data))

    url = 'http://3cbc4439-5001-4b6d-b704-adbfd1c79dd0.eastus.azurecontainer.io/score'
    api_key = ML_APP_KEY # Replace this with the API key for the web service

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        #print(result)
        result_dict = json.loads(result.decode('utf-8'))
        diagnosis = (result_dict['Results'][0])
        #print(diagnosis)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
    return render_template("index.html", prediction_text= "Diagnosis is {}".format(diagnosis))

if __name__ == "__main__":
    app.run(debug=True)
