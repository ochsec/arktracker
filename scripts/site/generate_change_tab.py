from lib import round_half_up

def get_change_tab(changes_df, start_date_str, end_date_str, num_days):
    html = f"""
        <div class="tab-pane fade" id="day-{num_days}" role="tabpanel" aria-labelledby="day-{num_days}-tab">
            <div class="container-fluid">
                <div class="row pt-3">
                    <h3>{num_days} Market Day Changes {start_date_str} - {end_date_str}</h3>
                </div>
                <table class="table table-hover">
                    <tr>
                        <th>Company</th>
                        <th>ticker</th>
                        <th>&Delta; Shares</th>
                        <th>&Delta; Market Value ($)</th>
                        <th>&Delta; Weight %</th>
                    </tr>
    """

    for _, row in changes_df.iterrows():
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

        if "- Added" in row["company"]:
            html += f"""<td class="table-success">+{row["shares"]}</td>"""
        elif "- Removed" in row["company"]:
            html += f"""<td class="table-danger">+{-(row["prev_shares"])}</td>"""
        else:
            if row["shares_diff"] > 0:
                html += f"""<td class="table-success">+{row["shares_diff"]}</td>"""
            elif row["shares_diff"] < 0:
                html += f"""<td class="table-danger">{row["shares_diff"]}</td>"""
            else:
                html += f"""<td>{row["shares_diff"]}</td>"""

        if "- Added" in row["company"]:
            html += f"""<td class="table-success">+{row["value"]}</td>"""
        elif "- Removed" in row["company"]:
            html += f"""<td class="table-success">+{-(row["prev_value"])}</td>"""
        else:
            if row["value_diff"] == 0:
                html += f"""<td>{int(row["value_diff"])}</td>"""
            elif row["value_diff"] > 0:
                html += f"""<td class="table-success">+{int(row["value_diff"])}</td>"""
            elif row["value_diff"] < 0:
                html += f"""<td class="table-danger">{int(row["value_diff"])}</td>"""
            else:
                html += f"""<td>{row["value_diff"]}</td>"""

        if "- Added" in row["company"]:
            html += f"""<td class="table-success">+{row["weight"]}</td>"""
        elif "- Removed" in row["company"]:
            html += f"""<td class="table-success">+{-(row["prev_weight"])}</td>"""        
        else:
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
            </table>
        </div>
    </div>
    """

    return html