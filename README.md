# TASK 1: Natural Gas Price Estimation for Arbitrage
- As a quantitative researcher for JP Morgan Chase & Co., I was given a task where I learn that the current process is to take a monthly snapshot of prices from a 
market data provider, which represents the market price of natural gas delivered at the end of each calendar month.

- I have to use this monthly snapshot data to produce a varying picture of the existing price data, as well as an extrapolation for an extra year, in case the client needs an 
indicative price for a longer-term storage contract.


- The main file which the model's script I built on is "Task1 (Final Code).py".
- In the "Task1 (Final Code).py" file, I used libraries like pandas and numpy to work this task out along side the library of matplotlib to visualize.
- In this file, I build a trendline (using np.polyfit) which represents the trend of prices from month to month from 2020 to 2024 with a slope m (representing how on average
the price's trend increased over time).
- I also build a variable named as "monthly_average_deviation" which measures the seasonal deviation of prices from month to month from the trendline and the model uses it to adjust accordingly
to predict the extrapolation and estimation of input date by any user.

# USAGE
This script prompts the user to input a reference date where the whole model takes this date as an input (in MM/DD/YY format) and then estimates the price value at the reference
date and also estimates (forcasts) the value of the price one year forward to the reference input entered by the user.

# TASK 2: Price a Commodity Storage Contract
- The client wants to start trading as soon as possible. They believe the winter will be colder than expected, so they want to buy gas now to store and sell in winter in order to take advantage of the resulting increase in gas prices. They ask me to write a script that they can use to price the contract.
- I have to create a prototype pricing model that can go through further validation and testing before being put into production. this model may be the basis for fully automated quoting to clients, but for now, the desk will use it with manual oversight to explore options with the client.
- I wrote the python code for this model in the "Task2.py" file, where the client can enter his inputs (multiple inputs) as follows:
(1) Injection dates,
(2) Withdrawal dates,
(3) The prices at which the commodity can be purchased/sold on those dates,
(4) The rate at which the gas can be injected/withdrawn,
(5) The maximum volume that can be stored,
(6) Storage costs.

and it calculates the final value of the contract according to the plans of client.
