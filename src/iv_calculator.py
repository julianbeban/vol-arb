import pandas as pd
import numpy as np
from black_scholes import implied_volatility_call, implied_volatility_put

def calculate_iv_for_chain(df):
    """
    Calculate implied volatility for each option in the chain
    """
    df = df.copy()
    
    ivs = []
    for idx, row in df.iterrows():
        if row['optionType'] == 'call':
            iv = implied_volatility_call(
                price=row['marketPrice'],
                S=row['spotPrice'],
                K=row['strike'],
                T=row['timeToExpiry'],
                r=row['riskFreeRate']
            )
        else:  # put
            iv = implied_volatility_put(
                price=row['marketPrice'],
                S=row['spotPrice'],
                K=row['strike'],
                T=row['timeToExpiry'],
                r=row['riskFreeRate']
            )
        
        ivs.append(iv)
    
    df['impliedVolatility'] = ivs
    
    # Remove failed calculations
    df = df.dropna(subset=['impliedVolatility'])
    
    # Filter unrealistic IVs (likely bad data)
    df = df[(df['impliedVolatility'] > 0.01) & (df['impliedVolatility'] < 5.0)]
    
    return df

if __name__ == "__main__":
    import glob
    
    # Load prepared data
    files = glob.glob('data/SPY_prepared_*.csv')
    df = pd.read_csv(max(files))
    
    print("Calculating implied volatilities...")
    df_with_iv = calculate_iv_for_chain(df)
    
    print(f"\nSuccessfully calculated IV for {len(df_with_iv)} options")
    print(f"\nIV Statistics:")
    print(df_with_iv['impliedVolatility'].describe())
    
    # Save
    from datetime import datetime
    output_file = f"data/SPY_with_iv_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_with_iv.to_csv(output_file, index=False)
    print(f"\nSaved to {output_file}")