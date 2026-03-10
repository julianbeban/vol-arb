import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.black_scholes import *

def test_iv_recovery():
    """Generate prices at known sigmas, verify IV solver recovers them"""
    S, K, T, r = 100, 100, 1.0, 0.05
    test_sigmas = [0.1, 0.2, 0.3, 0.5]
    
    print("Testing IV recovery on synthetic data:\n")
    for true_sigma in test_sigmas:
        call_price = black_scholes_call(S, K, T, r, true_sigma)
        recovered_sigma = implied_volatility_call(call_price, S, K, T, r)
        error = abs(recovered_sigma - true_sigma)
        
        print(f"True σ: {true_sigma:.3f} | Recovered: {recovered_sigma:.3f} | Error: {error:.6f}")
        assert error < 1e-6, "IV recovery failed"
    
    print("\n✓ All tests passed")

if __name__ == "__main__":
    test_iv_recovery()