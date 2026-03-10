import pandas as pd
import numpy as np

def clean_options_data(df, min_volume=10, min_open_interest=50, max_bid_ask_spread=0.5):
    """
    Filter options for quality:
    - Remove low liquidity
    - Remove stale quotes
    - Handle bid-ask spreads
    """
    df = df.copy()
    
    print(f"Initial rows: {len(df)}")
    
    # Filter by volume and open interest
    df = df[(df['volume'] >= min_volume) | (df['openInterest'] >= min_open_interest)]
    print(f"After liquidity filter: {len(df)}")
    
    # Remove zero bids/asks
    df = df[(df['bid'] > 0) & (df['ask'] > 0)]
    print(f"After removing zero quotes: {len(df)}")
    
    # Remove wide spreads (% of mid price)
    df['midPrice'] = (df['bid'] + df['ask']) / 2
    df['spread'] = df['ask'] - df['bid']
    df['spreadPct'] = df['spread'] / df['midPrice']
    df = df[df['spreadPct'] <= max_bid_ask_spread]
    print(f"After spread filter: {len(df)}")
    
    # Use mid price for valuation
    df['marketPrice'] = df['midPrice']
    
    return df

if __name__ == "__main__":
    # Load most recent data file
    import glob
    files = glob.glob('data/SPY_options_*.csv')
    latest_file = max(files)
    
    print(f"Loading {latest_file}\n")
    df = pd.read_csv(latest_file)
    
    cleaned = clean_options_data(df)
    
    print(f"\nCleaned data sample:")
    print(cleaned[['strike', 'marketPrice', 'volume', 'openInterest', 'optionType']].head())