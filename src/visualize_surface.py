import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_fitted_surface(df, calibration_df):
    
    """
    Plot fitted SVI surface vs market data
    """
    from svi_model import svi_formula
    
    fig = plt.figure(figsize=(14, 6))
    
    # Create grid
    tte_range = np.linspace(calibration_df['timeToExpiry'].min(), 
                            calibration_df['timeToExpiry'].max(), 20)
    k_range = np.linspace(-0.2, 0.2, 50)  # log-moneyness
    
    TTE, K = np.meshgrid(tte_range, k_range)
    IV_fitted = np.zeros_like(TTE)
    
    # Interpolate SVI parameters and compute fitted IV
    for i, tte in enumerate(tte_range):
        # Find nearest calibrated slice
        nearest_idx = np.argmin(np.abs(calibration_df['timeToExpiry'] - tte))
        params = calibration_df.iloc[nearest_idx][['a', 'b', 'rho', 'm', 'sigma']].values
        
        w = svi_formula(k_range, params)
        IV_fitted[:, i] = np.sqrt(w / tte)
    
    # Plot fitted surface
    ax1 = fig.add_subplot(121, projection='3d')
    surf = ax1.plot_surface(TTE, np.exp(K), IV_fitted, cmap='viridis', alpha=0.8)
    ax1.set_xlabel('Time to Expiry')
    ax1.set_ylabel('Moneyness (K/S)')
    ax1.set_zlabel('Implied Volatility')
    ax1.set_title('Fitted SVI Surface')
    
    # Plot market data points
    ax2 = fig.add_subplot(122, projection='3d')
    df_calls = df[df['optionType'] == 'call']
    ax2.scatter(df_calls['timeToExpiry'], df_calls['moneyness'], 
                df_calls['impliedVolatility'], alpha=0.3, s=10)
    ax2.set_xlabel('Time to Expiry')
    ax2.set_ylabel('Moneyness (K/S)')
    ax2.set_zlabel('Implied Volatility')
    ax2.set_title('Market Data')
    
    plt.tight_layout()
    plt.show()