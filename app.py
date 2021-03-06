# -*- coding: utf-8 -*-
"""
Created on Wed Feb 3 11:28:20 2021

@author: Shaon Sikder
"""

from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
#import tensorflow_hub as hub

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = flask.Flask(__name__, template_folder='templates')

# Model saved with Keras model.save()
MODEL_PATH ='fish_disease_detection.h5'

# Load your trained model
model = load_model(MODEL_PATH,custom_objects={'KerasLayer': hub.KerasLayer})
#model._make_predict_function() 


print('Model loaded. Check http://127.0.0.1:5000/')
def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   

   

    preds = model.predict(x)
    p=preds
    preds=np.argmax(preds, axis=1)
    if preds==0:
        preds="Argulus disease detected! Confidence:{}",np.argmax(p)
    elif preds==1:
        preds="Epizootic Ulcerative disease detected! Confidence:{}",np.argmax(p)
    elif preds==2:
        preds="Tail & Fin Rot disease detected! Confidence:{}",np.argmax(p)
    
    
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return flask.render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if flask.request.method == 'POST':
        # Get the file from post request
        f = flask.request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)
