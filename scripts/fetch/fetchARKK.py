import requests
import io
import sqlite3
import pandas as pd
from datetime import date

url = "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv"

def insert_data(df):
	insert_sql = "INSERT INTO ARKK(date, fund, company, ticker, cusip, shares, value, weight) VALUES "
	row_str_list = []
	for _, row in df.iterrows():
		row_str = f"""('{row["date"]}', '{row["fund"]}', '{row["company"]}', '{row["ticker"]}', '{row["cusip"]}', {int(row["shares"])}, {row["market value($)"]}, {row["weight(%)"]})"""
		row_str_list.append(row_str)

	insert_sql += ",".join(row_str_list)
	cur = conn.cursor()
	cur.executescript(insert_sql)
	conn.commit()

conn = sqlite3.connect("../db/ArkTracker.db")
print("Opened database successfully!")

r = requests.get(url)
data = r.content.decode('utf8')
df = pd.read_csv(io.StringIO(data))
df = df.dropna(how='any')
last_updated = df['date'][1]

print(f"Holdings last updated: {last_updated}")

query = conn.execute(f"SELECT COUNT(*) FROM ARKK WHERE date = \"{last_updated}\";")
data_fetched = query.fetchone()[0]

if data_fetched == 0:
	print("Fetching data...")
	r = requests.get(url)
	data = r.content.decode('utf8')
	df = pd.read_csv(io.StringIO(data))
	df = df.dropna(how='any')
	insert_data(df)
else:
	print("Most recent data already fetched.")
	

conn.close()


