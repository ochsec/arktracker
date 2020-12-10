import math
import requests
import io
import sqlite3
import pandas as pd
from datetime import date, timedelta

def connect_db():
    conn = sqlite3.connect("../db/ArkTracker.db")
    print("Opened database successfully!")
    return conn

def fetch_current_holdings(url):
    print("Fetching data...")
    r = requests.get(url)
    data = r.content.decode('utf8')
    df = pd.read_csv(io.StringIO(data))
    df = df.dropna(how='any')
    return df

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def get_daily_changes(fund_name):
    count = 0
    days = 0
    date1 = None # most recent market day that has data in database
    date2 = None # day before the most recent market day that has data in database

    conn = connect_db()

    while count == 0 and days < 8:
        date1 = date.today() - timedelta(days=days)
        date1_str = date1.strftime("%-m/%-d/%Y")
        print(f"Last market day: {date1_str}")
        query = conn.execute(f"SELECT COUNT(*) FROM {fund_name} WHERE date = \"{date1_str}\";")
        count = query.fetchone()[0]
        days += 1

    count = 0
    days = 1

    while count == 0 and days < 8:
        date2 = date1 - timedelta(days=days)
        date2_str = date2.strftime("%-m/%-d/%Y")
        query = conn.execute(f"SELECT COUNT(*) FROM {fund_name} WHERE date = \"{date2_str}\";")    
        count = query.fetchone()[0]
        if count != 0:
            print(f"2 market days ago: {date2_str}")
        days += 1

    if date1 is None:
        print("No previous data")
    else:
        df1 = pd.read_sql_query(f"SELECT * FROM {fund_name} WHERE date = \"{date1_str}\";", conn, index_col="id")
        df1 = df1[['company', 'ticker', 'shares', 'value', 'weight']]
        
    if date2 is None:
        print("No market data before previous market day.")
    else:
        df2 = pd.read_sql_query(f"SELECT * FROM {fund_name} WHERE date = \"{date2_str}\";", conn, index_col="id")
        df2 = df2[['company', 'shares', 'value', 'weight']]
        df2 = df2.rename(columns = {
            'shares': 'prev_shares',
            'value': 'prev_value',
            'weight': 'prev_weight'
        })

    df = pd.merge(df1, df2, how='left', on=['company'])
    df['shares_diff'] = df['shares'] - df['prev_shares']
    df['value_diff'] = df['value'] - df['prev_value']
    df['weight_diff'] = df['weight'] - df['prev_weight']
    return df, date2_str, date1_str