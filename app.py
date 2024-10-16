import os
import json
from flask import Flask, request, jsonify
import hashlib
from aws_lambda_powertools import Logger, Tracer
import boto3
from codeguru_profiler_agent import Profiler

app = Flask(__name__)

# Initialize Logger and Tracer
logger = Logger()
tracer = Tracer()

# Vulnerable global variable with your secret key
SECRET_KEY = "aL3X4D/hFQ6eefufuah6d1axLcJmgSRC+aPv6w8J"

@app.route('/hash', methods=['POST'])
def hash_data():
    data = request.json.get('data')
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    hash_object = hashlib.sha1(data.encode())
    return jsonify({'hashed_data': hash_object.hexdigest()}), 200

@app.route('/file_upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join('/uploads', filename))
    return jsonify({'success': 'File uploaded'}), 200

@app.route('/config', methods=['GET'])
def get_config():
    return jsonify({'secret_key': SECRET_KEY}), 200

@app.route('/eval', methods=['POST'])
def eval_code():
    code = request.json.get('code')
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    try:
        result = eval(code)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/some_route', methods=['GET'])
@tracer.capture_method
def some_method():
    logger.info("Some method has been called")
    return jsonify({'message': 'Hello, World!'}), 200

def start_application():
    app.run(debug=True)

if __name__ == "__main__":
    custom_session = boto3.session.Session(profile_name='dev', region_name='us-east-1')
    Profiler(profiling_group_name="VulnerablePythonAppProfiler", aws_session=custom_session).start()
    start_application()
