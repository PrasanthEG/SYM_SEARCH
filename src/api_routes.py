from flask import Flask,Blueprint, request, jsonify
from sqlalchemy.orm import aliased,sessionmaker
from sqlalchemy.sql import case
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,decode_token,verify_jwt_in_request
from src.extensions import db
from src.models import EquitySymbol,Instrument
from datetime import datetime,timedelta
from flask_cors import CORS, cross_origin
from sqlalchemy import func,desc,create_engine, or_
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
from src.config import Config




app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
#app.register_blueprint(routes)



DATABASE_URL = app.config["SQLALCHEMY_DATABASE_URI"]
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Priority Maps
ASSET_PRIORITY = { "INDEX": 0,"EQ": 1, "FUTIDX": 2, "FUTSTK": 3, "OPTIDX": 4, "OPTSTK": 5, "COM": 6, "COMDTY": 6, "FUTCUR": 7, "OPTCUR": 8,"MF": 9, "DB": 10, ,"WARRANT": 11}
EXCHANGE_PRIORITY = {"NSE": 0, "BSE": 1, "MCX": 2, "NCDEX": 3}


api_blueprint = Blueprint('api2', __name__)
#@api_blueprint.route('/api2')
@cross_origin()  # CORS only for this route


@api_blueprint.before_request
def log_headers():
    print(f"Incoming Request: {request.method} {request.url}")
    print(f"Headers: {request.headers}")
   

@api_blueprint.route("/api2/check_session", methods=["GET"])
@jwt_required()
def check_session():           
    try:
        user = get_jwt_identity()  # Extract user info from JWT
        return jsonify({"authenticated": True, "user": user}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"authenticated": False, "error": str(e)}), 401


@api_blueprint.route('/api2/symbols', methods=['GET'])
def get_symbols():
    symbol = request.args.get('query', '')
    asset_type = request.args.get('assetType', '')
    """ Fetch all symbols """
    
    symbols = EquitySymbol.query.filter(EquitySymbol.symbol.ilike(f"%{symbol}%")).all()

    return jsonify([symbol.to_dict() for symbol in symbols]), 200



def sort_priority(item):
    return (
        ASSET_PRIORITY.get(item.instrument_type.upper(), 99),
        EXCHANGE_PRIORITY.get(item.exchange.upper(), 99)
    )

@api_blueprint.route("/api2/search", methods=["GET"])
def search():
    symbol = request.args.get('symbol', '').upper()
    asset_type = request.args.get('assetType', '').upper()
    if not symbol:
        return jsonify({"error": "Missing Symbol."}), 400

    session = SessionLocal()
    try:
        results = session.query(Instrument).filter(
            or_(
                Instrument.trading_symbol.ilike(f"{symbol}%"),
                Instrument.name.ilike(f"{symbol}%"),
                Instrument.trading_symbol.ilike(f"%{symbol}%"),
                Instrument.name.ilike(f"%{symbol}%")
            )
        ).all()

        sorted_results = sorted(results, key=sort_priority)
        data = [r.to_dict() for r in sorted_results[:50]]  # Assuming you have a `to_dict()` method in model
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()



if __name__ == "__main__":
    app.run(debug=True)

