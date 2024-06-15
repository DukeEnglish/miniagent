# app.py
from flask import Flask, render_template, request, Response
from llm_service.glm import glm_client
from flask_cors import CORS
import json
import time

app = Flask(__name__)
CORS(app)  # 允许所有域名访问

# 默认设置
DEFAULT_LLM_SERVICE_URL = 'https://default-llm-service.com/api'
DEFAULT_API_KEY = 'default-api-key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    '''ChatGPT Prompt'''
    if request.method == 'POST':
        user_input = request.json.get('message', [])
        llm_service_url = request.json.get('llmservice', DEFAULT_LLM_SERVICE_URL)
        api_key = request.json.get('apikey', DEFAULT_API_KEY)

        headers = {'Authorization': f'Bearer {api_key}'}
        response = glm_client.llm_stream(user_input=user_input)

        messages = []
        for line in response:
            messages.append({"userMessage": user_input, "botMessage": line})

        return json.dumps(messages)

    def generate():
        user_input = request.args.get('message', [])
        llm_service_url = request.args.get('llmservice', DEFAULT_LLM_SERVICE_URL)
        api_key = request.args.get('apikey', DEFAULT_API_KEY)

        headers = {'Authorization': f'Bearer {api_key}'}
        response = glm_client.llm_stream(user_input=user_input)

        for line in response:
            time.sleep(0.5)
            print(f'data: {json.dumps({"userMessage": user_input, "botMessage": line})}\n\n')
            yield f'data: {json.dumps({"userMessage": user_input, "botMessage": line})}\n\n'

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
