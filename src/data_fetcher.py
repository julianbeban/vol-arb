import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_options_chain(ticker, save_to_csv=False):
    """
    Fetch all options data for a ticker
    Returns: DataFrame with calls and puts
    """
    stock = yf.Ticker(ticker)
    
    # Get current stock price
    spot_price = stock.history(period='1d')['Close'].iloc[-1]
    
    # Get all expiration dates
    expirations = stock.options
    
    all_options = []
    
    for expiry in expirations:
        # Fetch options chain for this expiry
        opt_chain = stock.option_chain(expiry)
        
        # Process calls
        calls = opt_chain.calls.copy()
        calls['optionType'] = 'call'
        calls['expirationDate'] = expiry
        
        # Process puts
        puts = opt_chain.puts.copy()
        puts['optionType'] = 'put'
        puts['expirationDate'] = expiry
        
        all_options.append(calls)
        all_options.append(puts)
    
    # Combine all data
    df = pd.concat(all_options, ignore_index=True)
    
    # Add spot price column
    df['spotPrice'] = spot_price
    df['fetchTime'] = datetime.now()
    
    if save_to_csv:
        filename = f"data/{ticker}_options_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        print(f"Saved to {filename}")
    
    return df, spot_price

if __name__ == "__main__":
    # Test with SPY (S&P 500 ETF - very liquid)
    print("Fetching SPY options data...")
    df, spot = fetch_options_chain('SPY', save_to_csv=True)
    
    print(f"\nSpot price: ${spot:.2f}")
    print(f"Total options: {len(df)}")
    print(f"\nSample data:")
    print(df[['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest', 'optionType', 'expirationDate']].head(10))