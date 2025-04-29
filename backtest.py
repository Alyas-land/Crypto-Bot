def simple_backtest(df):
    capital = 1000
    position = 0
    btc = 0
    for i in range(len(df)):
        if df.at[i, 'signal'] == 1 and position == 0:
            btc = capital / df.at[i, 'close']
            capital = 0
            position = 1
        elif df.at[i, 'signal'] == -1 and position == 1:
            capital = btc * df.at[i, 'close']
            btc = 0
            position = 0

    if position == 1:
        capital = btc * df.iloc[-1]['close']

    return capital

def backtest_stable_tf_stoploss(df, stop_loss_percent, take_profit_percent):
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
            # check stoploss / tf
            if price <= buy_price * (1 - stop_loss_percent / 100):
                # active stoploss
                capital = btc * price
                btc = 0
                position = 0
    
            elif price >= buy_price * (1 + take_profit_percent / 100):
                # active tf
                capital = btc * price
                btc = 0
                position = 0
    
            elif df.at[i, 'signal'] == -1:
                # buy signal
                capital = btc * price
                btc = 0
                position = 0
    
    
    if position == 1:
        capital = btc * df.iloc[-1]['close']
    
    return capital

def backtest_with_dynamic_stoploss(df, dynamic_stoploss, take_profit):
    capital = 1000
    position = 0
    btc = 0
    buy_price = 0
    dynamic_stop_price = 0
    take_profit_price = 0

    for i in range(len(df)):
        price = df.at[i, 'close']

        if position == 0:
            if df.at[i, 'signal'] == 1:
                # Buy
                btc = capital / price
                buy_price = price
                dynamic_stop_price = price * (1 - dynamic_stoploss / 100)
                take_profit_price = price * (1 + dynamic_stoploss / 100)
                capital = 0
                position = 1

        elif position == 1:
            # stoploss update if range big than a go
            new_stop = price * (1 - dynamic_stoploss / 100)
            if new_stop > dynamic_stop_price:
                dynamic_stop_price = new_stop

            # CHeck stoploss and take profill
            if price >= take_profit_price:
                # Actived take profill
                capital = btc * price
                btc = 0
                position = 0

            elif price <= dynamic_stop_price:
                # Actived stoploss
                capital = btc * price
                btc = 0
                position = 0

            elif df.at[i, 'signal'] == -1:
                capital = btc * price
                btc = 0
                position = 0

    # If posiotion is open:
    if position == 1:
        capital = btc * df.iloc[-1]['close']

    return capital
