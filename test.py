import yfinance as yf
import matplotlib.pyplot as plt

class Signal:
    def __init__(self, balance):
        self.states = ['buy', 'sell', 'none']
        self.state = 'none'
        self.balance = balance
        self.lotsize = None
    
    def buy_order(self, price_buy):
        if self.state == 'none' or self.state == 'sell':
            print('Bought at: {:.2f}'.format(price_buy))
            self.state = 'buy'
            self.lotsize = self.balance // price_buy
            print('Lot Size:', int(self.lotsize))
            # rest = self.balance - lotsize * price_buy
            self.balance = self.balance - self.lotsize * price_buy

        else:
            None

    def sell_order(self, price_sell):
        if self.state == 'buy':
            print('Sold at: {:.2f}'.format(price_sell))
            self.state = 'sell'
            self.balance = self.balance + self.lotsize * price_sell
            print('Balance: {:.2f}'.format(self.balance))
            print('\n')

        else:
            None

    def get_state(self):
        return self.state

    def get_balance(self):
        return self.balance

initial_balance = 10000
signal = Signal(balance=initial_balance)
symbol = "ANSGR.IS"
start_date = "2022-01-01"
end_date = "2023-01-01"
sma1 = 8
sma2 = 21

data = yf.download(symbol, start=start_date, end=end_date)
# close_price = data['Adj Close']
# print(close_price)

data['SMA1'] = data['Adj Close'].rolling(window=sma1).mean()
data['SMA2'] = data['Adj Close'].rolling(window=sma2).mean()


for i in range(len(data)):
    if data['SMA1'].iloc[i] > data['SMA2'].iloc[i]:
        signal.buy_order(data['Adj Close'].iloc[i])

    elif data['SMA1'].iloc[i] < data['SMA2'].iloc[i]:
        signal.sell_order(data['Adj Close'].iloc[i])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

ax1.plot(data['Adj Close'], label = symbol + ' Price', linewidth=3)
ax1.plot(data['SMA1'], label=f'{sma1} Day Moving Average', color='green')
ax1.plot(data['SMA2'], label=f'{sma2} Day Moving Average', color='purple')
ax1.set_title(f'{symbol} Stock Price With Moving Averages')
ax1.set_ylabel('Price (USD)')
ax1.legend()

# balance_data = [initial_balance - signal.get_balance() for _ in range(len(data))]
for _ in range(len(data)):
    print(signal.get_balance())
# print(signal.get_balance())
# ax2.plot(data.index, balance_data, label='Balance', linewidth=2, color='red')
ax2.set_xlabel('Date')
ax2.set_ylabel('Balance (USD)')
ax1.legend()

plt.show()




# plt.figure(figsize=(10, 6))
# plt.plot(data['Adj Close'], label=symbol + ' Price', linewidth=3)
# plt.plot(data['SMA1'], label=f'{sma1} Day Moving Average', color='green')
# plt.plot(data['SMA2'], label=f'{sma2} Day Moving Average', color='red')
# plt.title(f'{symbol} Stock Price With Moving Averages')
# plt.xlabel('Date')
# plt.ylabel('Price (USD)')
# plt.legend()
#
# plt.show()
