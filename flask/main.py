from flask import Flask, jsonify
from flask_cors import CORS
from blueprints import init_app

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

init_app(app)

@app.route('/')
def home():
    return jsonify(message="Hello, World!")

if __name__ == '__main__':
    app.run(debug=True)
