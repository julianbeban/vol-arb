import pandas as pd
import numpy as np
from datetime import datetime

def prepare_for_iv_calculation(df, spot_price, risk_free_rate=0.05):
    """
    Add columns needed for IV calculation:
    - Moneyness (K/S)
    - Time to expiry (years)
    - In-the-money flag
    """
    df = df.copy()
    
    # Calculate time to expiry
    df['expirationDate'] = pd.to_datetime(df['expirationDate'])
    df['daysToExpiry'] = (df['expirationDate'] - datetime.now()).dt.days
    df['timeToExpiry'] = df['daysToExpiry'] / 365.0
    
    # Remove expired or very short-dated
    df = df[df['timeToExpiry'] > 0.01]  # At least ~4 days
    
    # Moneyness
    df['moneyness'] = df['strike'] / spot_price
    
    # ITM/OTM classification
    df['isITM'] = ((df['optionType'] == 'call') & (spot_price > df['strike'])) | \
                  ((df['optionType'] == 'put') & (spot_price < df['strike']))
    
    # Add risk-free rate
    df['riskFreeRate'] = risk_free_rate
    
    return df

if __name__ == "__main__":
    import glob
    from data_cleaner import clean_options_data
    
    # Load and clean
    files = glob.glob('data/SPY_options_*.csv')
    df = pd.read_csv(max(files))
    spot = df['spotPrice'].iloc[0]
    
    df_clean = clean_options_data(df)
    df_prepared = prepare_for_iv_calculation(df_clean, spot)
    
    # Save prepared data
    output_file = f"data/SPY_prepared_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_prepared.to_csv(output_file, index=False)
    
    print(f"Prepared data saved to {output_file}")
    print(f"\nData overview:")
    print(df_prepared[['strike', 'marketPrice', 'moneyness', 'timeToExpiry', 'optionType']].describe())