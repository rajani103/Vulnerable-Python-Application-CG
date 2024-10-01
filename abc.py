# app.py

import os
import json
from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# Vulnerable global variable (potential sensitive data exposure)
SECRET_KEY = "my_secret_key"

@app.route('/hash', methods=['POST'])
def hash_data():
    # Insecure handling of user input (potentially unsafe data)
    data = request.json.get('data')
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Weak hash function (SHA1 is considered weak)
    hash_object = hashlib.sha1(data.encode())
    return jsonify({'hashed_data': hash_object.hexdigest()}), 200

@app.route('/file_upload', methods=['POST'])
def upload_file():
    # Insecure file upload (vulnerable to arbitrary file upload)
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    filename = file.filename
    file.save(os.path.join('/uploads', filename))  # Unsafe file saving path
    return jsonify({'success': 'File uploaded'}), 200

@app.route('/config', methods=['GET'])
def get_config():
    # Insecure config exposure (exposing sensitive config)
    return jsonify({'secret_key': SECRET_KEY}), 200

@app.route('/eval', methods=['POST'])
def eval_code():
    # Dangerous use of eval (vulnerable to code injection)
    code = request.json.get('code')
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    try:
        result = eval(code)  # Unsafe eval usage
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
