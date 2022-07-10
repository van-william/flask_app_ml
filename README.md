# Machine Learning Web App Using Flask
This web app provides a simple summary of using a variety of machine learning models (Sklearn, Tensorflow, and Azure Machine Learning) deployed to a python web app (Flask)
- Web App Link: https://python-ml-web-app-orthopedics.herokuapp.com/


## How to Use
- Clone this repository with: git clone https://github.com/van-william/flask_app_ml.git
- Reference the sample notebooks in the notebooks directory
- Leverage the simple web framework (html + css) for your own web app projects

## Web App Hosting
- This project is hosted on Heroku: https://python-ml-web-app-orthopedics.herokuapp.com/
- The repository contains context on the necessary Profile, runtime.txt, and other required files for Heroku hosting

## Model Deployment
- Originally, Microsoft Azure Machine Learning was used for model deployment (Jupyter Notebook and Azure Machine Learning API code are still in the repository), but the primary predictor was simplified to be a localized .pkl file from scitkit-learn
- There is a notebook for Deep Learning (Tensorflow), but the library was too big for the free version of Heroku.  However, the machine learning code is still referenced

## References
- I leveraged this detailed [Flask tutorial](https://www.youtube.com/playlist?list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz) for help in building the web page
- There are several examples for deployed machine learning models
    - https://www.geeksforgeeks.org/deploy-machine-learning-model-using-flask/
    - https://towardsdatascience.com/deploy-a-machine-learning-model-using-flask-da580f84e60c
- Francois Chollet has a [good repository](https://github.com/fchollet/deep-learning-with-python-notebooks) of deep learning examples for reference as well
- Data Source Citation: Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.






