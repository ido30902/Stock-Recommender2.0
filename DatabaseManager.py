from pymongo import MongoClient

class DatabaseManager:
    def __init__(self):
        
        self.mongo = MongoClient('mongodb://localhost:27017')
    
        try:
           
            self.mongo._connect()
           
            self.mongo.admin.command({'ping': 1})
            print("Pinged your deployment. You successfully connected to MongoDB!")
            
            
            if 'book_investment' in self.mongo.list_database_names():
                self.db = self.mongo["book_investment"]
                
        except:
            pass
        
    def insert_new_stock(self,stock):
        self.db['stocks'].insert_one(stock)
    
    def insert_many_stocks(self,stocks):
        self.db['stocks'].insert_many(stocks)
    
    def update_stock(self, stock):
        self.db['stocks'].update_one({'symbol': stock['symbol']}, {'$set': stock})

