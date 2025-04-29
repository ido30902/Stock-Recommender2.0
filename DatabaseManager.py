from pymongo import MongoClient
import os
from colorama import Fore, Style
from utils import print_border
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        
        self.mongo = MongoClient(os.getenv("DB_URL"))
    
        try:
           
            self.mongo._connect()
           
            self.mongo.admin.command({'ping': 1})
            print(Fore.CYAN + "\nPinged your deployment. You successfully connected to MongoDB!")
            
            if 'book_investment' in self.mongo.list_database_names():
                self.db = self.mongo["book_investment"]
                print(Fore.CYAN + "Database found")
                print_border()
            else:
                print(Fore.RED + "Database not found")
                print_border()
                
        except:
            print(Fore.RED + "Error connecting to MongoDB or Database not found")
            print_border()
        
    def insert_new_stock(self,stock):
        self.db['stocks'].insert_one(stock)
    
    def insert_many_stocks(self,stocks):
        self.db['stocks'].insert_many(stocks)
    
    def update_stock(self, stock):
        existing_stock = self.db['stocks'].find_one({'symbol': stock['symbol']})
        if existing_stock:
            self.db['stocks'].update_one({'symbol': stock['symbol']}, {'$set': stock})
        else:
            self.db['stocks'].insert_one(stock)
    
    def update_many_stocks(self, stocks):
        
        # Delete all stocks from the database
        self.db['stocks'].delete_many({})
        
        for stock in stocks:
            # Check if the stock exists before updating
            existing_stock = self.db['stocks'].find_one({'symbol': stock['symbol']})
            if existing_stock:
                # Update existing stock
                self.db['stocks'].update_one({'symbol': stock['symbol']}, {'$set': stock})
            else:
                # Insert new stock if not found
                self.db['stocks'].insert_one(stock)
    
    def generate_dummy_stock_list(self):
        return ['AAPL', 'TSLA', 'NVDA', 'MSFT', 'GOOG', 'AMZN', 'TSM', 'WMT', 'NFLX', 'ORCL', 'QCOM', 'IBM', 'JNJ', 'VZ', 'BA', 'CAT', 'MMM', 'GE', 'MCD', 'PFE', 'WBA', 'DIS', 'TM', 'V', 'IBM', 'JNJ', 'VZ', 'BA', 'CAT', 'MMM', 'GE', 'MCD', 'PFE', 'WBA', 'DIS', 'TM', 'V', 'IBM', 'JNJ']

    def update_last_updated(self):
        self.db['util'].update_one({}, {'$set': {'last_updated': datetime.now()}})

    def get_last_updated(self):
        return self.db['util'].find_one({})['last_updated']

