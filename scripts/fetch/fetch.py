from funds import funds
from lib import connect_db, check_updated, insert_data

for fund in funds:
    conn = connect_db()
    updated, df = check_updated(fund["csv_url"], conn)

    if not updated:
        insert_data(fund["name"], df, conn)
