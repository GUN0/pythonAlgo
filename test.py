import yfinance as yf
import matplotlib.pyplot as plt
import pandas

class Signal:
    def __init__(self, balance, stock_data):
        self.states = ['buy', 'sell', 'none']
        self.state = 'none'
        self.stock_data = stock_data
        self.balance = balance
        self.lotsize = 0
        # Initial Balance is Used as a Constant For Calculating Final Balance
        # Cannot Use self.balance Only Because The Balance Graph Goes to 0 When Buy Order Happens Because Using Whole Balance When Buying
        self.initial_balance = balance 
        self.pnl = 0
    
    def buy_order(self, price_buy):
        if self.state == 'none' or self.state == 'sell':
            print('Bought at: {:.2f}'.format(price_buy))
            self.state = 'buy'
            self.lotsize = self.balance // price_buy
            print('Lot Size:', int(self.lotsize))
            self.initial_balance = self.balance - self.lotsize * price_buy
            self.buy_price = price_buy

    def sell_order(self, price_sell):
        if self.state == 'buy':
            print('Sold at: {:.2f}'.format(price_sell))
            self.state = 'sell'
            self.balance = self.initial_balance + self.lotsize * price_sell
            self.pnl = (self.lotsize * price_sell) - (self.lotsize * self.buy_price)
            print('Balance: {:.2f}'.format(self.balance))
            print("P&L = {:.2f}".format(self.pnl))
            print('\n')

    def rsi(self, period):
        close_diff = self.stock_data['Adj Close'].diff()
        initial_average_gain = close_diff.clip(lower=0)
        initial_average_lose = -1 * close_diff.clip(upper=0)
        average_gain = initial_average_gain.rolling(window=period).mean()
        average_lose = initial_average_lose.rolling(window=period).mean()

        rs = average_gain / average_lose
        rsi = 100 - (100 / (1 + rs))

        return rsi



    def get_state(self):
        return self.state

    def get_balance(self):
        return self.balance

    def get_pnl(self):
        return self.pnl


initial_balance = 10000
pnl = []
symbol = "ANSGR.IS"
start_date = "2022-01-01"
end_date = "2023-01-01"
sma1 = 8
sma2 = 21
balance_data = []
stock_data = []
rsi = 0
data = yf.download(symbol, start=start_date, end=end_date)
signal = Signal(balance=initial_balance, stock_data=data)

data['SMA1'] = data['Adj Close'].rolling(window=sma1).mean()
data['SMA2'] = data['Adj Close'].rolling(window=sma2).mean()


for i in range(len(data)):
    if data['SMA1'].iloc[i] > data['SMA2'].iloc[i]:
        signal.buy_order(data['Adj Close'].iloc[i])

    elif data['SMA1'].iloc[i] < data['SMA2'].iloc[i]:
        signal.sell_order(data['Adj Close'].iloc[i])

    balance_data.append(signal.get_balance())
    pnl.append(signal.get_pnl())
    rsi = signal.rsi(14)
    

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

ax1.plot(data['Adj Close'], label = symbol + ' Price', linewidth=3)
ax1.plot(data['SMA1'], label=f'{sma1} Day Moving Average', color='green')
ax1.plot(data['SMA2'], label=f'{sma2} Day Moving Average', color='purple')
ax1.set_title(f'{symbol} Stock Price With Moving Averages')
ax1.set_ylabel('Price (USD)')
ax1.legend()

ax2.plot(data.index, balance_data, label='Balance', linewidth=2, color='red')
ax2.set_xlabel('Date')
ax2.set_ylabel('Balance (USD)')
ax2.legend()

# ax3.plot(data.index, pnl, label='P&L', linewidth=2, color='red')
# ax3.set_xlabel('Date')
# ax3.set_ylabel('P&L (USD)')
# ax3.legend()

ax3.plot(data.index, rsi, label='RSI', linewidth=2, color='orange')
ax3.set_xlabel('Date')
ax3.set_ylabel('RSI Data')
ax3.legend()

plt.show()


