import requests
import io
import sqlite3
import pandas as pd
from datetime import date

from generate_header import get_header_markdown

url = "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv"

print("Fetching data...")
r = requests.get(url)
data = r.content.decode('utf8')
df = pd.read_csv(io.StringIO(data))
df = df.dropna(how='any')

html = get_header_markdown()
html += """
        <h2>ARKQ / ARK Autonomous Technology & Robotics ETF</h2>
        <h3>Holdings</h3>
        <table>
            <tr>
                <th>Company</th>
                <th>Ticker</th>
                <th>Shares</th>
                <th>Market Value ($)</th>
                <th>Weight %</th>
            </tr>
"""

for _, row in df.iterrows():
    html += f"""
            <tr>
                <td>{row["company"]}</td>
                <td>{row["ticker"]}</td>
                <td>{row["shares"]}</td>
                <td>{row["market value($)"]}</td>
                <td>{row["weight(%)"]}</td>
            </tr>
    """

html += """
        </table>
    </body>
    </html>
"""

file = open("../site/arkq.html", "w")
file.write(html)
file.close()