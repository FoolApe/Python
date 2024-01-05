import twstock

def get_stock_info(stock_code):
    if ',' in stock_code:
        stock_codes = stock_code.split(',')
        stock_data = {}
        for code in stock_codes:
            stock = twstock.realtime.get(code.strip())
            success = stock.get('success', False)
            if success:
                open_price = round(float(stock['realtime']['open']), 1)
                high_price = round(float(stock['realtime']['high']), 1)
                low_price = round(float(stock['realtime']['low']), 1)
                stock_name = stock['info']['name']
                stock_data[code] = {'stockName': stock_name, 'openPrice': str(open_price), 'highPrice': str(high_price), 'lowPrice': str(low_price)}
            else:
                stock_data[code] = None
        return stock_data

# 從外部傳入股票代號
input_stock_code = input("請輸入股票代號：")
result = get_stock_info(input_stock_code)

# output
if result:
    if isinstance(result, dict):
        for code, data in result.items():
            if data:
                print(f"{data['stockName']} ({code}): 開盤價 {data['openPrice']}, 最高價 {data['highPrice']}, 最低價 {data['lowPrice']}")
            else:
                print(f"無法獲取股票 {code} 的資訊")
    else:
        if result:
            print(f"{result['stockName']}: 開盤價 {result['openPrice']}, 最高價 {result['highPrice']}, 最低價 {result['lowPrice']}")
else:
    print('沒有寫個股資訊。')
