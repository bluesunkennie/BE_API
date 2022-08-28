# Required Imports
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from flask_cors import CORS

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
device_ref = db.collection('device')


@app.route('/', methods=['GET'])
def home(): 
    return '<h1><center>Welcome to Device Back-End!</center></h1>'

""" Device """   
@app.route('/device', methods=['GET'])
def get_device():
    try:
        # Check if ID was passed to URL query
        device_id = request.args.get('id')
        if device_id:
            device = device_ref.document(device_id).get()
            return jsonify(device.to_dict()), 200
        else:
            devices = [doc.to_dict() for doc in device_ref.stream()]
            return jsonify(devices), 200
    except Exception as e:
        return f"An error occurred: {e}"


@app.route('/device', methods=['POST'])
def add_device():
    try:
        id = request.json['id_device']
        device_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An error occurred: {e}"
  
  
@app.route('/device', methods=['PUT'])
def update_device():
    try:
        id = request.json['id']
        device_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An error occurred: {e}"
    
    
@app.route('/device', methods=['DELETE'])
def delete_device():
    try:
        # Check for ID in URL query
        id = request.args.get('id')
        device_ref.document(id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An error occurred: {e}"
      

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
    