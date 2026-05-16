# =========================================================
# NATURAL GAS STORAGE CONTRACT PRICING SYSTEM
# =========================================================
# Author  : Ritu Mahajan
# Project : Natural Gas Analytics & Storage Pricing
# =========================================================

# -----------------------------
# IMPORT LIBRARIES
# -----------------------------

import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# CREATE IMAGES FOLDER
# -----------------------------

os.makedirs("images", exist_ok=True)

# -----------------------------
# PRICE DATA
# -----------------------------

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

# -----------------------------
# CONVERT TO DATAFRAME
# -----------------------------

df = pd.DataFrame(
    list(price_data.items()),
    columns=["Date", "Price"]
)

df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# STORAGE CONTRACT FUNCTION
# -----------------------------

def price_storage_contract(
    injection_dates,
    withdrawal_dates,
    injection_rate,
    withdrawal_rate,
    max_storage_volume,
    storage_cost_per_unit
):

    """
    Calculate storage contract value
    """

    total_profit = 0
    current_storage = 0

    transaction_history = []

    print("\n================================================")
    print("NATURAL GAS STORAGE CONTRACT VALUATION")
    print("================================================\n")

    # ====================================================
    # INJECTION OPERATIONS
    # ====================================================

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

    # ====================================================
    # WITHDRAWAL OPERATIONS
    # ====================================================

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

    # ====================================================
    # FINAL RESULTS
    # ====================================================

    print("================================================")
    print("FINAL CONTRACT VALUATION")
    print("================================================\n")

    print(f"Final Profit/Loss : ${round(total_profit, 2)}")

    # ====================================================
    # SAVE TRANSACTION HISTORY
    # ====================================================

    history_df = pd.DataFrame(transaction_history)

    history_df.to_csv(
        "contract_transactions.csv",
        index=False
    )

    # ====================================================
    # VISUALIZATION
    # ====================================================

    plt.figure(figsize=(14, 6))

    # Historical Prices
    plt.plot(
        df["Date"],
        df["Price"],
        marker='o',
        linewidth=2,
        label="Natural Gas Prices"
    )

    # Injection Points
    injection_x = [
        pd.to_datetime(date)
        for date in injection_dates
    ]

    injection_y = [
        price_data[date]
        for date in injection_dates
    ]

    plt.scatter(
        injection_x,
        injection_y,
        s=120,
        marker='^',
        label="Injection Points"
    )

    # Withdrawal Points
    withdrawal_x = [
        pd.to_datetime(date)
        for date in withdrawal_dates
    ]

    withdrawal_y = [
        price_data[date]
        for date in withdrawal_dates
    ]

    plt.scatter(
        withdrawal_x,
        withdrawal_y,
        s=120,
        marker='v',
        label="Withdrawal Points"
    )

    plt.title(
        "Natural Gas Storage Contract Analysis",
        fontsize=16
    )

    plt.xlabel("Date", fontsize=12)

    plt.ylabel("Natural Gas Price", fontsize=12)

    plt.legend()

    plt.grid(True)

    # Save Graph
    plt.savefig(
        "images/storage_contract_analysis.png",
        dpi=300,
        bbox_inches='tight'
    )

    plt.show()

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

print("2. images/storage_contract_analysis.png")

print("\nSystem Features:")
print("- Contract valuation")
print("- Cash flow analysis")
print("- Storage tracking")
print("- Graph visualization")
print("- CSV export")