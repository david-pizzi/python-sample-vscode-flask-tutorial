from . import rockpaperscissor
from . import app
from flask import Flask, render_template, request
from datetime import datetime
import requests
import os
import uuid
import json
from dotenv import load_dotenv
load_dotenv()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/translator/", methods=['GET'])
def translator():
    return render_template("translator.html")


@app.route('/translator/', methods=['POST'])
def translator_post():
    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    # Load the values from .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # Indicate that we want to translate and the API version (3.0) and the target language
    path = '/translate?api-version=3.0'
    # Add the target language parameter
    target_language_parameter = '&to=' + target_language
    # Create the full URL
    constructed_url = endpoint + path + target_language_parameter

    # Set up the header information, which includes our subscription key
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Create the body of the request with the text to be translated
    body = [{'text': original_text}]

    # Make the call using post
    translator_request = requests.post(
        constructed_url, headers=headers, json=body)
    # Retrieve the JSON response
    translator_response = translator_request.json()
    # Retrieve the translation
    translated_text = translator_response[0]['translations'][0]['text']

    # Call render template, passing the translated text,
    # original text, and target language to the template
    return render_template(
        'translator_results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )


@app.route("/rockpaperscissor/", methods=['Get'])
def rockpaperscissor():
    return render_template("rockpaperscissor.html")


@app.route("/rockpaperscissor/", methods=['POST'])
def rockpaperscissor_submit():
    return "submitted"


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name=None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
