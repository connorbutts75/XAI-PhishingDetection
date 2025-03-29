import subprocess
#Importing necessary libraries if they are missing (All of these will be used in model.py)
try:
    import openai
    from transformers import RobertaForSequenceClassification, RobertaTokenizer
    import torch
except:
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True) 

from flask import Flask, render_template, request
from model import classify_email  # Import AI model function

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        email_text = request.form["email_text"]
        result = classify_email(email_text)  # Call AI model

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
