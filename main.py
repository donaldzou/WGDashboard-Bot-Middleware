from pyexpat.errors import messages

from flask_cors import CORS
from flask import Flask, Response, request, jsonify
import os
from dotenv import load_dotenv
import requests
import json
from openai import OpenAI

load_dotenv()
AGENT_ENDPOINT = os.getenv('AGENT_ENDPOINT')
AGENT_ACCESS_KEY = os.getenv('AGENT_ACCESS_KEY')
app = Flask('WGDashboard Bot Middleware')
cors = CORS(app, resources={f"/api/*": {
    "origins": "*",
    "methods": "DELETE, POST, GET, OPTIONS",
    "allow_headers": ["Content-Type"]
}})

def GenerateResponse(status=True, message=None, data=None):
    return {
        "status": status,
        "message": message,
        "data": data
    }

@app.get('/api/health')
def API_Health():
    checkHealth = requests.get(f'{AGENT_ENDPOINT}/health')
    return checkHealth.json()

def AgentCompletion(clientMessages):
    try:
        client = OpenAI(
            base_url = f'{AGENT_ENDPOINT}/api/v1/',
            api_key = AGENT_ACCESS_KEY,
        )

        response = client.chat.completions.create(
            model = "n/a",
            stream=True,
            messages = clientMessages,
        )
    
        for choice in response:
            yield 'data: %s\n\n' % json.dumps(GenerateResponse(data=choice.to_dict(mode="json")))
        yield 'data: %s\n\n' % json.dumps(GenerateResponse(data="[DONE]"))
    except Exception as e:
        yield 'data: %s\n\n' % json.dumps(GenerateResponse(False, str(e)))


@app.post('/api/completion')
def API_Completion():
    data = request.get_json()
    if "messages" not in data.keys() or data['messages'] is None or type(data['messages']) != list or len(data['messages']) == 0:
        return jsonify(GenerateResponse(False, "Please provide list of messages"))
    
    
    return Response(AgentCompletion(data['messages']), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(port=10087, threaded=True, host='0.0.0.0')