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

def get_date_str(date):
    return date.strftime("%-m/%-d/%Y")

def get_fund_records_count_for_date(fund_name, date_str, conn):
    query = conn.execute(f"SELECT COUNT(*) FROM {fund_name} WHERE date = \"{date_str}\";")
    count = query.fetchone()[0]
    return count

def get_fund_records(fund_name, ticker, conn):
    df = pd.read_sql_query(f"""SELECT date, company, ticker, shares, value, weight 
        FROM {fund_name} WHERE ticker = '{ticker}';""", conn)
    return df

def get_days_changes(fund_name, period_days=0):
    count = 0
    days = 0
    date1 = None # most recent market day that has data in database
    date2 = None # day before the most recent market day that has data in database

    conn = connect_db()

    # find most recent market day
    while count == 0 and days < 8:
        date1 = date.today() - timedelta(days=days)
        date1_str = get_date_str(date1)
        count = get_fund_records_count_for_date(fund_name, date1_str, conn)
        if count > 0:
            print(f"Last market day: {date1_str}")
        else:
            days += 1

    count = 0
    days = period_days

    # find date at beginning of period
    while count == 0 and days < period_days + 8:
        date2 = date1 - timedelta(days=days)
        date2_str = get_date_str(date2)
        count = get_fund_records_count_for_date(fund_name, date2_str, conn)
        if count > 0:
            print(f"First market day of period: {date2_str}")
        else:
            days += 1

    if date1 is None:
        print("No previous data")
    else:
        df1 = pd.read_sql_query(f"SELECT * FROM {fund_name} WHERE date = \"{date1_str}\";", conn, index_col="id")
        df1 = df1[['company', 'ticker', 'shares', 'value', 'weight']]
        
    if date2 is None:
        print(f"No market data at or before {period_days} ago.")
    else:
        df2 = pd.read_sql_query(f"SELECT * FROM {fund_name} WHERE date = \"{date2_str}\";", conn, index_col="id")
        df2 = df2[['company', 'ticker', 'shares', 'value', 'weight']]
        df2 = df2.rename(columns = {
            'shares': 'prev_shares',
            'value': 'prev_value',
            'weight': 'prev_weight'
        })

    new_companies = []
    
    for i, irow in df1.iterrows():
        found = False
        company = irow['company']
        for j, jrow in df2.iterrows():
            if jrow['company'] == company:
                found = True

        if not found:
            new_companies.append(company)

    print(f"New companies for {fund_name}: {new_companies}")

    removed_companies = []

    for i, irow in df2.iterrows():
        found = False
        company = irow['company']
        for j, jrow in df1.iterrows():
            if jrow['company'] == company:
                found = True

        if not found:
            removed_companies.append(company)

    print(f"Removed companies from {fund_name}: {removed_companies}")

    df = pd.merge(df1, df2[['company', 'prev_shares', 'prev_value', 'prev_weight']], how='left', on=['company'])
    df['shares_diff'] = df['shares'] - df['prev_shares']
    df['value_diff'] = df['value'] - df['prev_value']
    df['weight_diff'] = df['weight'] - df['prev_weight']

    for company in new_companies:
        for _, row in df.iterrows():
            if row['company'] == company:
                df = df.replace([company], f"{company} - Added")

    for company in removed_companies:
        for _, row in df2.iterrows():
            if row['company'] == company:
                print(f"Removed company row: {row}")
                d = {
                    'company': f"{row['company']} - Removed",
                    'ticker': row['ticker'],
                    'shares': 0,
                    'value': 0,
                    'weight': 0,
                    'prev_shares': row['prev_shares'],
                    'prev_value': row['prev_value'],
                    'prev_weight': row['prev_weight'],
                    'shares_diff': -(row['prev_shares']),
                    'value_diff': -(row['prev_value']),
                    'weight_diff': -(row['prev_weight']),
                }
                df = df.append(d, ignore_index=True)

    return df, date2_str, date1_str
