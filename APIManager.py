import yfinance as yf
import bs4 as bs
import requests
from colorama import Fore
import pandas as pd

class APIManager:
    def __init__(self):
        self.client = yf
        
    def get_stock_data(self, symbol):
        return Stock(self.client.Ticker(symbol).info, self.client.Ticker(symbol).balance_sheet)
    
    def get_nyse_symbols(self):
        tickers=[]

        # Gets all the stocks in the table for every pagination at the website.
        for letter in list(map(chr, range(ord('A'), ord('Z')+1))):
            print(Fore.WHITE + f'Loading stocks that start with: {letter}')
            
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
    
    def get_current_AAA_yield(self):
        resp=requests.get(
                f'https://fred.stlouisfed.org/series/AAA')
        soup=bs.BeautifulSoup(resp.text, 'lxml')

        # Gets the current yield from the website
        current_yield = soup.find('span', {'class': 'series-meta-observation-value'}).text

        if current_yield == 'N/A':
            return 0
        else:
            return float(current_yield)

# Stock class
class Stock:
    def __init__(self, data, balance_sheet):
        api_manager = APIManager()
        self.data = data
        self.balance_sheet = balance_sheet
        self.ebit = self.get_ebit()
        self.ey = self.calculate_ey()
        self.roc = self.calculate_roc()
        self.intrinsic_value = self.calculate_intrinsic_value(7, api_manager.get_current_AAA_yield())
    
    def return_symbol(self):
        return self.data['symbol']
    
    def check_formula_valid(self):
        return (self.data['currentPrice'] / self.data['trailingEps']) > 0 and self.roc > 0 and self.ey > 0
    
    def calculate_intrinsic_value(self,growth_rate, current_yield):
        """
        Calculate the intrinsic value using Graham's formula.
        
        Parameters:
        eps (float): Trailing 12-month EPS of the company
        growth_rate (float): Long-term growth rate of the company (as a decimal)
        
        Returns:
        float: Intrinsic value
        """
        
        AVERAGE_BOND_YIELD_IN_1962 = 4.4
        PE_FOR_NON_GROWTH_STOCKS = 8.5
        
        intrinsic_value = self.data['trailingEps'] * (PE_FOR_NON_GROWTH_STOCKS + (2 * growth_rate) * AVERAGE_BOND_YIELD_IN_1962) / current_yield
        return intrinsic_value
    
    def calculate_roc(self):
         
        df = pd.DataFrame(self.balance_sheet)
       
        # Get the current assets and liabilities
        current_assets = df.loc['Current Assets'].iloc[0]
        current_liabilities = df.loc['Current Liabilities'].iloc[0]
        net_working_capital = current_assets - current_liabilities
        
        # Get the net fixed assets
        net_fixed_assets = df.loc['Current Assets'].iloc[0] - df.loc['Accumulated Depreciation'].iloc[0]
        
        # Calculate ROC
        if (net_fixed_assets + net_working_capital) != 0:
            return self.ebit / (net_fixed_assets + net_working_capital)
        return 0

    def calculate_ey(self):
        
        eps = self.data['trailingEps']
        stock_price = self.data['currentPrice']
        
        return eps / stock_price if eps else 0
    
    
    def get_ebit(self):
        self.pd = pd.DataFrame(yf.Ticker(self.data['symbol']).financials)
        
        return self.pd.loc['EBIT'].iloc[0]
        
        
        
        
    