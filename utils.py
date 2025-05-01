from APIManager import APIManager
from colorama import Fore
api_manager = APIManager()



def rank_graham_stocks(stocks):
    """
    Ranks stocks based on Benjamin Graham's investment criteria.
    
    Parameters:
    stocks (list): List of stock dictionaries with graham_props
    
    Returns:
    list: The same list with updated graham_rank values
    """
    
    for stock in stocks:
        stock['graham_props']['value_difference'] = (stock['price'] - stock["graham_props"]["intrinsic_value"]) / stock["graham_props"]["intrinsic_value"] * 100
    
    # Sort by Graham score and valuation
    stocks.sort(key=lambda x: x['graham_props']['value_difference'])
    
    # Add Graham ranking
    for i, stock in enumerate(stocks, 1):
        stock['graham_props']['graham_rank'] = i
        del stock['graham_props']['value_difference']

    # Calculate Graham score and rank stocks accordingly
    return stocks

def rank_magic_formula_stocks(stocks):
    """
    Ranks stocks based on Joel Greenblatt's Magic Formula.
    Combines Return on Assets (ROA) and Price-to-Earnings (PE) ratio
    with weighted importance.
    
    Parameters:
    stocks (list): List of stock dictionaries with magic_formula_props
    
    Returns:
    list: The same list with updated magic_formula_rank values
    """
   
    # Sort by combined score (higher is better)
    stocks.sort(key=lambda x: (x['magic_formula_props']['roc'],x['magic_formula_props']['ey']), reverse=True)
    # Add Magic Formula ranking
    for i, stock in enumerate(stocks, 1):
        stock['magic_formula_props']['magic_formula_rank'] = i
        
    
    return stocks

def fix_icon_missing(stock):
    if stock['symbol'] == 'META':
        stock['logo_url'] = 'https://logo.clearbit.com/meta.com'
        return stock
    if stock['symbol'] == 'GPN':
        stock['logo_url'] = 'https://logo.clearbit.com/globalpayments.com'
        return stock
    if stock['symbol'] == 'TBBB':
        stock['logo_url'] = 'https://bbbfoods.net/en/'
        return stock
    if stock['symbol'] == 'LAUR':
        stock['logo_url'] = 'https://logo.clearbit.com/laureate.net/'
        return stock
    if stock['symbol'] == 'CMBT':
        stock['logo_url'] = 'https://logo.clearbit.com/cmb.tech/'
        return stock
    if stock['symbol'] == 'HALO':
        stock['logo_url'] = 'https://logo.clearbit.com/halozyme.com'
        return stock
    if stock['symbol'] == 'HLI':
        stock['logo_url'] = 'https://logo.clearbit.com/hl.com'
        return stock
    if stock['symbol'] == 'TM':
        stock['logo_url'] = 'https://logo.clearbit.com/toyota.com'
        return stock
    if stock['symbol'] == 'DIS':
        stock['logo_url'] = 'https://logo.clearbit.com/disney.com'
        return stock
    if stock['symbol'] == 'HCA':
        stock['logo_url'] = 'https://logo.clearbit.com/hcahealthcare.com'
        return stock
    if stock['symbol'] == 'HMC':
        stock['logo_url'] = 'https://logo.clearbit.com/honda.com'
        return stock
    if stock['symbol'] == 'GRMN':
        stock['logo_url'] = 'https://logo.clearbit.com/garmin.com'
        return stock
    if stock['symbol'] == 'DXCM':
        stock['logo_url'] = 'https://logo.clearbit.com/dexcom.com'
        return stock
    if stock['symbol'] == 'SW':
        stock['logo_url'] = 'https://logo.clearbit.com/smurfitkappa.com'
        return stock
    if stock['symbol'] == 'VIK':
        stock['logo_url'] = 'https://logo.clearbit.com/viking.com'
        return stock
    if stock['symbol'] == 'LTM':
        stock['logo_url'] = 'https://logo.clearbit.com/latamairlines.com'
        return stock
    return stock


def print_border(): print(Fore.WHITE + "=====================================================")