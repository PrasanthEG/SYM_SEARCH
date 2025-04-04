import psycopg2
import re
import sys
import os

# PostgreSQL Database Connection
DB_CONFIG = {
    "dbname": "symbols",
    "user": "postgres",
    "password": "postgres123",
    "host": "localhost",
    "port": "5432"
}

# Create table query
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS mutual_funds (
    scheme_code VARCHAR(20) PRIMARY KEY,  -- Ensuring uniqueness
    isin_div_payout VARCHAR(20),
    isin_growth VARCHAR(20),
    scheme_name TEXT,
    net_asset_value DECIMAL(20,6) NULL,
    nav_date DATE
);
"""

# Function to create the table
def create_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_QUERY)
    conn.commit()
    cur.close()
    conn.close()

# Function to parse data
def parse_data(file_path):
    funds = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if re.match(r"^\d{5,};", line):  # Detects data rows
                parts = line.split(";")
                if len(parts) == 6:
                    scheme_code, isin_div_payout, isin_growth, scheme_name, nav, date = parts
                    
                    # Validate NAV (set to None if 'NA')
                    nav_value = None if nav.upper() == "N.A." else float(nav)

                    funds.append((scheme_code, isin_div_payout, isin_growth, scheme_name, nav_value, date))
    return funds


# Function to insert data
def insert_data(funds):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    
    INSERT_QUERY = """
INSERT INTO mutual_funds (scheme_code, isin_div_payout, isin_growth, scheme_name, net_asset_value, nav_date)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (scheme_code) 
DO UPDATE SET 
    isin_div_payout = EXCLUDED.isin_div_payout,
    isin_growth = EXCLUDED.isin_growth,
    scheme_name = EXCLUDED.scheme_name,
    net_asset_value = EXCLUDED.net_asset_value,
    nav_date = EXCLUDED.nav_date;
"""
  
    
    cur.executemany(INSERT_QUERY, funds)
    conn.commit()
    cur.close()
    conn.close()

# Main Execution
if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Usage: python dumper.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print("Error: File not found.")
        sys.exit(1)
    create_table()
    data = parse_data(file_path)
    insert_data(data)
    print("Data successfully inserted into PostgreSQL!")
