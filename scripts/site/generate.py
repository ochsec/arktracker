import requests
import io
import sqlite3
import pandas as pd
from datetime import date

from funds import funds
from lib import connect_db, fetch_current_holdings, get_daily_changes, round_half_up
from generate_header import get_header

for fund in funds:
    current_holdings_df = fetch_current_holdings(fund["csv_url"])
    daily_changes_df, start_date_str, end_date_str = get_daily_changes(fund["name"])
    # print(daily_changes_df)

    html = get_header()
    html += f"""
            <div class="container-fluid">
                <div class="row pt-3">
                <h2>{fund["full_name"]}</h2>
                </div>
                <nav>
                <div class="nav nav-tabs" id="nav-tab" role="tablist">
                    <a class="nav-link active" id="holdings-tab" data-bs-toggle="tab" href="#holdings" role="tab" aria-controls="holdings" aria-selected="true">Holdings</a>
                    <a class="nav-link" id="day-1-tab" data-bs-toggle="tab" href="#day-1" role="tab" aria-controls="day-1" aria-selected="false">1 Day &Delta;s</a>
                    <!-- <a class="nav-link" id="day7-tab" data-bs-toggle="tab" href="#day7" role="tab" aria-controls="day7" aria-selected="false">7 Day &Delta;s</a> -->        
                </div>
                </nav>
                <div class="tab-content" id="nav-tabContent">
                    <div class="tab-pane fade show active" id="holdings" role="tabpanel" aria-labelledby="holdings">
                        <div class="row pt-3">
                            <h3>Holdings as of {end_date_str}</h3>
                        </div>
                        <table class="table table-hover">
                        <tr>
                            <th>Company</th>
                            <th>Ticker</th>
                            <th>Shares</th>
                            <th>Market Value ($)</th>
                            <th>Weight %</th>
                        </tr>
            """

    for _, row in current_holdings_df.iterrows():
        html += f"""
                <tr>
                    <td>{row["company"]}</td>
                    <td>{row["ticker"]}</td>
                    <td>{row["shares"]}</td>
                    <td>{row["market value($)"]}</td>
                    <td>{row["weight(%)"]}</td>
                </tr>
        """

    html += f"""
            </table>
            <a href="{fund["csv_url"]}">Data Source</a>
            </div>
        """

    html += f"""
            <div class="tab-pane fade" id="day-1" role="tabpanel" aria-labelledby="day-1-tab">
                <div class="container-fluid">
                    <div class="row pt-3">
                        <h3>1 Day Changes {start_date_str} - {end_date_str}</h3>
                    <table class="table table-hover">
                        <tr>
                            <th>Company</th>
                            <th>Ticker</th>
                            <th>&Delta; Shares</th>
                            <th>&Delta; Market Value ($)</th>
                            <th>&Delta; Weight %</th>
                        </tr>
        """

    for _, row in daily_changes_df.iterrows():
        html += f"""
                <tr>
            """

        if "- Added" in row["company"]:
            html += f"""
                <td class="table-success">{row["company"]}</td>
                <td class="table-success">{row["ticker"]}</td>
            """
        elif "- Removed" in row["company"]:
            html += f"""
                <td class="table-danger">{row["company"]}</td>
                <td class="table-danger">{row["ticker"]}</td>
            """            
        else:
            html += f"""
                <td>{row["company"]}</td>
                <td>{row["ticker"]}</td>
            """


        if row["shares_diff"] > 0:
            html += f"""<td class="table-success">+{row["shares_diff"]}</td>"""
        elif row["shares_diff"] < 0:
            html += f"""<td class="table-danger">{row["shares_diff"]}</td>"""
        else:
            html += f"""<td>{row["shares_diff"]}</td>"""

        if row["value_diff"] == 0:
            html += f"""<td>{int(row["value_diff"])}</td>"""
        elif row["value_diff"] > 0:
            html += f"""<td class="table-success">+{int(row["value_diff"])}</td>"""
        elif row["value_diff"] < 0:
            html += f"""<td class="table-danger">{int(row["value_diff"])}</td>"""
        else:
            html += f"""<td>{row["value_diff"]}</td>"""

        if row["weight_diff"] == 0:
            html += f"""<td>{round_half_up(row["weight_diff"], 2)}</td>"""
        elif row["weight_diff"] > 0:
            html += f"""<td class="table-success">+{round_half_up(row["weight_diff"], 2)}</td>"""
        elif row["weight_diff"] < 0:
            html += f"""<td class="table-danger">{round_half_up(row["weight_diff"], 2)}</td>"""
        else:
            html += f"""<td>{row["weight_diff"]}</td>"""

        html += """
            </tr>
        """

    html += """
                </table>
            </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>
        </body>
        </html>
    """

    file = open(f"""../site/{fund["page_name"]}""", "w")
    file.write(html)
    file.close()

    if fund["name"] == "ARKK":
        file = open(f"../site/index.html", "w")
        file.write(html)
        file.close()