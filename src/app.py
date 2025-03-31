from flask import Flask,jsonify
from src.config import Config
from flask_jwt_extended import JWTManager,get_jwt_identity
from flask_cors import CORS
from src.api_routes import api_blueprint
from src.extensions import db
from datetime import timedelta
from flask_jwt_extended.exceptions import NoAuthorizationError




app = Flask(__name__)
CORS(app)


app.config.from_object(Config)

app.config["JWT_SECRET_KEY"] = "PRAGMATIC_2025@DIGITAL"  # Ensure it's set
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Increase expiry
app.config["JWT_ALGORITHM"] = "HS256"  # Ensure this matches frontend
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False  # Try disabling CSRF protection for now



jwt = JWTManager(app)

# Handle Missing or Invalid Token
@app.errorhandler(NoAuthorizationError)
def handle_missing_token(e):
    return jsonify({"message": "Session timed out. Please log in again.", "error": "unauthorized"}), 401



# Handle expired token using callback
@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    return jsonify({"message": "Session timed out. Please log in again.", "error": "unauthorized"}), 401


app.register_blueprint(api_blueprint)
db.init_app(app) 


if __name__ == "__main__":
    #app.run(debug=True, port=6000)
    app.run(host="0.0.0.0", port=5010, debug=True)




