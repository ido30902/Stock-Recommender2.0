from colorama import Fore, Style
from DatabaseManager import DatabaseManager
from APIManager import APIManager
import time
from utils import *

db_controller = DatabaseManager()
api_manager = APIManager()

def main():
    while True:
        # Get all the stocks from the NYSE
        stocks_list = api_manager.get_nyse_symbols()
        
        # Get the data for each stock
        stocks_list = get_stocks_data(stocks_list)

        # Rank the stocks based on Graham's formula
        stocks_list = rank_graham_stocks(stocks_list)

        # Rank the stocks based on the Magic Formula
        stocks_list = rank_magic_formula_stocks(stocks_list)
        
        # Update the stocks in the database
        db_controller.update_many_stocks(stocks_list)
        
        db_controller.update_last_updated()
        
        print(Style.RESET_ALL + '\nFinished a session. Waiting for 7 days before running again...')
        
        # Wait one week before running again
        time.sleep(604800)
    
    

def get_stocks_data(stocks):
    
    new_list = []

    current_yield = api_manager.get_current_AAA_yield()
    
    print_border()
    print(Fore.CYAN + f'Current yield: {current_yield}')
    print_border()
    
    print(Fore.CYAN + 'Collecting stock updates...\nStocks loaded:')

    for stock in stocks:
        try:
            # Get stock data using yfinance
            s = api_manager.get_stock_data(stock)
            
            if s.intrinsic_value <= 0:
                s.intrinsic_value = 0.01
            
            # Store data in preset
            preset = {
                'symbol': s.data['symbol'],
                'price': s.data['currentPrice'],
                'pe': (s.data['currentPrice'] / s.data['trailingEps']) if s.data['trailingEps'] != 0 else 0,
                'marketCap': s.data['marketCap'],
                'name': s.data['shortName'],
                'description': s.data['longBusinessSummary'],
                'logo_url': 'https://logo.clearbit.com/' + s.data['website'].strip('https://'),
                'sector': s.data['sectorDisp'],
                'website': s.data['website'],
                'graham_props':{
                    'graham_rank': 0,
                    'eps': s.data['trailingEps'],
                    'intrinsic_value': s.intrinsic_value,
                },
                'magic_formula_props':{
                    'roc': s.roc,
                    'ey': s.ey,
                    'magic_formula_rank': 0
                }
            }
            
            preset = fix_icon_missing(preset)

            # Magic Formula combines ROC and EY
            # Higher values are better
            if s.check_formula_valid():
                print_border()
                print(Fore.GREEN + f'Stock loaded: {stock}\nCompany name: {s.data["shortName"]}\nTrading Price: {s.data["currentPrice"]:.2f}$\nGraham Price Valuation: {s.intrinsic_value:.2f}$\nPE: {preset["pe"]:.2f}\nROC: {s.roc * 100 :.2f}%\nEY: {s.ey * 100 :.2f}%\nMarket Capital: {s.data["marketCap"]:,}$')
                new_list.append(preset)
            else:
                print_border()
                print(Fore.YELLOW + f"({s.data['symbol']}), {preset['name']} | Didn't match the criteria")  
        
        except Exception as e:
            if "Too Many Requests" in str(e):
                print_border()
                print(Fore.YELLOW + f"Rate limit reached. Waiting for 60 seconds...\nAdding {stock} back to the list")  
                time.sleep(60)
                stocks.append(stock)  # Add the failed stock back to the list
                continue
            print_border()
            print(Fore.RED + f'Error loading {stock}: {str(e)}')            

    return new_list

if __name__ == '__main__':
    main()
