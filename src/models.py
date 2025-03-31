from flask_sqlalchemy import SQLAlchemy
from src.extensions import db
from datetime import datetime


class EquitySymbol(db.Model):
    __tablename__ = 'equity_symbols'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.BigInteger, nullable=False, unique=False)
    symbol = db.Column(db.String(50), nullable=False)
    series = db.Column(db.String(2), nullable=False)
    instrument_type = db.Column(db.SmallInteger, nullable=False)
    issued_capital = db.Column(db.Float, nullable=True)
    permitted_to_trade = db.Column(db.SmallInteger, nullable=False)
    credit_rating = db.Column(db.String(17), nullable=True)
    security_eligibility_per_market = db.Column(db.String(6), nullable=True)
    board_lot_quantity = db.Column(db.BigInteger, nullable=True)
    tick_size = db.Column(db.BigInteger, nullable=True)

    # Dummy fields (11 placeholders)
    dummy1 = db.Column(db.Integer, nullable=True)
    dummy2 = db.Column(db.Integer, nullable=True)
    dummy3 = db.Column(db.Integer, nullable=True)
    dummy4 = db.Column(db.Integer, nullable=True)
    dummy5 = db.Column(db.Integer, nullable=True)
    dummy6 = db.Column(db.Integer, nullable=True)
    dummy7 = db.Column(db.Integer, nullable=True)
    dummy8 = db.Column(db.Integer, nullable=True)
    dummy9 = db.Column(db.Integer, nullable=True)
    dummy10 = db.Column(db.Integer, nullable=True)
    dummy11 = db.Column(db.Integer, nullable=True)

    name = db.Column(db.String(100), nullable=False)
    issue_rate = db.Column(db.SmallInteger, nullable=True)
    issue_start_date = db.Column(db.BigInteger, nullable=True)
    issue_ip_date = db.Column(db.BigInteger, nullable=True)
    maturity_date = db.Column(db.BigInteger, nullable=True)
    freeze_percent = db.Column(db.SmallInteger, nullable=True)
    listing_date = db.Column(db.BigInteger, nullable=True)
    expulsion_date = db.Column(db.BigInteger, nullable=True)
    re_admission_date = db.Column(db.BigInteger, nullable=True)
    ex_date = db.Column(db.BigInteger, nullable=True)
    record_date = db.Column(db.BigInteger, nullable=True)
    delivery_date_start = db.Column(db.BigInteger, nullable=True)
    no_delivery_date_end = db.Column(db.BigInteger, nullable=True)

    # Market participation & settlement
    participant_in_mkt_index = db.Column(db.String(1), nullable=True)
    aon = db.Column(db.String(1), nullable=True)
    mf = db.Column(db.String(1), nullable=True)
    settlement_type = db.Column(db.SmallInteger, nullable=True)
    
    # Book closure & event fields
    book_closure_start_date = db.Column(db.BigInteger, nullable=True)
    book_closure_end_date = db.Column(db.BigInteger, nullable=True)
    dividend = db.Column(db.String(1), nullable=True)
    rights = db.Column(db.String(1), nullable=True)
    bonus = db.Column(db.String(1), nullable=True)
    interest = db.Column(db.String(1), nullable=True)
    agm = db.Column(db.String(1), nullable=True)
    egm = db.Column(db.String(1), nullable=True)

    # Additional fields
    spread = db.Column(db.BigInteger, nullable=True)
    mm_min_qty = db.Column(db.BigInteger, nullable=True)
    ssec = db.Column(db.SmallInteger, nullable=True)
    remarks = db.Column(db.String(100), nullable=True)
    local_db_update_date_time = db.Column(db.BigInteger, nullable=True)
    delete_flag = db.Column(db.String(1), nullable=True)
    face_value = db.Column(db.BigInteger, nullable=True)
    isin_number = db.Column(db.String(20), unique=False, nullable=False)
    exchange = db.Column(db.String[10], nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    

    def to_dict(self):
        return {
            "id": self.id,
            "token": self.token,
            "symbol": self.symbol,
            "name": self.name,
            "isin_number": self.isin_number,
            "series": self.series,
            "instrument_type": self.instrument_type,
            "exchange":self.exchange
            
        }   
