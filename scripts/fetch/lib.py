import requests
import io
import sqlite3
import pandas as pd
from datetime import date

def connect_db():
    conn = sqlite3.connect("../db/ArkTracker.db")
    print("Opened database successfully!")
    return conn

def insert_data(fund_name, df, conn):
	insert_sql = f"INSERT INTO {fund_name}(date, fund, company, ticker, cusip, shares, value, weight) VALUES "
	row_str_list = []
	for _, row in df.iterrows():
		row_str = f"""('{row["date"]}', '{row["fund"]}', '{row["company"]}', '{row["ticker"]}', '{row["cusip"]}', {int(row["shares"])}, {row["market value($)"]}, {row["weight(%)"]})"""
		row_str_list.append(row_str)

	insert_sql += ",".join(row_str_list)
	cur = conn.cursor()
	cur.executescript(insert_sql)
	conn.commit()

def check_updated(url, conn):
    r = requests.get(url)
    data = r.content.decode('utf8')
    df = pd.read_csv(io.StringIO(data))
    df = df.dropna(how='any')
    last_updated = df['date'][1]
    print(f"Holdings last updated: {last_updated}")

    query = conn.execute(f"SELECT COUNT(*) FROM ARKK WHERE date = \"{last_updated}\";")
    count = query.fetchone()[0]

    if count == 0:
        print("Fetching data...")        
        return False, df
    else:
        print("Most recent data already fetched.")
        conn.close()
        return True, None
    
