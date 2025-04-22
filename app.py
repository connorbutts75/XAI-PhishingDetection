import subprocess

#Importing necessary libraries if they are missing (All of these will be used in model.py)
try:
    import openai
    from transformers import RobertaForSequenceClassification, RobertaTokenizer
    import torch
    import flask
except:
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True) 

from flask import Flask, render_template, request

#Loading model is being placed in a try in case some of the files are not properly loaded
modelNotPresent = False
try:
    from model import classify_email  # Import AI model function
except:
    modelNotPresent = True

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    confidence= None
    response = None

    if request.method == "POST":
        email_text = request.form["email_text"]
        if email_text != "":
            result, response, confidence = classify_email(email_text)  # Call AI model
        else:
            result = "There is no text to classify" #Will return this if user did not input any text
            response = ""
            confidence = ""
    
    if modelNotPresent == False:
        return render_template("index.html", result=result, response=response, confidence=confidence)
    else:
        return render_template("modelError.html")

if __name__ == "__main__":
    app.run(debug=True)