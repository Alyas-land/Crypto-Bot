# stop_loss_percent = 10 
# take_profit_percent = 20

def stable_str(df, stop_loss_percent, take_profit_percent):
    capital = 1000
    position = 0  # 0: no position, 1: holding BTC
    btc = 0
    buy_price = 0
    
    for i in range(len(df)):
        price = df.at[i, 'close']
    
        if position == 0:
            if df.at[i, 'signal'] == 1:
                # Buy
                btc = capital / price
                buy_price = price
                capital = 0
                position = 1
    
        elif position == 1:
            # بررسی استاپ‌لاس یا تیک‌پرافیت
            if price <= buy_price * (1 - stop_loss_percent / 100):
                # فعال شدن استاپ‌لاس
                capital = btc * price
                btc = 0
                position = 0
    
            elif price >= buy_price * (1 + take_profit_percent / 100):
                # فعال شدن تیک‌پرافیت
                capital = btc * price
                btc = 0
                position = 0
    
            elif df.at[i, 'signal'] == -1:
                # سیگنال فروش (عادی)
                capital = btc * price
                btc = 0
                position = 0
    
    
    if position == 1:
        capital = btc * df.iloc[-1]['close']
    
    