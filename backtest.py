def back_test(df):
    capital = 1000
    position = 0  # 0: no position, 1: holding BTC
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

    # If posiotion is open:
    if position == 1:
        capital = btc * df.iloc[-1]['close']

    return capital
