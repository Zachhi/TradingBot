# Trading Bot
This program uses an algorithm to automatically make trades for you using python and the QuantConnect platform

# Demo

![Demo](https://github.com/Zachhi/TradingBot/blob/master/botDemo.gif)

https://www.youtube.com/watch?v=99FonnBm1X8

# Strategy

***Breakout Strategy***
* Look at past highs of given instrument, if a breakout occurs, we buy
* Create a trailing stop loss behind it that rises with it, with an initial stop risk and trailing stop risk percentage
* If the market drops a certain amount, close the deal
* The stop loss helps protect against potential losses
* dynamically determine a lookback time frame which will help with deciding what defines a breakout
* The more change a market has, the farther the lookback
* The less change a market has, the shorter the lookback 
* This allows the algorithm to automatically adapt to changes in a market's volatility


# Usage

* Make a profile on https://www.quantconnect.com/
* Create a new python project and copy and paste `main.py` into the project
* Edit to the desired starting date->end date, the desired starting cash, and the desired markets under `def Initialize(self):`
* Build it and click `Backtest` to see the results (profit, where the bot bought/sold, etc.)
* Click `Go Live` if you wish to use real money or if you wish to paper trade

## Authors

Zachary Chi
zachchi@tamu.edu

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
