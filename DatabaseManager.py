from pymongo import MongoClient
import os



class DatabaseManager:
    def __init__(self):
        
        self.mongo = MongoClient(os.getenv("DB_URL"))
    
        try:
           
            self.mongo._connect()
           
            self.mongo.admin.command({'ping': 1})
            print("Pinged your deployment. You successfully connected to MongoDB!")
            
            if 'book_investment' in self.mongo.list_database_names():
                self.db = self.mongo["book_investment"]
                print("Database found")
            else:
                print("Database not found")
                
        except:
            print("Error connecting to MongoDB or Database not found")
        
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
        for stock in stocks:
            # Check if the stock exists before updating
            existing_stock = self.db['stocks'].find_one({'symbol': stock['symbol']})
            if existing_stock:
                # Update existing stock
                self.db['stocks'].update_one({'symbol': stock['symbol']}, {'$set': stock})
            else:
                # Insert new stock if not found
                self.db['stocks'].insert_one(stock)

