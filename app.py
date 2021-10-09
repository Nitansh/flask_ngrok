from flask import Flask, Response
from nsetools import Nse
import json

nse = Nse()
app = Flask(__name__)

all_stocks = [*nse.get_stock_codes()]

@app.route("/all_stock/")
def all_stock():
  return Response(
    json.dumps( all_stocks),
    mimetype='application/json'
  )

@app.route("/stock/<symbols>")
def stock_data(symbols):
  stock_data = []
  symbols = symbols.split('-')
  for symbol in symbols:
    try:
      if symbol:
        data = nse.get_quote(symbol)
        if 'pChange' in data and data[ 'pChange' ]:
          stock_data.append({'symbol': symbol, 'change' : float(data[ 'pChange' ]), 'lastPrice' : float(data['lastPrice'] ) })
    except:
      stock_data.append({'symbol': symbol, 'change' : -1, 'lastPrice' : -1 })

  return Response(
    json.dumps( stock_data ),
    mimetype='application/json'
  )

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)