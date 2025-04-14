from colorama import Fore, Style
from DatabaseManager import DatabaseManager
from APIManager import APIManager
import time
from utils import *

db_controller = DatabaseManager()
api_manager = APIManager()

def main():
    
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
     
    print(Style.RESET_ALL + '\n')
    
    

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
            
            # Calculate Benjamin Graham metrics
            current_ratio = s.data['currentRatio']
            debt_to_equity = s.data['debtToEquity']
            book_value = s.data['bookValue']
            current_price = s.data['currentPrice']
            graham_score = 0

            # Calculate Graham score based on his criteria
            if current_ratio >= 2 and debt_to_equity < 0.5:
                graham_score += 1
            if current_price < book_value * 1.5:
                graham_score += 1
            if s.data['trailingEps'] > 0:
                graham_score += 1
            
            intrinsic_value = s.calculate_intrinsic_value(7, current_yield)
            
            roc = s.calculate_roc()
            ey = s.calculate_ey()
            
            if intrinsic_value <= 0:
                intrinsic_value = 0.01
            
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
                'graham_props':{
                    'graham_score': graham_score,
                    'current_ratio': current_ratio,
                    'debt_to_equity': debt_to_equity,
                    'book_value': book_value,
                    'graham_rank': 0,
                    'eps': s.data['trailingEps'],
                    'intrinsic_value': intrinsic_value,
                },
                'magic_formula_props':{
                    'roc': roc,
                    'ey': ey,
                    'magic_formula_rank': 0
                }
            }

            # Magic Formula combines ROC and EY
            # Higher values are better
            if s.check_formula_valid():
                print_border()
                print(Fore.GREEN + f'Stock loaded: {stock}\nCompany name: {s.data["shortName"]}\nTrading Price: {s.data["currentPrice"]:.2f}$\nGraham Price Valuation: {intrinsic_value:.2f}$\nPE: {preset["pe"]:.2f}\nROC: {preset["magic_formula_props"]["roc"] * 100 :.2f}%\nEY: {preset["magic_formula_props"]["ey"] * 100 :.2f}%\nMarket Capital: {s.data["marketCap"]:,}$')
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
