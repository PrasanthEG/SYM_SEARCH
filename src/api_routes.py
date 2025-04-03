from flask import Flask,Blueprint, request, jsonify
from sqlalchemy.orm import aliased
from sqlalchemy.sql import case
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,decode_token,verify_jwt_in_request
from src.extensions import db
from src.models import EquitySymbol
from datetime import datetime,timedelta
from flask_cors import CORS, cross_origin
from sqlalchemy import func,desc
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
from src.config import Config




app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
#app.register_blueprint(routes)



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



@api_blueprint.route('/api2/add_symbols', methods=['POST'])
def add_symbol():
    """ Add a new symbol """
    data = request.json
    new_symbol = EquitySymbol(
        token=data.get("token"),
        symbol=data.get("symbol"),
        series=data.get("series"),
        instrument_type=data.get("instrument_type"),
        issued_capital=data.get("issued_capital"),
        permitted_to_trade=data.get("permitted_to_trade"),
        credit_rating=data.get("credit_rating"),
        security_eligibility_per_market=data.get("security_eligibility_per_market"),
        board_lot_quantity=data.get("board_lot_quantity"),
        tick_size=data.get("tick_size"),
        name=data.get("name"),
        issue_rate=data.get("issue_rate"),
        issue_start_date=data.get("issue_start_date"),
        issue_ip_date=data.get("issue_ip_date"),
        maturity_date=data.get("maturity_date"),
        freeze_percent=data.get("freeze_percent"),
        listing_date=data.get("listing_date"),
        expulsion_date=data.get("expulsion_date"),
        re_admission_date=data.get("re_admission_date"),
        ex_date=data.get("ex_date"),
        record_date=data.get("record_date"),
        delivery_date_start=data.get("delivery_date_start"),
        no_delivery_date_end=data.get("no_delivery_date_end"),
        participant_in_mkt_index=data.get("participant_in_mkt_index"),
        aon=data.get("aon"),
        mf=data.get("mf"),
        settlement_type=data.get("settlement_type"),
        book_closure_start_date=data.get("book_closure_start_date"),
        book_closure_end_date=data.get("book_closure_end_date"),
        dividend=data.get("dividend"),
        rights=data.get("rights"),
        bonus=data.get("bonus"),
        interest=data.get("interest"),
        agm=data.get("agm"),
        egm=data.get("egm"),
        spread=data.get("spread"),
        mm_min_qty=data.get("mm_min_qty"),
        ssec=data.get("ssec"),
        remarks=data.get("remarks"),
        local_db_update_date_time=data.get("local_db_update_date_time"),
        delete_flag=data.get("delete_flag"),
        face_value=data.get("face_value"),
        isin_number=data.get("isin_number")
    )
    db.session.add(new_symbol)
    db.session.commit()
    return jsonify(new_symbol.to_dict()), 201




if __name__ == "__main__":
    app.run(debug=True)

