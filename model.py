import openai
from transformers import RobertaForSequenceClassification, RobertaTokenizer
import torch

client = openai.Client(api_key="OPEN-AI-KEY")

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
        str(confidence)
    }

#This will be called by app.py
def classify_email(text):
    confidence, label = classify_text(text)
    output =''

    #Explain decision (Could not develop text AI so used ChatGPT)
    if label == 'LABEL_1':
        response = client.chat.completions.create(
        model="gpt-4o",  # Use the latest model

        #Based on R. Chataut, P. K. Gyawali and Y. Usman, "Can AI Keep You Safe? A Study of Large Language Models for Phishing Detection,"
        #DOI: 10.1109/CCWC60891.2024.10427626
        messages=[
            {"role": "system", "content": "You are a CyberGPT, an expert cybersecurity assistaint AI tasked with explaining why emails have been classified as phishing."},
            {"role": "user", "content": "Explain why this email might be phishing. Please keep it short\n" + text}
        ]
)   

        output = "Email is likely phishing.\nReasoning: " + response.choices[0].message.content  # Extracts the AI's response
    else:
        output = "Email is likely safe"
    return output
