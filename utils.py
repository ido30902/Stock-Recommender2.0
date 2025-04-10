from APIManager import APIManager
from colorama import Fore
api_manager = APIManager()

def calculate_intrinsic_value(eps, growth_rate, current_yield):
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
    
    intrinsic_value = eps * (PE_FOR_NON_GROWTH_STOCKS + (2 * growth_rate) * AVERAGE_BOND_YIELD_IN_1962) / current_yield
    return intrinsic_value

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
    stocks.sort(key=lambda x: (x['graham_props']['graham_score'], stock['graham_props']['value_difference']), reverse=True)
    
    # Add Graham ranking
    for i, stock in enumerate(stocks, 1):
        stock['graham_props']['graham_rank'] = i

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
    
    # Weights for the magic formula
    ROA_WEIGHT = 0.3 # 30% of the overall score
    PE_WEIGHT = 0.7 # 70% of the overall score

    # Calculate combined score where PE is 70% and ROA is 30% of overall score
    for stock in stocks:
        pe_score = stock['pe'] if stock['pe'] != 0 else float('inf')
        roa_score = stock['magic_formula_props']['roa'] if 'roa' in stock['magic_formula_props'] else 0
        # Lower PE is better, higher ROA is better
        # Invert PE so higher values are better for sorting
        if pe_score != float('inf'):
            stock['magic_formula_props']['combined_score'] = (PE_WEIGHT * (1/pe_score)) + (ROA_WEIGHT * roa_score)
        else:
            stock['magic_formula_props']['combined_score'] = ROA_WEIGHT * roa_score
       
    # Sort by combined score (higher is better)
    stocks.sort(key=lambda x: x['magic_formula_props']['combined_score'], reverse=True)
    # Add Magic Formula ranking
    for i, stock in enumerate(stocks, 1):
        stock['magic_formula_props']['magic_formula_rank'] = i
        del stock['magic_formula_props']['combined_score']
    
    return stocks

def print_border(): print(Fore.WHITE + "=====================================================")