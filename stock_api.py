from flask import Flask, jsonify, request
import twstock

app = Flask(__name__)

def get_stock_info(stock_code):
    if ',' in stock_code:
        stock_codes = stock_code.split(',')
        stock_data = {}
        for code in stock_codes:
            stock = twstock.realtime.get(code.strip())
            success = stock.get('success', False)
            if success:
                open_price = round(float(stock['realtime']['open']), 2)
                high_price = round(float(stock['realtime']['high']), 2)
                low_price = round(float(stock['realtime']['low']), 2)
                stock_name = stock['info']['name']
                stock_data[code] = {
                    'stockName': stock_name,
                    'openPrice': str(open_price),
                    'highPrice': str(high_price),
                    'lowPrice': str(low_price)
                }
            else:
                stock_data[code] = None
        return stock_data

@app.route('/get_stock_info', methods=['GET'])
def stock_info():
    stock_code = request.args.get('stock_code')
    if not stock_code:
        return jsonify({'error': 'Stock code is required'})

    result = get_stock_info(stock_code)

    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Unable to retrieve stock information'})

if __name__ == '__main__':
    app.run(debug=True, port=80)
