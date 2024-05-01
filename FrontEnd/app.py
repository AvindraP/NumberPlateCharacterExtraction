from flask import Flask, jsonify
from firebase_admin import credentials, firestore, initialize_app


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


if __name__ == '__main__':
    app.run(debug=True)
