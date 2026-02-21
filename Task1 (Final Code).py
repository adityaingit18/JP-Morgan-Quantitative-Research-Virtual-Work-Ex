import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Framing data
data = pd.read_csv("Nat_Gas.csv")
df = pd.DataFrame(data)
df['Dates'] = pd.to_datetime(df['Dates'], format="%m/%d/%y")

# Month and date extraction
df['Month'] = df['Dates'].dt.month
date_given = df["Dates"].map(pd.Timestamp.toordinal)
price_given = df["Prices"]

# Trendline
m, c = np.polyfit(date_given, price_given, 1)

# Deviation of actual price from trendline
df['Linear_Price'] = (m * date_given) + c
df['Deviation'] = df['Prices'] - df['Linear_Price']
monthly_average_deviation = df.groupby('Month')['Deviation'].mean() # Average Deviation / Month

# User input
user_input_date = input("Enter a reference date (MM/DD/YY): ")

input_date = pd.to_datetime(user_input_date, format="%m/%d/%y")

# Estimating price on user input's date
input_month = input_date.month
input_date_ord = input_date.toordinal()
current_price = (m * input_date_ord) + c + monthly_average_deviation[input_month]

# Extrapolating of purchase price one year into future
target_date = input_date + pd.DateOffset(years=1)
target_month = target_date.month
target_date_ord = target_date.toordinal()
target_price = (m * target_date_ord) + c + monthly_average_deviation[target_month]

# Outputs
print(f"\nReference date provided: {input_date.date()}")
print(f"1. Estimated price on the reference date: ${current_price:.2f}")
print(f"2. Estimated price 1 year forward ({target_date.date()}): ${target_price:.2f}")

plt.figure(figsize=(10, 6)) # Make the chart a bit wider to see the future clearly
plt.plot(df['Dates'], df['Prices'], label='Historical Prices', marker='o')
plt.plot(df['Dates'], df['Linear_Price'], label='Linear Trend', linestyle='--')

# Plotting for visualization
plt.scatter([input_date], [current_price], color='blue', zorder=5, s=100, label=f'Current Est: ${current_price:.2f}')
plt.scatter([target_date], [target_price], color='red', zorder=5, s=100, label=f'1-Year Est: ${target_price:.2f}')

plt.title('Natural Gas Prices: Current & 1-Year Extrapolation')
plt.xlabel('Date')
plt.ylabel('Price in USD')
plt.legend()
plt.grid(True)
plt.show()