from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import spacy
import os
# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Define action synonyms
calendar_synonyms = ["calendar", "date", "open the calendar", "open calendar","calendar app", "open the calendar app", "open calendar app"]
settings_synonyms = ["settings", "setting", "open the settings", "open settings", "open the setting", "open setting",
                    "settings app", "setting app", "open the settings app", "open settings app", "open the setting app", "open setting app"]
youtube_synonyms = ["you tube","youtube", "open the youtube", "open youtube", "youtube app", "open the youtube app"]
playstore_synonyms = ["play store","playstore", "open the playstore", "open playstore", "playstore app", "open the playstore app"]
call_synonyms = ["call", "dial", "make a phone call to", "ring", "place a call to","contacts","contact"]
camera_synonyms = ["open the camera","camera","photo", "launch the camera", "start the camera", "activate the camera", "use the camera"]
message_synonyms=  ["send a message", "send message", "text", "inbox","message","messaging","send a text", "respond", "answer the message", "reply to message"]
email_synonyms=["read the latest mail","read latest mail","read latest email","read latest","read the last mail","read"]
reply_synonyms=['reply','reply to latest mail','reply to latest mail','reply the latest mail','reply latest mail','reply mail','reply the mail','reply the last mail','reply last mail']
subject_mail_synonyms=['subject','read subject']
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
                    

    for synonym in camera_synonyms:
        if synonym in sentence_lower:
            action = "Open the Camera"

    for synonym in calendar_synonyms:
        if synonym in sentence_lower:
            action = "Open the Calendar"

    for synonym in settings_synonyms:
        if synonym in sentence_lower:
            action = "Open the Settings"

    for synonym in youtube_synonyms:
        if synonym in sentence_lower:
            action = "Open the Youtube"
    
    for synonym in playstore_synonyms:
        if synonym in sentence_lower:
            action = "Open the PlayStore"
          
    for synonym in email_synonyms:
        if synonym in sentence_lower:
            action = "Read the Latest Mail"
            
    for synonym in reply_synonyms:
        if synonym in sentence_lower:
            action = "Reply the Latest Mail"

    for synonym in subject_mail_synonyms:
        if synonym in sentence_lower:
            action = "Read the Mail with Given Subject"
    
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
