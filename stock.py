import twstock

def get_stock_info(stock_code):
    # 更新code(only once)
    #twstock.__update_codes()

    # 撈取實時價格
    stock = twstock.realtime.get(stock_code)

    # 驗證
    chk = stock['success']

    # 回傳
    if chk:
        openPrice = round(float(stock['realtime']['open']), 1)
        highPrice = round(float(stock['realtime']['high']), 1)
        lowPrice = round(float(stock['realtime']['low']), 1)
        return openPrice, highPrice, lowPrice
    else:
        return None

# 從外部傳入股票代號
input_stock_code = input("請輸入股票代號：")
result = get_stock_info(input_stock_code)

if result:
    openPrice, highPrice, lowPrice = result
    print(openPrice, highPrice, lowPrice)
else:
    print('無法獲取股票資訊。')
