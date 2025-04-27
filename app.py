import pandas as pd
from rsi import RSI
from backtest import back_test
from colorama import init, Fore
init()
#green
green = Fore.GREEN
#red
red = Fore.RED
#blue
cyan = Fore.CYAN
#reset
reset = Fore.RESET


#read dataset
print(f'{cyan} Reading Dataset File {reset}')
df = pd.read_excel("dataset/btc_binance.xlsx")
print(f'{green} Reading Dataset File is SuccessFulled {reset}\n')


# preprocess
print(f'{cyan} Start Preprocess {reset}\n')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp')

# RSI 
print(f'{cyan} Run RSI Method {reset}\n')
data_frame_rsi = RSI(df)


# Add sell and buy signal
print(f'{cyan} Set Signal For Selling And Buying {reset}\n')
df['signal'] = 0
df.loc[(data_frame_rsi < 30) & (data_frame_rsi.shift(1) >= 30), 'signal'] = 1  # buy
df.loc[(data_frame_rsi > 70) & (data_frame_rsi.shift(1) <= 70), 'signal'] = -1 # sell

# Set stopless and take Profill
dynamic_stoploss_percent = int(input(f'{green}Please Enter Stopless Percent:{reset}')) 
take_profill_percent = int(input(f'{green}Please Enter TP Percent:{reset} '))

# Backtesting
print(f'{cyan} Start Backtest Method {reset}')
backtest = back_test(df=df, dynamic_stoploss=dynamic_stoploss_percent, take_profit=take_profill_percent)
print(f'{green} Backtest Completed Successfully. {reset}\n')




print(f'{red}Final Money:'+ str(round(backtest, 2))+ f"${reset}")

