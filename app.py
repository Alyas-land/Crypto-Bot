import pandas as pd
from rsi import RSI
from backtest import simple_backtest, backtest_stable_tf_stoploss, backtest_with_dynamic_stoploss
from colorama import init, Fore

init()
green = Fore.GREEN
red = Fore.RED
cyan = Fore.CYAN
yellow = Fore.YELLOW
reset = Fore.RESET


#read dataset
print(f'{cyan} Reading Dataset File {reset}')
df = pd.read_excel("dataset/btc_binance.xlsx")
print(f'{green} Reading Dataset File SuccessFulled {reset}')


# preprocess
print(f'{cyan} Start Preprocess {reset}')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp')

# RSI 
print(f'{cyan} Run RSI Method {reset}')
data_frame_rsi = RSI(df)


# Add sell and buy signal
print(f'{cyan} Set Signal For Selling And Buying {reset}')
df['signal'] = 0
df.loc[(data_frame_rsi > 30) & (data_frame_rsi.shift(1) <= 30), 'signal'] = 1  # buy
df.loc[(data_frame_rsi < 70) & (data_frame_rsi.shift(1) >= 70), 'signal'] = -1 # sell

#select strategy
strategy = None
while(strategy != 0):
    #select strategy
    strategy = int(input(f'''{yellow}Select strategy:
        1 - with 30-70 strategy
        2 - stable strategy
        3 - dynamic
        0 - exit
        Your choice: '''))
    
    if strategy == 1:
        print(f'{cyan}\n Strategy : with 30-70 strategy {reset}')
        print(f'{cyan} Start Backtest Method {reset}')
        result = simple_backtest(df=df)
        print(f'{green} Simple Backtest Completed Successfully. {reset}')
        print(f'{red}Final Money:'+ str(round(result, 2))+ f"${reset}\n")

    elif strategy == 2:
        # Get stopless and take Profill from user
        print(f'{cyan}\n Strategy : Stable stoploss and tp strategy {reset}')
        stable_stoploss_percent = int(input(f'{green}Please Enter Stopless Percent:{reset}')) 
        take_profill_percent = int(input(f'{green}Please Enter TP Percent:{reset} '))
        print(f'{cyan} Start Backtest Method {reset}')
        result = backtest_stable_tf_stoploss(df=df, stop_loss_percent=stable_stoploss_percent, take_profit_percent=take_profill_percent)
        print(f'{green} Stable Strategy Backtest Completed Successfully. {reset}\n')
        print(f'{red}Final Money:'+ str(round(result, 2))+ f"${reset}\n")

    elif strategy == 3:
        print(f'{cyan}\n Strategy : Dynamic stoploss and tp strategy {reset}')
        # Get dynamic stopless and take Profill
        dynamic_stoploss_percent = int(input(f'{green}Please Enter Dynamic Stopless Percent:{reset}')) 
        take_profill_percent = int(input(f'{green}Please Enter TP Percent:{reset} '))

        # Backtesting
        print(f'{cyan} Start Backtest Method {reset}')
        backtest = backtest_with_dynamic_stoploss(df=df, dynamic_stoploss=dynamic_stoploss_percent, take_profit=take_profill_percent)
        print(f'{green} Backtest Completed Successfully. {reset}\n')
        print(f'{red}Final Money:'+ str(round(backtest, 2))+ f"${reset}")

    elif strategy == 0:
        exit()





