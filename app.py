import os

import requests
from flask import Flask, Response, render_template, request
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

API_URL = 'http://34.64.111.198:8000/chatbot_streams'

@app.route('/')
def index():
    return render_template('ai.html')


def stream_response(image_path, langchain_prompt):
    # Prepare data for the API request
    files = {'langchain_image': open(image_path, 'rb')} if image_path else {}
    data = {'langchain_prompt': langchain_prompt}
    
    with requests.post(API_URL, files=files, data=data, stream=True) as r:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                yield chunk.decode('utf-8')

@app.route('/submit', methods=['POST'])
def submit():
    if 'langchain_image' in request.files:
        langchain_image = request.files['langchain_image']
        image_filename = secure_filename(langchain_image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        langchain_image.save(image_path)
    else:
        image_path = None

    langchain_prompt = request.form.get('langchain_prompt', '')

    return Response(stream_response(image_path, langchain_prompt), content_type='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
