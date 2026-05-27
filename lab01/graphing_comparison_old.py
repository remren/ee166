import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import csv

import fir_verification as data
import fir_TAP63 

import os

# Parameters
TAPS = 63

SAVE_DIR = "./images"
GRAPHING_TN = np.linspace(0, data.t_total, int(data.s_rate * data.t_total))
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

def write_combined_to_csv(filename="combined.csv"):
    """
    Read s_comb from fir_verification data and write to CSV file.
    Format: One integer value per line (scaled for 10-bit signed).
    """
    s_comb = data.x_comb
    
    # Scale the floating point values to 10-bit signed integers (-512 to 511)
    # Find max absolute value for scaling
    max_abs = np.max(np.abs(s_comb))
    if max_abs > 0:
        scaled_data = np.round(s_comb / max_abs * 511).astype(int)
    else:
        scaled_data = np.zeros_like(s_comb, dtype=int)
    
    # Clamp to 10-bit signed range
    scaled_data = np.clip(scaled_data, -512, 511)
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for value in scaled_data:
            writer.writerow([value])
    
    print(f"  Saved {len(scaled_data)} samples to {filename}")
    return scaled_data

def write_filter_taps_to_csv(filename="filter_taps.txt"):
    """
    Write filter coefficients to a text file.
    Format: One integer value per line (scaled for 10-bit signed).
    """
    ## Assuming filter taps are available in data, or using default bandpass filter
    ## For a 63-tap FIR filter with passband around 400 Hz
    # if hasattr(data, 'filter_taps'):
    #     taps = data.filter_taps
    # # else:
    # #     exit("Failed - No taps found")
    # else:
    #     # Generate example 63-tap bandpass filter coefficients
    #     # This is a placeholder - replace with actual filter design
    #     from scipy import signal
    #     nyquist = data.s_rate / 2
    #     low = 350 / nyquist
    #     high = 450 / nyquist
    #     taps = signal.firwin(63, [low, high], pass_zero=False)

    scaled_taps = fir_TAP63.filt_coeff
    
    # # Scale to 10-bit signed integers
    # max_abs = np.max(np.abs(taps))
    # if max_abs > 0:
    #     scaled_taps = np.round(taps / max_abs * 511).astype(int)
    # else:
    #     scaled_taps = np.zeros_like(taps, dtype=int)
    
    # scaled_taps = np.clip(scaled_taps, -512, 511)
    
    with open(filename, 'w', newline='') as f:
        for value in scaled_taps:
            f.write(f"{value}\n")
    
    print(f"  Saved {len(scaled_taps)} filter taps to {filename}")

## *** Graphing Python Results ***

def graph_sin_all(s_400, s_500, s_comb, filename):
    # Graphing combining sinusoids for test data.

    figure, (sp1, sp2, sp3) = plt.subplots(3, 1, figsize=(20, 8))

    # 400 Hz component
    sp1.plot(GRAPHING_TN, s_400, lw=1, color='green', marker='.')
    sp1.grid(True)
    sp1.set_title('400 Hz Sinusoid Component')
    sp1.set_ylabel('Amplitude')
    sp1.set_xlabel('Time (s)')

    # 500 Hz component
    sp2.plot(GRAPHING_TN, s_500, lw=1, color='blue', marker='.')
    sp2.grid(True)
    sp2.set_title('500 Hz Sinusoid Component')
    sp2.set_ylabel('Amplitude')
    sp2.set_xlabel('Time (s)')

    # Combined signal (400 Hz + 500 Hz)
    sp3.plot(GRAPHING_TN, s_comb, lw=1, color='red', marker='.')
    sp3.grid(True)
    sp3.set_title('Combined Sinusoid (400 Hz + 500 Hz)')
    sp3.set_ylabel('Amplitude')
    sp3.set_xlabel('Time (s)')

    figure.suptitle('Sinusoid Components and Combined Signal', fontsize=14, fontweight='bold')
    figure.tight_layout()

    _save(figure, filename)

def graph_sin_comb():
    """Plot filtered output vs. shifted and original 400 Hz references."""
    s_y = data.y
    shifted_400 = data.shifted_400
    s_400 = data.x_400

    figure, (sp1, sp2) = plt.subplots(2, 1, figsize=(20, 8))

    # Top subplot: filtered output vs. time-shifted 400 Hz reference
    sp1.plot(GRAPHING_TN, s_y, lw=1, color="green", marker=".", label="Filtered Output")
    sp1.plot(
        GRAPHING_TN,
        shifted_400,
        lw=1,
        color="red",
        marker=".",
        label="400 Hz (Shifted 30 Samples)",
    )
    sp1.grid(True)
    sp1.set_title("Filtered Output vs. Time-Shifted 400 Hz Sinusoid")
    sp1.set_ylabel("Amplitude")
    sp1.set_xlabel("Time (s)")
    sp1.legend(loc="upper right")

    # Bottom subplot: filtered output vs. original 400 Hz component
    sp2.plot(GRAPHING_TN, s_y, lw=1, color="green", marker=".", label="Filtered Output")
    sp2.plot(
        GRAPHING_TN,
        s_400,
        lw=1,
        color="blue",
        marker=".",
        label="Original 400 Hz",
    )
    sp2.grid(True)
    sp2.set_title("Filtered Output vs. Original 400 Hz Sinusoid")
    sp2.set_ylabel("Amplitude")
    sp2.set_xlabel("Time (s)")
    sp2.legend(loc="upper right")

    figure.suptitle(
        "FIR Filter Output Comparison (Lack of Group Delay)", fontsize=14, fontweight="bold"
    )
    figure.tight_layout()

    _save(figure, "result_conv_overlay.png")

## *** Comparing Python vs. RTL Outputs ***
## Helpers

def float_to_q9(value):
    values = np.asarray(value)
    scaled = np.round(values * SCALE)
    # Q1.8: 1 sign + 1 int + 8 frac = 10 bits total
    # Range: [-512, 511]
    max_val = 2 * SCALE - 1  # 511
    min_val = -2 * SCALE       # -512
    scaled = np.clip(scaled, min_val, max_val)
    return scaled.astype(int)

def q9_to_float(value):
    values = np.asarray(value)
    return values / SCALE

# def float_to_q9(value):
#     """Convert floating point to Q1.9 fixed point"""
#     # Scale and round
#     scaled = round(value * SCALE)
    
#     # Clamp to 10-bit signed range
#     if scaled > 127:
#         scaled = 127
#     elif scaled < -128:
#         scaled = -128
        
#     return scaled

# def q9_to_float(value):
#     """Convert Q1.15 fixed point to floating point"""
#     return value / SCALE

def write_py_s400_output_to_csv(py_output, filename="s400_py_output_float.csv"):
    with open(filename, 'w', newline='') as f:
        for value in py_output:
            f.write(f"{value}\n")
    print(f"  Saved {len(py_output)} output values to {filename}")

def graph_sin_comb_fxp(py_fxp, rtl_fxp):
    """Plot filtered output vs. shifted and original 400 Hz references, but for FXP."""

    figure, (sp1, sp2) = plt.subplots(2, 1, figsize=(20, 8))

    # Top subplot: filtered output vs. time-shifted 400 Hz reference
    sp1.plot(GRAPHING_TN, py_fxp, lw=1, color="green", marker=".", label="Filtered Output")
    sp1.plot(
        GRAPHING_TN,
        rtl_fxp,
        lw=1,
        color="red",
        marker=".",
        label="400 Hz (Shifted 30 Samples)",
    )
    sp1.grid(True)
    sp1.set_title("Filtered Output vs. Time-Shifted 400 Hz Sinusoid")
    sp1.set_ylabel("Amplitude")
    sp1.set_xlabel("Time (s)")
    sp1.legend(loc="upper right")

    # Bottom subplot: filtered output vs. original 400 Hz component
    random_taps = []
    with open("random_taps.csv", 'r') as f:
        for line in f:
            sign = 1
            line = line.strip()
            # print(line[0][0])
            if line[0][0] == '-':
                sign = -1
                # print('neg')
                line = line[1:] # strip the negative so its detected as a numeric
            if line.isnumeric():
                integer_line = int(line)
                value = sign * integer_line
                # print(f"numeric:{line}, sign:{sign}")
                random_taps.append(value)
            else:
                random_taps.append(0)
    print(f"Read: random_taps.csv as input data for random_taps")
    sp2.plot(np.arange(0,63,1), random_taps, lw=1, color="green", marker=".", label="Random Taps")
    # sp2.plot(GRAPHING_TN, rtl_fxp, lw=1, color="green", marker=".", label="Filtered Output")
    # sp2.plot(
    #     GRAPHING_TN,
    #     s_400,
    #     lw=1,
    #     color="blue",
    #     marker=".",
    #     label="Original 400 Hz",
    # )
    sp2.grid(True)
    sp2.set_title("Filtered Output vs. Original 400 Hz Sinusoid")
    sp2.set_ylabel("Amplitude")
    sp2.set_xlabel("Time (s)")
    sp2.legend(loc="upper right")

    figure.suptitle(
        "FIR Filter Output Comparison (Lack of Group Delay)", fontsize=14, fontweight="bold"
    )
    figure.tight_layout()

    _save(figure, "result_conv_overlay_fxp.png")


if __name__ == "__main__":
    
    # Generate CSV files for SystemVerilog testbench
    scaled_data = write_combined_to_csv("s400_500_input_signal.csv")
    write_filter_taps_to_csv("filter_taps.txt")
    
    # Generate plots
    graph_sin_all(data.x_400, data.x_500, data.x_comb, "s_400_500hz_modulated")
    graph_sin_comb()
    print("\nDone. All plots saved to images/")

    write_py_s400_output_to_csv(data.y)

    y_fxp = [float_to_q9(v) for v in data.y]
    y_fxp = np.asarray(y_fxp)
    # print(y_fxp)

    write_py_s400_output_to_csv(y_fxp, "s400_py_output_fxp.csv")

    rtl_fxp = []
    fxp_filename = "output.csv"
    with open(fxp_filename, 'r') as f:
        for line in f:
            sign = 1
            line = line.strip()
            # print(line[0][0])
            if line[0][0] == '-':
                sign = -1
                # print('neg')
                line = line[1:] # strip the negative so its detected as a numeric
            if line.isnumeric():
                integer_line = int(line)
                value = sign * integer_line
                # print(f"numeric:{line}, sign:{sign}")
                rtl_fxp.append(value)
            else:
                rtl_fxp.append(0)
    print(f"Read: {fxp_filename} as input data for rtl_fxp")
    print(rtl_fxp)

    # graph_sin_comb_fxp(y_fxp, rtl_fxp)

    shift = 1
    rtl_fxp_shift = rtl_fxp[shift:]
    for i in range(shift):
        rtl_fxp_shift.append(0)
    # rtl_fxp_shift = 2 * np.asarray(rtl_fxp_shift) # Test scaling to check if there's some weird conversion
    # graph_sin_comb_fxp(y_fxp, rtl_fxp_shift)
    graph_sin_comb_fxp(y_fxp, rtl_fxp_shift[0:len(y_fxp)])


    test_taps = [float_to_q9(v) for v in fir_TAP63.filt_coeff]
    # print(test_taps)
    write_py_s400_output_to_csv(test_taps, filename="test_taps.csv")

    random_taps = []
    with open("random_taps.csv", 'r') as f:
        for line in f:
            sign = 1
            line = line.strip()
            # print(line[0][0])
            if line[0][0] == '-':
                sign = -1
                # print('neg')
                line = line[1:] # strip the negative so its detected as a numeric
            if line.isnumeric():
                integer_line = int(line)
                value = sign * integer_line
                # print(f"numeric:{line}, sign:{sign}")
                random_taps.append(value)
            else:
                random_taps.append(0)
    print(f"Read: random_taps.csv as input data for random_taps")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(np.arange(0, 63, 1), random_taps)
    ax.grid(True)
    ax.set_title("Random Filter Taps")
    ax.set_xlabel("Tap Index")
    ax.set_ylabel("Tap Value")
    _save(fig, "random_taps_plot.png")

    new_input_signal = []
    with open("RTL_s400_500_input_signal.csv", 'r') as f:
        for line in f:
            sign = 1
            line = line.strip()
            # print(line[0][0])
            if line[0][0] == '-':
                sign = -1
                # print('neg')
                line = line[1:] # strip the negative so its detected as a numeric
            if line.isnumeric():
                integer_line = int(line)
                value = sign * integer_line
                # print(f"numeric:{line}, sign:{sign}")
                new_input_signal.append(value)
            else:
                new_input_signal.append(0)
    print(f"Read: RTL_s400_500_input_signal.csv as input data for new_input_signal")
    graph_sin_all(data.x_comb, scaled_data, new_input_signal, "compare_float_vs_scaled.png")
