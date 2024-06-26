from flask import Flask, Response, jsonify
from flask_cors import CORS
from blueprints import init_app

app = Flask(__name__)
app.config["CORS_AUTOMATIC_OPTIONS"] = True
CORS(app, supports_credentials=True)  # This will enable CORS for all routes

init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
