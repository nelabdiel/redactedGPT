from flask import Flask, request, abort, redirect, render_template
#from bokeh.util.string import encode_utf8
import os #Comment out if no '_if_ =_main_ at the bottom
import math
import re
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get('OPENAI_KEY')
completion = openai.ChatCompletion()


def askgpt(question, chat_log=None):
    if chat_log is None:
        chat_log = [{
            'role': 'system',
            'content': 'You are a helpful, upbeat and funny assistant.',
        }]
    chat_log.append({'role': 'user', 'content': question})
    response = completion.create(model='gpt-3.5-turbo', messages=chat_log)
    answer = response.choices[0]['message']['content']
    chat_log.append({'role': 'assistant', 'content': answer})
    return answer, chat_log



def remove_pii(text):
    # Define regex pattern for different types of PII
    ssn_pattern = r'\b(?:\d{3}-\d{2}-\d{4}|\d{9})\b'
    dob_pattern = r'\b(?:\d{2}\/\d{2}\/\d{4})\b'
    nin_pattern = r'\b(?:\d{9})\b'
    ccn_pattern = r'\b(?:\d{4}-\d{4}-\d{4}-\d{4})\b'
    vin_pattern = r'\b(?:[A-Z]\d{3}[A-Z]{2})\b'
    phone_pattern = r'\b(?:\d{3}[-.\s]?\d{3}[-.\s]?\d{4})\b'

    # Replace PII patterns with placeholders
    text = re.sub(ssn_pattern, '[SSN]', text)
    text = re.sub(dob_pattern, '[DOB]', text)
    text = re.sub(nin_pattern, '[NIN]', text)
    text = re.sub(ccn_pattern, '[CCN]', text)
    text = re.sub(vin_pattern, '[VIN]', text)
    text = re.sub(phone_pattern, '[PHONE]', text)

    return text

# Example usage
#input_text = "John Doe's SSN is 123-45-6789 and his phone number is 555-123-4567."
#processed_text = remove_pii(input_text)
#print(processed_text)









# Create the application instance
APP = Flask(__name__)


# Create a URL route in our application for "/"
#Index page
@APP.route('/')
def main():
    return redirect('/index')


@APP.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        text = ''
        chatgpt = "Hi there, I will try my best to remove PII, PHI and IP but remember it's always better to not even include it in the first place."
        #html = render_template('index.html')
        #return html

    else:
        if request.form:
            #remove PII
            text = remove_pii(request.form['input_text'])
            # Get Answer
            chatgpt= askgpt(text)[0]
            #"Answer will appear here"
            
            text = '~You~: ' + text
            
            
            
        
    html = render_template('index.html', inputScrubbed=text, chatGPTAnswer=chatgpt)
    return html
    #else:
        #return abort(404)






#Comment out everything below for CloudFoundry deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5002))
    APP.run(host='0.0.0.0', port=port)