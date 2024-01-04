from flask import Flask, request, jsonify
import twstock

app = Flask(__name__)

def get_stock_info(stock_code):
    stock = twstock.realtime.get(stock_code)
    chk = stock['success']

    if chk:
        openPrice = round(float(stock['realtime']['open']), 1)
        highPrice = round(float(stock['realtime']['high']), 1)
        lowPrice = round(float(stock['realtime']['low']), 1)
        return openPrice, highPrice, lowPrice
    else:
        return None

@app.route('/get_stock_info', methods=['GET'])
def stock_info():
    stock_code = request.args.get('stock_code')
    if not stock_code:
        return jsonify({'error': 'Stock code is required'})

    result = get_stock_info(stock_code)
    if result:
        openPrice, highPrice, lowPrice = result
        return jsonify({'openPrice': openPrice, 'highPrice': highPrice, 'lowPrice': lowPrice})
    else:
        return jsonify({'error': 'Unable to retrieve stock information'})

if __name__ == '__main__':
    app.run(debug=True)
