"""
Wrapper script to run app.py with numpy compatibility fixes for Python 3.13
"""
import os
import sys

# Disable numpy's problematic long double support on Windows + Python 3.13
os.environ['NPY_DISABLE_FLOAT16_SUPPORT'] = '1'
os.environ['OPENBLAS_CORETYPE'] = 'prescott'

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

# Now import and run the app
try:
    import app
    # The app.py module will execute when imported
except Exception as e:
    print(f"Error starting application: {e}")
    sys.exit(1)
