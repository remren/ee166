import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import csv

import os

# Parameters
SAVE_DIR = "./images"
FXP_FRAC = 8
FXP_INT  = 1
SCALE = int(2 ** FXP_FRAC) # for 10-bit, 1 signed bit, 1 integer bit, 8 fractional bits.

# Plotting Helpers
def _save(fig, filename):
    """Save figure to images/ and close."""
    os.makedirs(SAVE_DIR, exist_ok=True)
    path = os.path.join(SAVE_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")

# Conversion Helpers
def float_to_fxp(value):
    scaled = round(value * SCALE)
    
    # 10-bit signed range: -2^(10-1) to 2^(10-1)-1
    min_val = -2* FXP_INT*SCALE
    max_val = 2* FXP_INT*SCALE-1
    
    # Clamp to range
    if scaled > max_val:
        scaled = max_val
    elif scaled < min_val:
        scaled = min_val
    return scaled

# def float_to_fxp(value):
#     values = np.asarray(value)
#     scaled = np.round(values * SCALE)
#     # Q1.8: 1 sign + 1 int + 8 frac = 10 bits total
#     # Range: [-512, 511]
#     max_val = 2 * SCALE - 1  # 511
#     min_val = -2 * SCALE       # -512
#     scaled = np.clip(scaled, min_val, max_val)
#     return scaled.astype(int)

def float_to_fxp_np(value):
    values = np.asarray(value)
    scaled = np.round(values * SCALE)
    # Q1.8: 1 sign + 1 int + 8 frac = 10 bits total
    # Range: [-512, 511]
    max_val = 2 * SCALE - 1  # 511
    min_val = -2 * SCALE       # -512
    scaled = np.clip(scaled, min_val, max_val)
    return scaled.astype(int)

def fxp_to_float(value):
    values = np.asarray(value)
    return values / SCALE

if __name__ == "__main__":
   if __name__ == "__main__":
    # Test parameters
    NUM_TESTS = 100000
    RANGE_MIN = -2.0
    RANGE_MAX = 2.0
    
    print(f"Testing {NUM_TESTS:,} random numbers between {RANGE_MIN} and {RANGE_MAX}...")
    print(f"SCALE = {SCALE} (fixed-point with {FXP_FRAC} fractional bits)")
    print(f"Integer range: [{-SCALE}, {SCALE-1}]")
    print("-" * 60)
    
    # Test 1: Detailed comparison with proper type handling
    np.random.seed(42)
    
    # Generate test values
    test_values = []
    test_values.extend(np.random.uniform(RANGE_MIN, RANGE_MAX, NUM_TESTS // 3))
    test_values.extend(np.random.uniform(-1.1, 1.1, NUM_TESTS // 3))
    test_values.extend(np.random.uniform(-5.0, 5.0, NUM_TESTS // 3))
    test_values = np.array(test_values)
    
    # Convert using both methods
    results_fxp = np.array([float_to_fxp(x) for x in test_values], dtype=np.int32)
    results_np = float_to_fxp_np(test_values)
    
    # Compare (convert np results to int for comparison)
    mismatches = results_fxp != results_np.astype(np.int32)
    error_indices = np.where(mismatches)[0]
    
    print(f"Total tests: {len(test_values):,}")
    print(f"Mismatches: {len(error_indices):,}")
    print(f"Match rate: {(1 - len(error_indices)/len(test_values))*100:.2f}%")
    print("-" * 60)
    
    if len(error_indices) > 0:
        print("\nAnalyzing mismatches...")
        
        # Categorize the errors
        error_analysis = {
            'clipping_differences': 0,
            'rounding_differences': 0,
            'type_related': 0,
            'other': 0
        }
        
        print("\nFirst 20 mismatches:")
        print(f"{'Index':<8} {'Input':<15} {'Scaled':<15} {'Round':<10} {'fxp':<8} {'np':<8} {'np(int)':<8} {'np(float)':<12}")
        print("-" * 110)
        
        for idx in error_indices[:20]:
            val = test_values[idx]
            scaled = val * SCALE
            rounded = round(scaled)
            res_fxp = results_fxp[idx]
            res_np_float = results_np[idx]
            res_np_int = int(res_np_float)
            
            print(f"{idx:<8} {val:<15.6f} {scaled:<15.6f} {rounded:<10.2f} "
                  f"{res_fxp:<8} {res_np_int:<8} {res_np_int:<8} {res_np_float:<12.6f}")
            
            # Categorize the error
            if res_fxp != res_np_int:
                if abs(scaled) >= SCALE:
                    error_analysis['clipping_differences'] += 1
                elif scaled == int(scaled) + 0.5 or scaled == int(scaled) - 0.5:
                    error_analysis['rounding_differences'] += 1
                elif isinstance(res_np_float, np.floating):
                    error_analysis['type_related'] += 1
                else:
                    error_analysis['other'] += 1
        
        print(f"\nError Categories:")
        for category, count in error_analysis.items():
            print(f"  {category}: {count}")
    
    # Test 2: Edge cases with detailed analysis
    print("\n" + "=" * 60)
    print("EDGE CASE ANALYSIS")
    print("=" * 60)
    
    edge_cases = [
        (0.0, "zero"),
        (0.5, "half"),
        (-0.5, "negative half"),
        (1.0, "max positive before clamp"),
        (-1.0, "min negative before clamp"),
        (SCALE-1/SCALE, "near max positive"),
        (-SCALE/SCALE, "exact min negative"),
        (100.0, "extreme positive"),
        (-100.0, "extreme negative"),
        (0.00390625, "1/256 (resolution)"),
        (-0.00390625, "-1/256"),
        (0.001953125, "0.5/256 (half resolution)"),
    ]
    
    print(f"{'Value':<15} {'Description':<30} {'Scaled':<12} {'Rounded':<10} {'fxp':<8} {'np':<8} {'Match':<8}")
    print("-" * 95)
    
    for val, desc in edge_cases:
        scaled = val * SCALE
        rounded = round(scaled)
        res_fxp = float_to_fxp(val)
        res_np = float_to_fxp_np(val)
        res_np_int = int(res_np)
        match = "✅" if res_fxp == res_np_int else "❌"
        
        print(f"{val:<15.10f} {desc:<30} {scaled:<12.6f} {rounded:<10.2f} "
              f"{res_fxp:<8} {res_np_int:<8} {match:<8}")
    
    # Test 3: Show the actual return types
    print("\n" + "=" * 60)
    print("TYPE ANALYSIS")
    print("=" * 60)
    
    test_val = 0.5
    result_fxp = float_to_fxp(test_val)
    result_np = float_to_fxp_np(test_val)
    
    print(f"Input: {test_val}")
    print(f"float_to_fxp return: {result_fxp} (type: {type(result_fxp).__name__})")
    print(f"float_to_fxp_np return: {result_np} (type: {type(result_np).__name__})")
    print(f"Are they equal as ints? {int(result_fxp) == int(result_np)}")
    
    # Test 4: My own tests
    print("\n" + "=" * 60)
    print("MY OWN TESTS")
    print("=" * 60)

    # testing fractional max/min, as the integer bit would only be adding +/-1 seperately!
    values = [-1, -0.5, 0, 0.5, 1]
    values_fxp = [-1*SCALE*FXP_INT, -1*SCALE*FXP_INT/2, 0, FXP_INT*SCALE/2, FXP_INT*SCALE-1]
    print(f"values: {values}")
    print(f"test: {float_to_fxp(1)}")
    print(f"float_to_fxp: {[float_to_fxp(v) for v in values]}")
    print(f"float_to_fxp_np: {float_to_fxp_np(values)}")
    print(f"values_fxp: {values_fxp}")
    print(f"fxp_to_float: {fxp_to_float(values_fxp)}")