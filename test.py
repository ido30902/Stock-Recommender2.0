from APIManager import APIManager, Stock

ap = APIManager()

print(ap.get_stock_data('CCL').data)


