import requests
import io
import sqlite3
import pandas as pd
from datetime import date

from funds import funds
from lib import connect_db, fetch_current_holdings, get_days_changes, round_half_up
from generate_header import get_header
from generate_change_tab import get_change_tab

for fund in funds:
    current_holdings_df = fetch_current_holdings(fund["csv_url"])
    day_changes_df, day_start_date_str, day_end_date_str = get_days_changes(fund["name"], 1)
    weekly_changes_df, week_start_date_str, week_end_date_str = get_days_changes(fund["name"], 7)

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
                    <a class="nav-link" id="day-5-tab" data-bs-toggle="tab" href="#day-5" role="tab" aria-controls="day-5" aria-selected="false">5 Day &Delta;s</a>
                </div>
                </nav>
                <div class="tab-content" id="nav-tabContent">
                    <div class="tab-pane fade show active" id="holdings" role="tabpanel" aria-labelledby="holdings">
                        <div class="row pt-3">
                            <h3>Holdings as of {day_end_date_str}</h3>
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

    # Add changes tabs
    html += get_change_tab(day_changes_df, day_start_date_str, day_end_date_str, 1)
    html += get_change_tab(weekly_changes_df, week_start_date_str, week_end_date_str, 5)

    html += """
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-576GKZKB5W"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-576GKZKB5W');
        </script>
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