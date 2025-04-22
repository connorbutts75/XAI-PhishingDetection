import openai
from transformers import RobertaForSequenceClassification, RobertaTokenizer
import torch

client = openai.Client(api_key="OpenAI-API-Key")

#Loading in model
model_path = "./AI" 
model = RobertaForSequenceClassification.from_pretrained(model_path)
tokenizer = RobertaTokenizer.from_pretrained(model_path)

#This is the actual ai
def classify_text(text):
    # Tokenize
    inputs = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=512,
        return_tensors="pt",
    )
    
    # Predict
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1).cpu().numpy()[0]
    
    # Get label and confidence
    predicted_class = torch.argmax(logits).item()
    predicted_label = model.config.id2label[predicted_class]
    confidence = probabilities[predicted_class]
    
    return {
        predicted_label,
        float(confidence)
    }

#This will be called by app.py
def classify_email(text):
    confidence, label = classify_text(text)
    output =''
    response = ''

    print(confidence)   #Have to print confidence or else I wont be able to modify it for display for some reason
    #Modifying confidence for display
    confidence = str(int(confidence*100)) + '%'

    #Explain decision (Could not develop text AI so used ChatGPT)
    if label == 'LABEL_1':
        #Try statement being used to ensure that allow for catch errors with OpenAI
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Changed to use a more budget friendly model and found no signifigant performance difference

                #Based on R. Chataut, P. K. Gyawali and Y. Usman, "Can AI Keep You Safe? A Study of Large Language Models for Phishing Detection,"
                #DOI: 10.1109/CCWC60891.2024.10427626
                messages=[
                    {"role": "system", "content": "You are a CyberGPT, an expert cybersecurity assistaint AI tasked with explaining why emails have been classified as phishing."},
                    {"role": "user", "content": "Explain why this email might be phishing. Please keep it short and as a paragraph and not as a list\n" + text}
                ]
            ) 
            response = response.choices[0].message.content
        except:
            response = "Error using OpenAI, please make sure a valid API key is being used, to find out how please check the README"


#response.choices[0].message.content  # This is the AIs response
        output = "Phishing"
    else:
        output = "Safe"
    return output, response, confidence