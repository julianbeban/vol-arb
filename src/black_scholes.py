import numpy as np
from scipy.stats import norm
from scipy.optimize import newton


def black_scholes_call(S, K, T, r, sigma):
    """
    S: spot price
    K: strike price
    T: time to maturity (years)
    r: risk-free rate
    sigma: volatility
    """
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    call_price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    return call_price

def black_scholes_put(S, K, T, r, sigma):
    """Put option price via put-call parity"""
    call_price = black_scholes_call(S, K, T, r, sigma)
    put_price = call_price - S + K*np.exp(-r*T)
    return put_price

def implied_volatility_call(price, S, K, T, r, initial_guess=0.3, max_iter=100):
    """
    Solve for sigma such that BS(sigma) = market_price
    Uses Newton-Raphson method
    """
    def objective(sigma):
        return black_scholes_call(S, K, T, r, sigma) - price
    
    try:
        iv = newton(objective, initial_guess, maxiter=max_iter)
        return iv if iv > 0 else None
    except:
        return None

def implied_volatility_put(price, S, K, T, r, initial_guess=0.3, max_iter=100):
    """IV solver for puts"""
    def objective(sigma):
        return black_scholes_put(S, K, T, r, sigma) - price
    
    try:
        iv = newton(objective, initial_guess, maxiter=max_iter)
        return iv if iv > 0 else None
    except:
        return None

# Test
if __name__ == "__main__":
    S = 100    # Stock at $100
    K = 100    # Strike at $100 (ATM)
    T = 1.0    # 1 year to expiry
    r = 0.05   # 5% risk-free rate
    sigma = 0.2  # 20% volatility
    
    call = black_scholes_call(S, K, T, r, sigma)
    put = black_scholes_put(S, K, T, r, sigma)
    
    print(f"Call price: ${call:.2f}")
    print(f"Put price: ${put:.2f}")

    print("\n--- IV Recovery Test ---")
    market_call_price = 10.45
    recovered_iv = implied_volatility_call(market_call_price, S, K, T, r)
    print(f"Original sigma: {sigma:.4f}")
    print(f"Recovered IV: {recovered_iv:.4f}")