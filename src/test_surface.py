import pandas as pd
import glob
from visualize_surface import plot_fitted_surface

# Load data with IVs
iv_files = glob.glob('data/SPY_with_iv_*.csv')
df = pd.read_csv(max(iv_files))

# Load calibration results
calib_files = glob.glob('data/SVI_calibration_*.csv')
calibration_df = pd.read_csv(max(calib_files))

print("Plotting fitted surface...")
plot_fitted_surface(df, calibration_df)