def back_test(df, dynamic_stoploss, take_profit):
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
            # آپدیت داینامیک استاپ اگر قیمت بالاتر رفت
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
                # سیگنال فروش هم باعث فروش میشه
                capital = btc * price
                btc = 0
                position = 0

    # If posiotion is open:
    if position == 1:
        capital = btc * df.iloc[-1]['close']

    return capital
