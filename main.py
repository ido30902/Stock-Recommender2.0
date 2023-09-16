import pandas as pd
import bs4 as bs
import requests
import yfinance as yf
from string import ascii_uppercase as alphabet
import json
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText


def main():
    stocks_list = get_nyse_symbols_from_db()

    choose_recommended_stocks(stocks_list)


def choose_recommended_stocks(stocks):
    
    preset = {'symbol': '', 'pe': 0.0, 'roa': 0.0, 'marketCap': 0, 'name': ''}
    new_list = []

    print('Collecting stock updates...\nStocks loaded:')

    # Information from Yahoo Finance
    for stock in stocks:
        # List preparation preset
        preset = {'symbol': '', 'pe': 0.0, 'roa': 0.0, 'marketCap': 0, 'name': ''}
        try:
            # Retrieves the data and stores it in the object
            data = yf.Ticker(stock)
            preset['marketCap'] = data.info['marketCap']
            preset['name'] = data.info['shortName']
            preset['roa'] = data.info['returnOnAssets']
            preset['pe'] = (data.info['currentPrice'] / data.info['trailingEps'])
            preset['symbol'] = stock

            # Checks if parameters are valid - Return on Assets > 0, Price to Earnings ratio > 0 and Market value is above 2B$
            if (data.info['currentPrice'] / data.info['trailingEps']) > 0 and data.info['returnOnAssets'] > 0 and data.info['marketCap'] > 2000000000:
                print_border()
                print(f'Stock loaded: {stock}\nCompany name: {data.info["shortName"]}\nPE: {(data.info["currentPrice"] / data.info["trailingEps"]):.2f}\nROA: {data.info["returnOnAssets"] * 100:.2f}%\nMarket Capital: {data.info["marketCap"]:,}$')
                new_list.append(preset)
            else:
                print_border()
                print(f"({stock}), {preset['name']} | Didn't match the criteria")
        except:
            print_border()
            print(f'Error loading {stock}')

    # Sorts the list 
    new_list.sort(key=lambda x: (-x['roa'], x['pe']))
    
    # Strips the list so the it keeps only the 10 first items
    new_list = new_list[:10]
    for stock in new_list:
        print(stock['symbol'],end=', ')
    
    


# Updates the stocks list to the stock_list.json file
def update_stocks_list(stocks):
    with open('stocks_list.json', 'w') as json_file:
        json_file.write(json.dumps(stocks))

# Loads the stocks list from the stock_list.json file
def get_nyse_symbols_from_db():
    with open('stocks_list.json') as json_file:
        return json.load(json_file)
        

def get_nyse_symbols_from_web():

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

def mail_list(output_list):
    pass
    # s = smtplib.SMTP(host='your_host_address_here', port=your_port_here)
    # s.starttls()
    # s.login(MY_ADDRESS, PASSWORD)

    # msg = MIMEMultipart() 

    # # setup the parameters of the message
    # msg['From']=MY_ADDRESS
    # msg['To']=email
    # msg['Subject']="This is TEST"
    # msg.attach(MIMEText(message, 'plain'))
    # s.sendmail

def print_border(): print("=====================================================")


if __name__ == '__main__':
    main()