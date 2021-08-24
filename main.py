import numpy as np

#strategy - simple breakout
#breakout -> buy
#trailing stop loss
#drop a certain amount -> close

#use a certain lookback time frame to determine when breakout is
#if a stock has more change, time frame will be higher
#if a stock has relatively low change, time frame will be shorter
#gives us a dynamic approach

class StockAlgo(QCAlgorithm):
    
    #init parameters, variables, etc.
    def Initialize(self): 
    
        self.lookback = 10 #in days. Doesnt matter here it will change below
        self.ceiling, self.floor = 50, 10 #set limits for lookback
        
        self.SetStartDate(2020,1,1) # beginning of year -> now for backtesting
        self.SetEndDate(2020,8,22)
        
        self.SetCash(500000)        # $500,000 for backtesting
        
        self.symbol = self.AddEquity("SPY", Resolution.Daily).Symbol #using daily data. SPY tracks S&P 500

        self.initialStopRisk = 0.97 #allows 3% before stop order
        self.trailingStopRisk = 0.95
        

        # schedule for daily, after 10 minutes of market being open, using function everymarketopen
        self.Schedule.On(self.DateRules.EveryDay(self.symbol), self.TimeRules.AfterMarketOpen(self.symbol, 10), Action(self.EveryMarketOpen))
                        
    def OnData(self, data):
        self.Plot("Data Chart", self.symbol, self.Securities[self.symbol].Close) #plot on data

    def EveryMarketOpen(self):
        #here, we determine the lookback length, using volatility change on 30 days
        C = self.History(self.symbol, 31, Resolution.Daily)["close"]
        
        todayVolatility = np.std(C[1:31]) #todays volatility change rate
        yesterdayVolatility = np.std(C[0:30]) #ydays volatility chane rate
        deltaVolatility = (todayVolatility - yesterdayVolatility) / todayVolatility #dynamically determining lookback length
        self.lookback = round(self.lookback * (1 + deltaVolatility)) 
        
        if self.lookback > self.ceiling:
            self.lookback = self.ceiling #set lookback to max if above max
        elif self.lookback < self.floor:
            self.lookback = self.floor #set lookback to min if below min
        
        # Retrieve list of daily highs so we can know when to buy
        self.high = self.History(self.symbol, self.lookback, Resolution.Daily)["high"]
        
        # using that list and lookback, we can now buy incase of breakout
        
        #not invested and breakout has occured
        if not self.Securities[self.symbol].Invested and self.Securities[self.symbol].Close >= max(self.high[:-1]): 
            self.SetHoldings(self.symbol, 1) #buy it
            self.breakoutlvl = max(self.high[:-1])
            self.highestPrice = self.breakoutlvl #new highest price
        
        #if invested, created trailing stop loss
        if self.Securities[self.symbol].Invested:
            
            # If no order exists
            if not self.Transactions.GetOpenOrders(self.symbol):
                #stop loss
                self.stopMarketTicket = self.StopMarketOrder(self.symbol, -self.Portfolio[self.symbol].Quantity, self.initialStopRisk * self.breakoutlvl)
                                        
                                        
            # if price higher than current highestPrice AND initial stop price < trailing stop price
            if self.Securities[self.symbol].Close > self.highestPrice and self.initialStopRisk * self.breakoutlvl < self.Securities[self.symbol].Close * self.trailingStopRisk:
                self.highestPrice = self.Securities[self.symbol].Close  #update highest price
                
                updateFields = UpdateOrderFields()  # Update stop price
                updateFields.StopPrice = self.Securities[self.symbol].Close * self.trailingStopRisk
                self.stopMarketTicket.Update(updateFields)
                
                self.Debug(updateFields.StopPrice) # Print new stop price
             
            self.Plot("Data Chart", "Stop Price", self.stopMarketTicket.Get(OrderField.StopPrice))  # plot trailing stop