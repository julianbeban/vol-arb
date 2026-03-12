import pandas as pd
import numpy as np
from svi_model import calibrate_svi_slice, svi_formula

def calibrate_full_surface(df, option_type='call'):
    """
    Calibrate SVI model to all maturity slices
    """
    df_filtered = df[df['optionType'] == option_type].copy()
    
    # Group by similar maturities (bucket into ~weekly intervals)
    df_filtered['tte_bucket'] = (df_filtered['timeToExpiry'] * 52).round() / 52
    
    calibrations = []
    
    for tte_bucket, group in df_filtered.groupby('tte_bucket'):
        if len(group) < 5:  # Need enough points to calibrate
            continue
        
        moneyness = group['moneyness'].values
        iv = group['impliedVolatility'].values
        tte = group['timeToExpiry'].mean()
        
        params = calibrate_svi_slice(moneyness, iv, tte)
        
        if params is not None:
            calibrations.append({
                'timeToExpiry': tte,
                'a': params[0],
                'b': params[1],
                'rho': params[2],
                'm': params[3],
                'sigma': params[4],
                'num_points': len(group)
            })
    
    return pd.DataFrame(calibrations)

if __name__ == "__main__":
    import glob
    from datetime import datetime
    
    # Load data
    files = glob.glob('data/SPY_with_iv_*.csv')
    df = pd.read_csv(max(files))
    
    print("Calibrating SVI across all maturities...")
    calibration_results = calibrate_full_surface(df, option_type='call')
    
    print(f"\nCalibrated {len(calibration_results)} maturity slices")
    print(calibration_results)
    
    # Save calibration parameters
    output_file = f"data/SVI_calibration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    calibration_results.to_csv(output_file, index=False)
    print(f"\nSaved to {output_file}")