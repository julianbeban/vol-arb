import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_iv_surface(df, option_type='call'):
    """
    Create 3D surface plot of implied volatility
    """
    df_filtered = df[df['optionType'] == option_type].copy()
    
    # Create pivot table: rows=moneyness, cols=timeToExpiry
    pivot = df_filtered.pivot_table(
        values='impliedVolatility',
        index='moneyness',
        columns='timeToExpiry',
        aggfunc='mean'
    )
    
    # Create meshgrid for 3D plot
    X = pivot.columns.values  # Time to expiry
    Y = pivot.index.values    # Moneyness
    X, Y = np.meshgrid(X, Y)
    Z = pivot.values
    
    # Plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    
    ax.set_xlabel('Time to Expiry (years)')
    ax.set_ylabel('Moneyness (K/S)')
    ax.set_zlabel('Implied Volatility')
    ax.set_title(f'Implied Volatility Surface - {option_type.upper()}s')
    
    fig.colorbar(surf, shrink=0.5)
    plt.show()
    
    return pivot

def plot_volatility_smile(df, min_tte=0.08, max_tte=0.12):
    """
    Plot volatility smile for near-term options
    """
    df_filtered = df[
        (df['timeToExpiry'] >= min_tte) & 
        (df['timeToExpiry'] <= max_tte)
    ].copy()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Calls
    calls = df_filtered[df_filtered['optionType'] == 'call']
    ax1.scatter(calls['moneyness'], calls['impliedVolatility'], alpha=0.6, label='Market IV')
    ax1.set_xlabel('Moneyness (K/S)')
    ax1.set_ylabel('Implied Volatility')
    ax1.set_title('Call Volatility Smile')
    ax1.axvline(x=1.0, color='red', linestyle='--', label='ATM')
    ax1.legend()
    ax1.grid(True)
    
    # Puts
    puts = df_filtered[df_filtered['optionType'] == 'put']
    ax2.scatter(puts['moneyness'], puts['impliedVolatility'], alpha=0.6, label='Market IV', color='orange')
    ax2.set_xlabel('Moneyness (K/S)')
    ax2.set_ylabel('Implied Volatility')
    ax2.set_title('Put Volatility Smile')
    ax2.axvline(x=1.0, color='red', linestyle='--', label='ATM')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    import glob
    
    # Load data with IVs
    files = glob.glob('data/SPY_with_iv_*.csv')
    df = pd.read_csv(max(files))
    
    print("Plotting volatility smile for ~1 month options...")
    plot_volatility_smile(df, min_tte=0.08, max_tte=0.12)
    
    print("\nPlotting full IV surface...")
    pivot = plot_iv_surface(df, option_type='call')
    
    print("\nSurface grid shape:", pivot.shape)