from flask import Flask, render_template, request
from random import randint
import requests

app = Flask(__name__)



def fetch_price(ticker):
    API_URL =f'https://financialmodelingprep.com/api/v3/stock/full/real-time-price/{ticker}?apikey=aTwuVNDl0v10VMLXZwApUMSTm2GdZJ3l'
    response = requests.get(API_URL).json()
    data = response
    price = data[0]['askPrice']
    return  f"{price}"



@app.route('/stock/<ticker>', methods= ['GET'])
def stock(ticker):
    price = fetch_price(ticker)
    return render_template('stock_quote.html',ticker=ticker, price=price)


@app.route('/',  methods=['GET', 'POST'])
def home_page():
   stock_data = None  #
   if request.method == 'POST':
        # Get the stock type from the form
        stock_type = request.form.get('stockType')
        price = fetch_price(stock_type)

        # Mock response for demonstration (replace with real stock data fetching logic)
        stock_data = {
            "name": stock_type.upper(),
            "value": price   # Example static value
        }
   return render_template('index.html', stock_data=stock_data)
 
 
@app.route('/financials', methods=['GET'])
def financials():
    # Get the ticker from the query parameters (e.g., /financials?ticker=AAPL)
    ticker = request.args.get('ticker')
    
    # Fetch financial data for the ticker
    data = fetch_income(ticker)
    
    # Render the financials template with the retrieved data
    return render_template('financials.html', ticker=ticker, financials=data)

def fetch_income(ticker):
    # URL for the income statement API, replace `{ticker}` with the actual stock symbol
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period=annual&apikey=aTwuVNDl0v10VMLXZwApUMSTm2GdZJ3l"
    
    # Make a request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON data
        financials = response.json()
        
        # Sort financials by 'date' in descending order
        financials.sort(key=lambda x: x['date'], reverse=True)
        return financials
    else:
        # Return an empty list if there's an error
        return []
    
    

if __name__ == '__main__':
    app.run(debug=True)