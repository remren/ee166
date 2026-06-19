import matplotlib.pyplot as plt
import numpy as np
import os

# Configuration
SAVE_DIR = "images"

# *** Plotting Helpers ***
def _save(fig, filename):
    """Save figure to images/ and close."""
    os.makedirs(SAVE_DIR, exist_ok=True)
    path = os.path.join(SAVE_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")

# Data from sim_run_data.py
ahb_out = [
    0, 0, 0, -2, -3, -3, -3, 1, 5, 1, -6, -8, 2, 11, 3, -12, -12, 6, 18, 2,
    -23, -15, 19, 28, -9, -41, -11, 46, 40, -45, -87, 30, 226, 268, 57, -193,
    -193, 50, 222, 99, -153, -201, 19, 214, 121, -138, -215, 2, 221, 136, -141,
    -226, 2, 229, 138, -147, -228, 5, 230, 137, -147, -231, 0, 229, 144, -141,
    -234, -4, 233, 148, -145, -238, 0, 237, 144, -149, -234, 4, 233, 140, -145,
    -230, 0, 229, 144, -141, -234, -4, 233, 148, -145, -238, 0, 237, 144, -149,
    -234, 4, 233, 140, -145, -230, 0, 229, 144, -141, -234, -4, 233, 148, -145,
    -238, 0, 237, 144, -149, -234, 4, 233, 140, -145, -230, 0, 229, 144, -141,
    -234, -4, 233, 148, -145, -238, 0, 237, 144, -149, -234, 4, 233, 140, -145,
    -230, 0, 229, 144, -141, -234, -4, 233, 148, -145, -238, 0, 237, 144, -149,
    -234, 4, 233, 140, -145, -230, 0, 229, 144, -141, -234, -4, 233, 148, -145,
    -238, 0, 237, 144, -149, -234, 4, 233, 140, -145, -230, 0, 229, 144, -141,
    -234, -4, 233, 148, -145, -238, 0, 237, 144, -149, -234, 4, 233, 140, -145,
    -230, 0, 231, 146, -138, -231, -6, 227, 146, -139, -230, -3, 225, 140, -137,
    -222, -3, 214, 137, -122, -215, -20, 200, 152, -100, -223, -51, 192, 192,
    -58, -269, -227, -31, 86, 44, -41, -47, 10, 40, 8, -29, -20, 14, 22, -3,
    -19, -7, 11, 11, -4, -12, -3, 7, 5, -2, -6, -2, 2, 2, 2, 1, 0
]

# Data from RTL_output.csv - this is what you provided in the message
rtl_output = [
    0, 0, 0, -2, -3, -3, -3, 1, 5, 1, -6, -8, 2, 11, 3, -12, -12, 6, 18, 2,
    -23, -15, 19, 28, -9, -41, -11, 46, 40, -45, -87, 30, 226, 268, 57, -193,
    -193, 50, 222, 99, -153, -201, 19, 214, 121, -138, -215, 2, 221, 136, -141,
    -226, 2, 229, 138, -147, -228, 5, 230, 137, -147, -231, 0, 229, 144, -141,
    -234, -4, 233, 148, -145, -238, 0, 237, 144, -149, -234, 4, 233, 140, -145,
    -230, 0, 229, 144, -141, -234, -4, 233, 148, -145, -238, 0, 237, 144, -149,
    -234, 4, 233, 140, -145, -230, 0, 229, 144, -141, -234, -4, 233, 148, -145,
    -238, 0, 237, 144, -149, -234, 4, 233, 140, -145, -230, 0, 229, 144, -141,
    -234, -4, 233, 148, -145, -238, 0, 237, 144, -149, -234, 4, 233, 140, -145,
    -230, 0, 229, 144, -141, -234, -4, 233, 148, -145, -238, 0, 237, 144, -149,
    -234, 4, 233, 140, -145, -230, 0, 229, 144, -141, -234, -4, 233, 148, -145,
    -238, 0, 237, 144, -149, -234, 4, 233, 140, -145, -230, 0, 229, 144, -141,
    -234, -4, 233, 148, -145, -238, 0, 237, 144, -149, -234, 4, 233, 140, -145,
    -230, 0, 231, 146, -138, -231, -6, 227, 146, -139, -230, -3, 225, 140, -137,
    -222, -3, 214, 137, -122, -215, -20, 200, 152, -100, -223, -51, 192, 192,
    -58, -269, -227, -31, 86, 44, -41, -47, 10, 40, 8, -29, -20, 14, 22, -3,
    -19, -7, 11, 11, -4, -12, -3, 7, 5, -2, -6, -2, 2, 2, 2, 1, 0
]

# Verify if they are truly identical
ahb_array = np.array(ahb_out)
rtl_array = np.array(rtl_output)

print(f"AHB array length: {len(ahb_array)}")
print(f"RTL array length: {len(rtl_array)}")
print(f"Arrays identical? {np.array_equal(ahb_array, rtl_array)}")

# Find where they differ
differences = ahb_array != rtl_array
diff_indices = np.where(differences)[0]

if len(diff_indices) == 0:
    print("\n✓ CONFIRMED: The arrays are EXACT matches! No differences found.")
    
    # Create plot showing they're identical
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: Signal overlay
    ax1.plot(ahb_out, 'b-', label='AHB Output (sim_run_data)', linewidth=2, alpha=0.7)
    ax1.plot(rtl_output, 'r--', label='RTL Output (RTL_output.csv)', linewidth=2, alpha=0.7)
    ax1.set_xlabel('Sample Index')
    ax1.set_ylabel('Value')
    ax1.set_title('Comparison: AHB Output vs RTL Output (IDENTICAL MATCH)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.text(0.5, 0.5, '✓ EXACT MATCH\nAll values identical', 
             transform=ax1.transAxes, ha='center', va='center',
             fontsize=20, color='green', alpha=0.3,
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Plot 2: Show the data with markers
    ax2.plot(ahb_out[:50], 'bo-', label='First 50 samples', markersize=4, linewidth=1)
    ax2.set_xlabel('Sample Index')
    ax2.set_ylabel('Value')
    ax2.set_title('First 50 Samples (Identical Data)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    _save(fig, "ahb_vs_rtl_identical_match.png")
    
    # Print some sample comparisons
    print("\nSample spot checks (first 10 values):")
    for i in range(10):
        print(f"  [{i}]: AHB={ahb_out[i]:4d}, RTL={rtl_output[i]:4d} - Match: ✓")
        
else:
    print(f"\nFound {len(diff_indices)} differences!")
    print(f"First 20 different indices: {diff_indices[:20]}")
    print("\nDetailed differences (first 10):")
    for i, idx in enumerate(diff_indices[:10]):
        print(f"  [{idx}]: AHB={ahb_out[idx]:4d}, RTL={rtl_output[idx]:4d}, Diff={ahb_out[idx] - rtl_output[idx]:4d}")
    
    # Create comparison plot with differences highlighted
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: Signal overlay with difference highlights
    ax1.plot(ahb_out, 'b-', label='AHB Output', linewidth=1.5, alpha=0.8)
    ax1.plot(rtl_output, 'r--', label='RTL Output', linewidth=1.5, alpha=0.8)
    if len(diff_indices) > 0:
        ax1.scatter(diff_indices, [ahb_out[i] for i in diff_indices], 
                   color='yellow', s=50, zorder=5, label=f'Differences ({len(diff_indices)})')
    ax1.set_xlabel('Sample Index')
    ax1.set_ylabel('Value')
    ax1.set_title('Comparison: AHB Output vs RTL Output')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Difference
    diff_values = ahb_array - rtl_array
    ax2.stem(range(len(diff_values)), diff_values, linefmt='g-', markerfmt='go', basefmt='k-')
    ax2.set_xlabel('Sample Index')
    ax2.set_ylabel('Difference (AHB - RTL)')
    ax2.set_title(f'Differences ({len(diff_indices)} mismatches)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    _save(fig, "ahb_vs_rtl_with_differences.png")