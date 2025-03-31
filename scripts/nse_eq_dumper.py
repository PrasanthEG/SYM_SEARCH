import csv
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import EquitySymbol  # Import your SQLAlchemy model

# Database connection
DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/symbols"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def parse_value(value, data_type):
    """Convert values to the correct data type or return None if empty"""
    if value.strip() == "":
        return None
    try:
        if data_type == "int":
            return int(value)
        elif data_type == "float":
            return float(value)
        elif data_type == "bigint":
            return int(value)  # BigInt can be stored as int in Python
        return value.strip()
    except ValueError:
        return None

def insert_data_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="|")
        next(reader)  # Skip the header row

        for row in reader:
            if len(row) < 54:  # Ensure row has enough columns
                continue

            equity = EquitySymbol(
                token=parse_value(row[0], "bigint"),
                symbol=parse_value(row[1], "string"),
                series=parse_value(row[2], "string"),
                instrument_type=parse_value(row[3], "int"),
                issued_capital=parse_value(row[4], "float"),
                permitted_to_trade=parse_value(row[5], "int"),
                credit_rating=parse_value(row[6], "string"),
                security_eligibility_per_market=parse_value(row[7], "string"),
                board_lot_quantity=parse_value(row[8], "bigint"),
                tick_size=parse_value(row[9], "bigint"),
                dummy1=parse_value(row[10], "int"),
                dummy2=parse_value(row[11], "int"),
                dummy3=parse_value(row[12], "int"),
                dummy4=parse_value(row[13], "int"),
                dummy5=parse_value(row[14], "int"),
                dummy6=parse_value(row[15], "int"),
                dummy7=parse_value(row[16], "int"),
                dummy8=parse_value(row[17], "int"),
                dummy9=parse_value(row[18], "int"),
                dummy10=parse_value(row[19], "int"),
                dummy11=parse_value(row[20], "int"),
                name=parse_value(row[21], "string"),
                issue_rate=parse_value(row[22], "int"),
                issue_start_date=parse_value(row[23], "bigint"),
                issue_ip_date=parse_value(row[24], "bigint"),
                maturity_date=parse_value(row[25], "bigint"),
                freeze_percent=parse_value(row[26], "int"),
                listing_date=parse_value(row[27], "bigint"),
                expulsion_date=parse_value(row[28], "bigint"),
                re_admission_date=parse_value(row[29], "bigint"),
                ex_date=parse_value(row[30], "bigint"),
                record_date=parse_value(row[31], "bigint"),
                delivery_date_start=parse_value(row[32], "bigint"),
                no_delivery_date_end=parse_value(row[33], "bigint"),
                participant_in_mkt_index=parse_value(row[34], "string"),
                aon=parse_value(row[35], "string"),
                mf=parse_value(row[36], "string"),
                settlement_type=parse_value(row[37], "int"),
                book_closure_start_date=parse_value(row[38], "bigint"),
                book_closure_end_date=parse_value(row[39], "bigint"),
                dividend=parse_value(row[40], "string"),
                rights=parse_value(row[41], "string"),
                bonus=parse_value(row[42], "string"),
                interest=parse_value(row[43], "string"),
                agm=parse_value(row[44], "string"),
                egm=parse_value(row[45], "string"),
                spread=parse_value(row[46], "bigint"),
                mm_min_qty=parse_value(row[47], "bigint"),
                ssec=parse_value(row[48], "int"),
                remarks=parse_value(row[49], "string"),
                local_db_update_date_time=parse_value(row[50], "bigint"),
                delete_flag=parse_value(row[51], "string"),
                face_value=parse_value(row[52], "bigint"),
                isin_number=parse_value(row[53], "string"),
                exchange='NSE'
            )

            session.add(equity)

        session.commit()
        print("Data inserted successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dumper.py <filename>")
        sys.exit(1)

    file_path = sys.argv[1]
    insert_data_from_file(file_path)




 