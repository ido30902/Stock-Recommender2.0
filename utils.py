def calculate_intrinsic_value(eps, growth_rate):
    """
    Calculate the intrinsic value using Graham's formula.
    
    Parameters:
    eps (float): Trailing 12-month EPS of the company
    growth_rate (float): Long-term growth rate of the company (as a decimal)
    
    Returns:
    float: Intrinsic value
    """
    intrinsic_value = eps * (8.5 + 2 * growth_rate)
    return intrinsic_value

def rank_graham_stocks(stocks):
    """
    Ranks stocks based on Benjamin Graham's investment criteria.
    
    Parameters:
    stocks (list): List of stock dictionaries with graham_props
    
    Returns:
    list: The same list with updated graham_rank values
    """
    # Sort by Graham score
    stocks.sort(key=lambda x: x['graham_props']['graham_score'], reverse=True)
    
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