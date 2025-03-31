import os
import sys
import csv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.models import EquitySymbol  # Import your SQLAlchemy model


def parse_value(value, dtype):
    """Parse value based on data type."""
    if value in [None, "", "NULL"]:
        return None
    try:
        if dtype == "bigint":
            return int(value)
        elif dtype == "int":
            return int(value)
        elif dtype == "float":
            return float(value)
        elif dtype == "string":
            return value.strip()
    except ValueError:
        return None

def insert_data_from_file(file_path, session):
    """Read data from a pipe-separated file and insert it into the database."""
    
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="|")
        next(reader)  # Skip the header row

        for row in reader:
            try:  
                trade_flag = 1 if parse_value(row[12], "string") == 'A' else 0
                instr_type = 0 if parse_value(row[5], "string") == 'E' else 4
                series = 'EQ' if (row[22] and parse_value(row[22], "string")) == 'EQ' else 'BE'
            
            
                equity = EquitySymbol(
                    token=parse_value(row[0], "bigint"),
                    exchange=parse_value(row[1], "string"),
                    symbol=parse_value(row[2], "string"),
                    name=parse_value(row[3], "string"),
                    instrument_type=instr_type,
                    permitted_to_trade=trade_flag,
                    face_value=parse_value(row[8], "bigint"),
                    board_lot_quantity=parse_value(row[9], "bigint"),
                    tick_size=parse_value(row[10], "bigint"),
                    delivery_date_start=parse_value(row[14], "bigint"),
                    no_delivery_date_end=parse_value(row[15], "bigint"),
                    isin_number=parse_value(row[17], "string"),
                    series=series,
                    book_closure_start_date=parse_value(row[19], "bigint"),
                    book_closure_end_date=parse_value(row[24], "bigint"),
                    settlement_type=parse_value(row[25], "int"),
                )
                session.add(equity)
     
        session.commit()
        print("Data successfully inserted.")
    
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()

def main():
    if len(sys.argv) < 2:
        print("Usage: python dumper.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print("Error: File not found.")
        sys.exit(1)
    DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/symbols"
    engine = create_engine(DATABASE_URL)  # Update credentials
    Session = sessionmaker(bind=engine)
    session = Session()

    insert_data_from_file(file_path, session)
    session.close()

if __name__ == "__main__":
    main()
