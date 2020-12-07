import requests
import io
import sqlite3
import pandas as pd
from datetime import date

url = "https://ark-funds.com/wp-content/fundsiteliterature/csv/THE_3D_PRINTING_ETF_PRNT_HOLDINGS.csv"

def insert_data(df):
	insert_sql = "INSERT INTO PRNT(date, fund, company, ticker, cusip, shares, value, weight) VALUES "
	row_str_list = []
	for i, row in df.iterrows():
		row_str = f"""('{row["date"]}', '{row["fund"]}', '{row["company"]}', '{row["ticker"]}', '{row["cusip"]}', {int(row["shares"])}, {row["market value($)"]}, {row["weight(%)"]})"""
		row_str_list.append(row_str)

	insert_sql += ",".join(row_str_list)
	cur = conn.cursor()
	cur.executescript(insert_sql)
	conn.commit()

conn = sqlite3.connect("../db/ArkTracker.db")
print("Opened database successfully!")

today = date.today()
print("Today's date:", today.strftime("%-m/%-d/%Y"))

query = conn.execute(f"SELECT COUNT(*) FROM PRNT WHERE date = \"{today.strftime('%-m/%-d/%Y')}\";")
data_fetched = query.fetchone()[0]

if data_fetched == 0:
	print("Fetching data...")
	r = requests.get(url)
	data = r.content.decode('utf8')
	df = pd.read_csv(io.StringIO(data))
	df = df.dropna(how='any')
	insert_data(df)
else:
	print("Yesterday's data already fetched.")
	

conn.close()


