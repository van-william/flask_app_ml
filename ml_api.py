import urllib.request
import json
import ssl
import os
#import tensorflow as tf #removed to save space in Heroku
import numpy as np
import sklearn
#tf.get_logger().setLevel('FATAL')

def predict_azure(request, url, api_key):
    # Request data goes here
    # The example below assumes JSON formatting which may be updated
    # depending on the format your endpoint expects.
    # More information can be found here:
    # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
    def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context
    #allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
    ortho_dict = dict(request.form)
    data =  {
    "Inputs": {
        "data": [
        {
            "pelvic_incidence": ortho_dict['pelvic_incidence'],
            "pelvic_tilt": ortho_dict['pelvic_tilt'],
            "lumbar_lordosis_angle": ortho_dict['lumbar_lordosis_angle'],
            "sacral_slope": ortho_dict['sacral_slope'],
            "pelvic_radius": ortho_dict['pelvic_radius'],
            "degree_spondylolisthesis": ortho_dict['degree_spondylolisthesis']
        }
        ]
    },
    "GlobalParameters": {
        "method": "predict"
    }
    }

    body = str.encode(json.dumps(data))
   
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
    return diagnosis

#NOTE: tensorflow module was commented out to reduce flask app size
#def predict_tf(request, dir='static/models/tf_model'):
    #deep_model = tf.keras.models.load_model(dir)
    #decoder = {'Normal': 0, 'Hernia':1, 'Spondylolisthesis':2 }
    #features = [float(x) for x in request.form.values()]
    #tf_feature = tf.convert_to_tensor([np.array(features)])
    #prediction = deep_model.predict(tf_feature)
    #value = np.argmax(prediction, axis=1)
    #diagnosis = list(decoder.keys())[list(decoder.values()).index(value)]
    #return diagnosis


def predict_sk(request, model, scaler):
    
    features = [float(x) for x in request.form.values()]
    inputs = np.asarray(features).reshape((1, -1))
    scaled_inputs = scaler.transform(inputs)
    prediction = model.predict(scaled_inputs)
    output = prediction[0]
    return output