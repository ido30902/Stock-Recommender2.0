from colorama import Fore, Style
from DatabaseManager import DatabaseManager
from APIManager import APIManager, Stock
import time

db_controller = DatabaseManager()
api_manager = APIManager()

def main():
    
    stocks_list = api_manager.get_nyse_symbols()

    stocks_list = get_stocks_data(stocks_list)
    
    db_controller.insert_many_stocks(stocks_list)
     
    print(Style.RESET_ALL + '\n')
    

def rank_graham_stocks(stocks):
    # Sort by Graham score
    stocks.sort(key=['graham_props']['graham_score'], reverse=True)
    
    # Add Graham ranking
    for i, stock in enumerate(stocks, 1):
        stock['graham_rank'] = i
    
    return stocks

def rank_magic_formula_stocks(stocks):
    stocks.sort(key=lambda x: (-x['magic_formula_props']['roa'], x['pe']))
    
     # Add Magic Formula ranking
    for i, stock in enumerate(stocks, 1):
        stock['magic_formula_props']['magic_formula_rank'] = i
    
    return stocks

def get_stocks_data(stocks):
    
    new_list = []

    print('Collecting stock updates...\nStocks loaded:')

    for stock in stocks:
        try:
            # Get stock data using yfinance
            s = api_manager.get_stock_data(stock)
            
            # Calculate Return on Capital (ROC)
            # ROC = EBIT / (Net Working Capital + Net Fixed Assets)
            #ebitda = s.data['ebitda']
            #working_capital = s.data['totalCurrentAssets'] - s.data['totalCurrentLiabilities']
            #fixed_assets = s.data['propertyPlantEquipment']
            #roc = ebitda / (working_capital + fixed_assets) if (working_capital + fixed_assets) != 0 else 0
            # different way to calculate ROC


            # Calculate Earnings Yield (EY)
            # EY = EBITDA / Enterprise Value
            #enterprise_value = s.data['enterpriseValue']
            #ey = ebitda / enterprise_value if enterprise_value != 0 else 0
            
            
            

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

            # Store data in preset
            preset = {
                'symbol': s.data['symbol'],
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
                    'graham_rank': 0
                },
                'magic_formula_props':{
                    'roa': s.data['returnOnAssets'],
                    'magic_formula_rank': 0
                }
            }

            # Magic Formula combines ROC and EY
            # Higher values are better
            if s.check_formula_valid():
                print_border()
                print(Fore.GREEN + f'Stock loaded: {stock}\nCompany name: {s.data["shortName"]}\nPE: {preset["pe"]:.2f}\nROA: {s.data["returnOnAssets"] * 100 :.2f}%\nMarket Capital: {s.data["marketCap"]:,}$\nGraham Score: {graham_score}/3')
                new_list.append(preset)
            else:
                print_border()
                print(Fore.YELLOW + f"({s.data['symbol']}), {preset['name']} | Didn't match the criteria")
        
        except Exception as e:
            if "Too Many Requests" in str(e):
                print(Fore.YELLOW + f"Rate limit reached. Waiting for 60 seconds...\nAdding {stock} back to the list")
                print_border()
                time.sleep(60)
                stocks.append(stock)  # Adds the failed stock back to the list
                continue
            print(Fore.RED + f'Error loading {stock}: {str(e)}')
            print_border()

    print_border()
    #new_list = rank_graham_stocks(new_list)
    #new_list = rank_magic_formula_stocks(new_list)
    
    return new_list

def print_border(): print(Fore.WHITE + "=====================================================")


if __name__ == '__main__':
    main()
