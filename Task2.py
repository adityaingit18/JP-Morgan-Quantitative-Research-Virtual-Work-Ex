import pandas as pd
import numpy as np
from datetime import datetime

# Estimating Price - Model from Task 1
data = pd.read_csv("Nat_Gas.csv")
df = pd.DataFrame(data)
df["Dates"] = pd.to_datetime(df["Dates"],format = "%m/%d/%y")
df["Month"] = df["Dates"].dt.month
date_given = df["Dates"].map(pd.Timestamp.toordinal)
price_given = df["Prices"]

# Calculating the linear trendline of prices
m, c = np.polyfit(date_given,price_given,1)
df["Linear Price"] = (m * date_given) + c 

# Calculation of deviation from Linear Trendline of prices in Task - 1
df["Deviation"] = df["Prices"] - df["Linear Price"]
monthly_average_deviation = df.groupby('Month')['Deviation'].mean() # Average Deviation of Prices (Month to Month)


def get_estimated_price(date_as_string):
    target_date = pd.to_datetime(date_as_string, format = "%m/%d/%y")
    target_date_ord = target_date.toordinal()
    target_month = target_date.month

    estimate_of_price = (m * target_date_ord) + c + monthly_average_deviation[target_month]
    return estimate_of_price


# Building the Calculator to estimate the Contract Value
def contract_value_calculator(schedule,max_volume,max_rate):

    # Storage Fees
    pump_fee = 10000/1000000 # $10K per Million MMBtu
    transport_fee = 50000.00 # Flat Fee per trip
    monthly_rent = 100000 # Flat Rent to be paid per month of storing gas

    ledger = 0.0
    inventory = 0.0
    last_date = None

    # Client's date schedule arranged chronologically
    schedule.sort(key=lambda x: pd.to_datetime(x["Date"], format="%m/%d/%y"))

    for entry in schedule:
        current_date = pd.to_datetime(entry["Date"], format="%m/%d/%y")
        action = entry["Action"].lower()
        volume = entry["Volume"]

        # Physical Limits of Storage
        if volume > max_rate:
            print(f"ERROR: Cannot move {volume} MMBtu becuase it exceeds the maximum rate of {max_rate}. Trade rejected is rejected!!!")
            continue

        # Calculation of storage rent to be paid
        if last_date is not None and inventory > 0:
            months_stored = (current_date - last_date).days / 30.416 # 30.416 is the average days per month in a year (365/12 = 30.416)
            rent_cost = monthly_rent * months_stored
            ledger -= rent_cost
            print(f"[{current_date.date()}] Storage: Paid ${rent_cost:,.2f} rent for {months_stored:.2f} months.")

        # Getting the market price of Natural Gas
        current_price = get_estimated_price(entry["Date"])

        # Cash-Flows
        if action == "inject":
            if inventory + volume > max_volume:
                print(f"Tank is full! Cannot inject {volume} MMBtu.")
                continue
        
            gas_cost = current_price * volume
            pump_cost = pump_fee * volume

            ledger = ledger - gas_cost - pump_cost - transport_fee
            inventory += volume
            print(f"[On {current_date.date()}], Injection : Bought {volume:,.0f} units of Natural Gas @ ${current_price:.2f}, Paid ${transport_fee:,.0f} as transport fee & ${pump_cost:,.0f} as total pumping cost")

        elif action == "withdraw":
            if inventory < volume:
                print(f"Tank is empty! Cannot withdraw {volume} MMBtu.")
                continue

            gas_revenue = current_price * volume
            pump_cost = pump_fee * volume

            ledger = ledger + gas_revenue - pump_cost - transport_fee
            inventory -= volume
            print(f"[On {current_date.date()}], Withdrawal : Sold {volume:,.0f} units of Natural Gas @ ${current_price:.2f}, Paid ${transport_fee:,.0f} as transport fee & ${pump_cost:,.0f} as total pumping cost")
        
        last_date = current_date
        print(f"Contract Value: ${ledger:,.2f} | Current Inventory: {inventory:,.0f} MMBtu\n")

    return ledger

# Client's Input Work

client_schedule = []

while True:
    date_input = input("Enter Date (MM/DD/YY) or type 'stop': ")

    if date_input.lower() == 'stop':
        break

    action_input = input("Enter Action (Inject/Withdraw): ")
    volume_input = float(input("Volume of Natural Gas you want to move: "))

    row_entry = {
        "Date": date_input,
        "Action": action_input,
        "Volume": volume_input
    }

    client_schedule.append(row_entry)
    print("Client's Input recorded.\n")

# An Example:
Maximum_Storage_Capacity = 2000000 # Tank at max, can hold 2 million MMBtu of Gas
Maximum_Transfer_Rate = 1500000 # Tank at max can pump in/out 1.5 million MMBtu of Gas


# Executing the model only if client enters any input, else the contract didn't take place
if len(client_schedule) > 0:
    final_profit = contract_value_calculator(client_schedule, Maximum_Storage_Capacity, Maximum_Transfer_Rate)

    print(f"Final Contract Value: ${final_profit:,.2f}")
else:
    print("No trades were entered. Contract value is $0.00")