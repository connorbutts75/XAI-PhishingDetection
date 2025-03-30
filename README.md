XAI-PhishingDetection-Web
This code works on Python 3.13 and Flask

This code was designed as part of my Senior Project to develop an XAI to detect phishing emails. This code funcitons by having the user input an email that they recieved into a self-hosted website and then the website would use flask to execute a python script which would use a model to analyze the message to determine if its a phishing email and if so generate a response as to why it is a phishing email. The classification model was trained using RoBERTa model with training data from https://www.kaggle.com/datasets/subhajournal/phishingemails. The model itself cannot generate a response explaining why it is a phishing email in which I used ChatGPT to explain reasons the message is potentially dangerous.

To use this project
1) Download the repository
2) Download model.safetensors which to do so you must click adding binary under announcements on the right side and then click on model.safetensors
3) Move model.safetensors into the XAI-PhishingDetection\AI folder
4) Modify line 5 of model.py to add an OpenAI API key
5) Install all necessary libraries which are in requirements.txt (or you can just run app.py because it will automatically install all the necessary libraries, it just might also set off whatever antivirius you have)
6) Launch app.py
