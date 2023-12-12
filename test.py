import yfinance as yf
import matplotlib.pyplot as plt

class Signal:
    def __init__(self, balance,cnst_blnc):
        self.states = ['buy', 'sell', 'none']
        self.state = 'none'
        self.balance = balance
        self.lotsize = None
        # Get Initial Balance as a Constant For Profit Loss Calculation Difference
        self.cnst_blnc = cnst_blnc
        # Holder is Used to Store the Profit Loss Data 
        self.holder = 0
        # Holder2 is Used for storing Updated Balance (If Used the self.balance instead the P&L Ratio gets Affected Poorly)
        self.holder2 = cnst_blnc
    
    def buy_order(self, price_buy):
        if self.state == 'none' or self.state == 'sell':
            print('Bought at: {:.2f}'.format(price_buy))
            self.state = 'buy'
            self.lotsize = self.balance // price_buy
            print('Lot Size:', int(self.lotsize))
            self.holder2 = self.balance - self.lotsize * price_buy

        else:
            None

    def sell_order(self, price_sell):
        if self.state == 'buy':
            print('Sold at: {:.2f}'.format(price_sell))
            self.state = 'sell'
            self.balance = self.holder2 + self.lotsize * price_sell
            self.holder = self.balance - self.cnst_blnc
            print('Balance: {:.2f}'.format(self.balance))
            print("P&L = {:.2f}".format(self.holder))
            print('\n')

        else:
            None

    def get_state(self):
        return self.state

    def get_balance(self):
        return self.balance

    def get_cnst_blnc(self):
        return self.holder


initial_balance = 10000
int_blc2 = initial_balance
pnl = []
signal = Signal(balance=initial_balance, cnst_blnc=int_blc2)
symbol = "ANSGR.IS"
start_date = "2022-01-01"
end_date = "2023-01-01"
sma1 = 8
sma2 = 21
balance_data = []

data = yf.download(symbol, start=start_date, end=end_date)

data['SMA1'] = data['Adj Close'].rolling(window=sma1).mean()
data['SMA2'] = data['Adj Close'].rolling(window=sma2).mean()


for i in range(len(data)):
    if data['SMA1'].iloc[i] > data['SMA2'].iloc[i]:
        signal.buy_order(data['Adj Close'].iloc[i])

    elif data['SMA1'].iloc[i] < data['SMA2'].iloc[i]:
        signal.sell_order(data['Adj Close'].iloc[i])

    balance_data.append(signal.get_balance())
    pnl.append(signal.get_cnst_blnc())

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

ax3.plot(data.index, pnl, label='P&L', linewidth=2, color='red')
ax3.set_xlabel('Date')
ax3.set_ylabel('P&L (USD)')
ax3.legend()

plt.show()


