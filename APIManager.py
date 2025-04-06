import yfinance as yf
import bs4 as bs
import requests

class APIManager:
    def __init__(self):
        self.client = yf
        
    def get_stock_data(self, symbol):
        return Stock(self.client.Ticker(symbol).info)
    
    def get_nyse_symbols(self):
        tickers=[]

        # Gets all the stocks in the table for every pagination at the website.
        for letter in list(map(chr, range(ord('A'), ord('Z')+1))):
            print(f'Loading stocks that start with: {letter}')
            
            # Stock list found online. The BeautifulSoup library reads the page's HTML
            resp=requests.get(
                f'https://stock-screener.org/stock-list.aspx?alpha={letter}')
            soup=bs.BeautifulSoup(resp.text, 'lxml')
            
            # Tracks the table element from the website
            table=soup.find('table', {'class': 'styled'})

            # Fetches the actual value from the table
            for row in table.findAll('tr')[1:]:
                ticker=row.findAll('td')[0].text
                tickers.append(ticker.strip())
    
        return tickers

# Stock class
class Stock:
    def __init__(self, data):
        self.data = data
    
    def return_symbol(self):
        return self.data['symbol']
    
    def check_formula_valid(self):
        return (self.data['currentPrice'] / self.data['trailingEps']) > 0 and self.data['returnOnAssets'] > 0
        
    