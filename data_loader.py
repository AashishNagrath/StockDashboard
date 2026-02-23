import yfinance as yf

def get_stock_data(ticker, start_date, end_date):
    stockdata = yf.download(ticker, start=start_date, end=end_date)
    if stockdata.empty:
        return None
    
    if isinstance(stockdata.columns, tuple) or hasattr(stockdata.columns, 'levels'):
        stockdata.columns = stockdata.columns.get_level_values(0)
    stockdata = stockdata.reset_index()
    stockdata = stockdata.dropna()
    return stockdata