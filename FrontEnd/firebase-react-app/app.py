from flask import Flask, request,jsonify,redirect, url_for, render_template
from firebase_admin import credentials, firestore, initialize_app
import subprocess
import re

app = Flask(__name__)

cred = credentials.Certificate("serviceAccountKey.json")
firebase_app = initialize_app(cred)
db = firestore.client()

@app.route('/violated')
def get_violated_data():
    data = []
    docs = db.collection('violations').stream()
    for doc in docs:
        data.append(doc.to_dict())
    return jsonify(data)

@app.route('/data')
def get_data():
    data = []
    docs = db.collection('details').stream()
    for doc in docs:
            data.append(doc.to_dict())
    return jsonify(data)

@app.route('/login')
def get_login_data():
    data = []
    docs = db.collection('login').stream()
    for doc in docs:
        data.append(doc.to_dict())
    return jsonify(data)

@app.route('/run-script')
def run_script():
    subprocess.run(['python', 'main.py'])  # Replace 'main.py' with the actual path to your Python script
    return jsonify({'message': 'Script executed successfully'})

def validate_sri_lankan_vehicle_number(vehicle_number):
    pattern = r'^[A-Za-z]{1,3}\d+$'
    if re.match(pattern, vehicle_number):
        return False
    else:
        return True

@app.route('/add_detail', methods=['POST'])
def add_details():
    data = request.json
    email = data.get('email')
    name = data.get('name')
    vehicle_number = data.get('vehicle_number')
    
    vehicle_ref = db.collection('details')
    vehicle_ref.add({'name': name, 'email': email, 'vehicle_number': vehicle_number})
    if not all([name, email, vehicle_number]):
        return jsonify({'error': 'Missing data'}), 400
    
    if (validate_sri_lankan_vehicle_number(vehicle_number)):
        return jsonify({'error': 'Invalid Sri Lankan vehicle numbe'}), 400
    
    return jsonify({'message': 'vehicle details added successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)