# =========================================================
# NATURAL GAS STORAGE CONTRACT PRICING DASHBOARD
# =========================================================
# Author  : Ritu Mahajan
# Project : Natural Gas Analytics & Storage Pricing
# =========================================================

# =========================================================
# IMPORT LIBRARIES
# =========================================================

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# =========================================================
# CREATE IMAGES FOLDER
# =========================================================

os.makedirs("images", exist_ok=True)

# =========================================================
# PRICE DATA
# =========================================================

price_data = {
    "2024-01-31": 10,
    "2024-02-29": 11,
    "2024-03-31": 12,
    "2024-04-30": 13,
    "2024-05-31": 14,
    "2024-06-30": 15,
    "2024-07-31": 16,
    "2024-08-31": 17,
}

# =========================================================
# CONVERT DATA TO DATAFRAME
# =========================================================

df = pd.DataFrame(
    list(price_data.items()),
    columns=["Date", "Price"]
)

df["Date"] = pd.to_datetime(df["Date"])

# =========================================================
# STORAGE CONTRACT PRICING FUNCTION
# =========================================================

def price_storage_contract(
    injection_dates,
    withdrawal_dates,
    injection_rate,
    withdrawal_rate,
    max_storage_volume,
    storage_cost_per_unit
):

    total_profit = 0
    current_storage = 0

    total_injection_cost = 0
    total_storage_cost = 0
    total_revenue = 0

    transaction_history = []

    print("\n================================================")
    print("NATURAL GAS STORAGE CONTRACT VALUATION")
    print("================================================\n")

    # =====================================================
    # INJECTION OPERATIONS
    # =====================================================

    for date in injection_dates:

        buy_price = price_data[date]

        injected_volume = min(
            injection_rate,
            max_storage_volume - current_storage
        )

        injection_cost = (
            buy_price * injected_volume
        )

        storage_cost = (
            storage_cost_per_unit * injected_volume
        )

        total_cost = (
            injection_cost + storage_cost
        )

        total_profit -= total_cost

        total_injection_cost += injection_cost
        total_storage_cost += storage_cost

        current_storage += injected_volume

        transaction_history.append({
            "Date": date,
            "Action": "Injection",
            "Price": buy_price,
            "Volume": injected_volume,
            "Cash Flow": -total_cost
        })

        print(f"Injected Gas on : {date}")
        print(f"Purchase Price  : ${buy_price}")
        print(f"Volume Injected : {injected_volume}")
        print(f"Storage Cost    : ${storage_cost}")
        print(f"Current Storage : {current_storage}")
        print()

    # =====================================================
    # WITHDRAWAL OPERATIONS
    # =====================================================

    for date in withdrawal_dates:

        sell_price = price_data[date]

        withdrawn_volume = min(
            withdrawal_rate,
            current_storage
        )

        revenue = (
            sell_price * withdrawn_volume
        )

        total_profit += revenue

        total_revenue += revenue

        current_storage -= withdrawn_volume

        transaction_history.append({
            "Date": date,
            "Action": "Withdrawal",
            "Price": sell_price,
            "Volume": withdrawn_volume,
            "Cash Flow": revenue
        })

        print(f"Withdrawn Gas on : {date}")
        print(f"Selling Price    : ${sell_price}")
        print(f"Volume Withdrawn : {withdrawn_volume}")
        print(f"Revenue Earned   : ${revenue}")
        print(f"Remaining Storage: {current_storage}")
        print()

    # =====================================================
    # FINAL RESULTS
    # =====================================================

    print("================================================")
    print("FINAL CONTRACT VALUATION")
    print("================================================\n")

    print(f"Final Profit/Loss : ${round(total_profit, 2)}")

    # =====================================================
    # SAVE TRANSACTION HISTORY
    # =====================================================

    history_df = pd.DataFrame(transaction_history)

    history_df.to_csv(
        "contract_transactions.csv",
        index=False
    )

    # =====================================================
    # CREATE PROFESSIONAL DASHBOARD
    # =====================================================

    fig = make_subplots(

        rows=1,
        cols=2,

        subplot_titles=(
            "Natural Gas Price Trend",
            "Financial Breakdown"
        ),

        specs=[
            [{"type": "scatter"}, {"type": "pie"}]
        ]
    )

    # =====================================================
    # MAIN PRICE TREND LINE
    # =====================================================

    fig.add_trace(

        go.Scatter(

            x=df["Date"],
            y=df["Price"],

            mode='lines+markers',

            name='Gas Prices',

            line=dict(width=4),

            marker=dict(size=10),

            hovertemplate=
            "<b>Date:</b> %{x}<br>" +
            "<b>Price:</b> $%{y}<extra></extra>"
        ),

        row=1,
        col=1
    )

    # =====================================================
    # INJECTION POINTS
    # =====================================================

    injection_x = [
        pd.to_datetime(date)
        for date in injection_dates
    ]

    injection_y = [
        price_data[date]
        for date in injection_dates
    ]

    fig.add_trace(

        go.Scatter(

            x=injection_x,
            y=injection_y,

            mode='markers+text',

            text=["BUY"] * len(injection_x),

            textposition="top center",

            name='Injection',

            marker=dict(
                size=18,
                symbol='triangle-up'
            ),

            hovertemplate=
            "<b>Injection:</b><br>" +
            "Date: %{x}<br>" +
            "Price: $%{y}<extra></extra>"
        ),

        row=1,
        col=1
    )

    # =====================================================
    # WITHDRAWAL POINTS
    # =====================================================

    withdrawal_x = [
        pd.to_datetime(date)
        for date in withdrawal_dates
    ]

    withdrawal_y = [
        price_data[date]
        for date in withdrawal_dates
    ]

    fig.add_trace(

        go.Scatter(

            x=withdrawal_x,
            y=withdrawal_y,

            mode='markers+text',

            text=["SELL"] * len(withdrawal_x),

            textposition="bottom center",

            name='Withdrawal',

            marker=dict(
                size=18,
                symbol='triangle-down'
            ),

            hovertemplate=
            "<b>Withdrawal:</b><br>" +
            "Date: %{x}<br>" +
            "Price: $%{y}<extra></extra>"
        ),

        row=1,
        col=1
    )

    # =====================================================
    # PIE CHART
    # =====================================================

    fig.add_trace(

        go.Pie(

            labels=[
                "Revenue",
                "Injection Cost",
                "Storage Cost"
            ],

            values=[
                total_revenue,
                total_injection_cost,
                total_storage_cost
            ],

            hole=0.45,

            textinfo='label+percent',

            hovertemplate=
            "<b>%{label}</b><br>" +
            "Value: $%{value}<extra></extra>"
        ),

        row=1,
        col=2
    )

    # =====================================================
    # DASHBOARD LAYOUT
    # =====================================================

    fig.update_layout(

        title={
            'text':
            "Natural Gas Storage Contract Analysis Dashboard",
            'x': 0.5
        },

        template="plotly_dark",

        height=700,

        width=1400,

        font=dict(size=13),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),

        annotations=[

            dict(

                text=
                f"<b>Total Profit:</b> ${round(total_profit, 2)}",

                showarrow=False,

                x=0.5,
                y=-0.12,

                xref="paper",
                yref="paper",

                font=dict(
                    size=18
                )
            )
        ]
    )

    # =====================================================
    # SAVE DASHBOARD
    # =====================================================

    fig.write_html(
        "images/storage_dashboard.html"
    )

    # =====================================================
    # SHOW DASHBOARD
    # =====================================================

    fig.show()

    # =====================================================
    # RETURN FINAL PROFIT
    # =====================================================

    return round(total_profit, 2)

# =========================================================
# SAMPLE TEST CASE
# =========================================================

contract_value = price_storage_contract(

    injection_dates=[
        "2024-01-31",
        "2024-02-29"
    ],

    withdrawal_dates=[
        "2024-07-31",
        "2024-08-31"
    ],

    injection_rate=1000,

    withdrawal_rate=1000,

    max_storage_volume=2000,

    storage_cost_per_unit=0.5
)

# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n================================================")
print("PROJECT COMPLETED SUCCESSFULLY")
print("================================================\n")

print(f"Calculated Contract Value : ${contract_value}")

print("\nGenerated Files:")

print("1. contract_transactions.csv")
print("2. images/storage_dashboard.html")

print("\nSystem Features:")
print("- Interactive professional dashboard")
print("- Dynamic hover values")
print("- BUY/SELL indicators")
print("- Financial pie chart")
print("- Cash flow analysis")
print("- Storage tracking")
print("- HTML interactive visualization")
print("- CSV export")