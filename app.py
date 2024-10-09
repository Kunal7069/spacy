from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import spacy
import os

nlp = spacy.load("en_core_web_sm")

# Define action synonyms
call_synonyms = ["call", "dial", "make a phone call to", "ring", "place a call to"]
camera_synonyms = ["open the camera","camera","photo", "launch the camera", "start the camera", "activate the camera", "use the camera"]
message_synonyms=  ["send a message", "send message", "text", "inbox","message", "send a text", "respond", "answer the message", "reply to message"]
email_synonyms=["Read the latest mail","Read latest mail","Read latest email","Read latest","Read the last mail"]
reply_synonyms=['Reply the latest mail','Reply latest mail','Reply mail','Reply the mail','Reply the last mail','Reply last mail']

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

def extract_task(sentence):
    doc = nlp(sentence)
    
    action = None
    target = None
    sentence_lower = sentence.lower()

    for synonym in call_synonyms:
        if synonym in sentence_lower:
            action = "Call"
            
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    target = ent.text
                    break
            
            if not target:
                for token in doc:
                    if token.pos_ == "PROPN":
                        target = token.text
                        break
    
    for synonym in message_synonyms:
        if synonym in sentence_lower:
            action = "Message"
            
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    target = ent.text
                    break
            
            if not target:
                for token in doc:
                    if token.pos_ == "PROPN":
                        target = token.text
    for synonym in reply_synonyms:
        if synonym in sentence_lower:
            action = "Reply the Latest Mail"                

    for synonym in camera_synonyms:
        if synonym in sentence_lower:
            action = "Open the Camera"
    for synonym in email_synonyms:
        if synonym in sentence_lower:
            action = "Read the Latest Mail"
    result = []
    if action and target:
        result.append(action)
        result.append(target)
        return result
    elif action:
        result.append(action)
        return result
    else:
        result.append("NO ACTION")
        return result

@app.route('/extract-task', methods=['POST'])
def handle_request():
    # Get the JSON data from the request
    data = request.get_json()
    # Extract the sentence from the request body
    sentence = data.get("sentence")
    
    if not sentence:
        return jsonify({"error": "No sentence provided"}), 400

    result = extract_task(sentence)
    return jsonify(result)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if no PORT variable is found
    app.run(host='0.0.0.0', port=port)
