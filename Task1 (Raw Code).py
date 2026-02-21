import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("Nat_Gas.csv")
df = pd.DataFrame(data)

df['Dates'] = pd.to_datetime(df['Dates'], format = "%m/%d/%y")

date_given = df["Dates"].map(pd.Timestamp.toordinal)
price_given = df["Prices"]

m, c = np.polyfit(date_given,price_given,1)


user_input_date = input("Enter a reference date (MM/DD/YY): ")

input_date = pd.to_datetime(user_input_date, format = "%m/%d/%y")

next_date = input_date + pd.DateOffset(years=1)

next_date_ord = next_date.toordinal()

next_price = (m * next_date_ord) + c

print(f"\nReference date provided: {input_date.date()}")
print(f"The estimated price on {next_date.date()}: ${next_price : .2f}")