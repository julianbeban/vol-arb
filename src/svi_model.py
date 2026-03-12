import numpy as np
from scipy.optimize import minimize

def svi_formula(k, params):
    """
    SVI parameterization for a single maturity slice
    k: log-moneyness (ln(K/S))
    params: [a, b, rho, m, sigma] - 5 parameters
    Returns: total variance (w = sigma^2 * T)
    """
    a, b, rho, m, sigma = params
    w = a + b * (rho * (k - m) + np.sqrt((k - m)**2 + sigma**2))
    return w

def calibrate_svi_slice(moneyness, iv, tte):
    """
    Calibrate SVI to a single maturity slice
    
    moneyness: array of K/S ratios
    iv: array of implied vols
    tte: time to expiry (constant for this slice)
    
    Returns: optimized parameters [a, b, rho, m, sigma]
    """
    # Convert to log-moneyness
    k = np.log(moneyness)
    
    # Convert IV to total variance
    w_market = iv**2 * tte
    
    # Initial guess
    a0 = np.median(w_market)
    b0 = 0.1
    rho0 = 0.0
    m0 = 0.0
    sigma0 = 0.1
    initial_params = [a0, b0, rho0, m0, sigma0]
    
    # Constraints: -1 < rho < 1, b > 0, sigma > 0
    bounds = [
        (None, None),  # a
        (0.001, None), # b > 0
        (-0.999, 0.999), # -1 < rho < 1
        (None, None),  # m
        (0.001, None)  # sigma > 0
    ]
    
    # Objective: minimize sum of squared errors
    def objective(params):
        w_model = svi_formula(k, params)
        return np.sum((w_model - w_market)**2)
    
    result = minimize(objective, initial_params, bounds=bounds, method='L-BFGS-B')
    
    return result.x if result.success else None

if __name__ == "__main__":
    import pandas as pd
    import glob
    import matplotlib.pyplot as plt
    
    # Load data
    files = glob.glob('data/SPY_with_iv_*.csv')
    df = pd.read_csv(max(files))
    
    # Pick a single maturity (~1 month)
    df_slice = df[
        (df['timeToExpiry'] > 0.08) & 
        (df['timeToExpiry'] < 0.12) &
        (df['optionType'] == 'call')
    ].copy()
    
    tte = df_slice['timeToExpiry'].mean()
    moneyness = df_slice['moneyness'].values
    iv = df_slice['impliedVolatility'].values
    
    print(f"Calibrating SVI to {len(df_slice)} options with ~{tte*365:.0f} days to expiry")
    
    params = calibrate_svi_slice(moneyness, iv, tte)
    
    if params is not None:
        print(f"SVI parameters: a={params[0]:.4f}, b={params[1]:.4f}, rho={params[2]:.4f}, m={params[3]:.4f}, sigma={params[4]:.4f}")
        
        # Plot fit
        k_grid = np.log(np.linspace(0.8, 1.2, 100))
        w_fitted = svi_formula(k_grid, params)
        iv_fitted = np.sqrt(w_fitted / tte)
        
        plt.figure(figsize=(10, 6))
        plt.scatter(moneyness, iv, alpha=0.6, label='Market IV')
        plt.plot(np.exp(k_grid), iv_fitted, 'r-', linewidth=2, label='SVI Fit')
        plt.xlabel('Moneyness (K/S)')
        plt.ylabel('Implied Volatility')
        plt.title('SVI Model Fit')
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        print("Calibration failed")