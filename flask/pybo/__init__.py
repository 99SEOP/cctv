from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from time import time

app = Flask(__name__)

CORS(app)

number = 0

@app.route('/')
def index():
    global number
    return jsonify({'number' : number})
    

@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    time = int(time())
    if request.method == 'GET':
        return jsonify(time)

    elif request.method == 'POST':
        # Accessing POST data
        data = request.json
        return jsonify(message="POST request received, CORS is enabled!", data=data)

@app.route('/numPlus', methods=['GET'])
def numPlus():
    global number
    number += 1
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)