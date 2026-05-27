import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import csv

import os

# Parameters
TAPS = 63
SAVE_DIR = "./images"
FXP_FRAC = 8
FXP_INT  = 1
SCALE = int(2 ** FXP_FRAC) # for 10-bit, 1 signed bit, 1 integer bit, 8 fractional bits.

# *** Plotting Helpers ***
def _save(fig, filename):
    """Save figure to images/ and close."""
    os.makedirs(SAVE_DIR, exist_ok=True)
    path = os.path.join(SAVE_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")

# *** Conversion Helpers ***

# def float_to_fxp(value):
#     values = np.asarray(value)
#     scaled = np.round(values * SCALE)
#     # Q1.8: range is [-2^(INT_BITS), 2^(INT_BITS) - 2^(-FRAC_BITS)]
#     max_val = (2 ** FXP_INT) * SCALE - 1  
#     min_val = -(2 ** FXP_INT) * SCALE
#     scaled = np.clip(scaled, min_val, max_val)
#     return scaled.astype(int)

# def fxp_to_float(value):
#     values = np.asarray(value)
#     return values / SCALE

# def float_to_fxp(value):
#     values = np.asarray(value)
#     scaled = np.round(values * SCALE)
#     scaled = np.clip(scaled, -FXP_INT*SCALE, FXP_INT*SCALE-1)
#     return scaled.astype(int)

def float_to_fxp(value):
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

# *** File Reading and Writing Helpers ***

def write_array_to_csv(array, filename: str):
    """
    Read an array writes its contents to an CSV file.
    Format: One integer value per line (scaled for 10-bit signed).
    """

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for value in array:
            writer.writerow([value])
    
    print(f"  Saved {len(array)} values to {filename}")

 # Code to process RTL csv output and return as an array
def read_array_from_csv(filename: str):
    arr = []
    with open(filename, 'r') as f:
        for line in f:
            sign = 1
            line = line.strip()
            if line[0][0] == '-':
                sign = -1
                line = line[1:] # strip the negative so its detected as a numeric
            if line.isnumeric():
                integer_line = int(line)
                value = sign * integer_line
                # print(f"numeric:{line}, sign:{sign}")
                arr.append(value)
            else:
                arr.append(0)
    print(f"Read: {filename} as input data for returned array")
    return arr

# *** Graphing Functions ***
def graph_sin_all(x_arr, s_400, s_500, s_comb, filename):
    # Graphing combining sinusoids for test data.

    figure, (sp1, sp2, sp3) = plt.subplots(3, 1, figsize=(20, 8))

    # 400 Hz component
    sp1.plot(x_arr, s_400, lw=1, color='green', marker='.')
    sp1.grid(True)
    sp1.set_title('400 Hz Sinusoid Component')
    sp1.set_ylabel('Amplitude')
    sp1.set_xlabel('Time (s)')

    # 500 Hz component
    sp2.plot(x_arr, s_500, lw=1, color='blue', marker='.')
    sp2.grid(True)
    sp2.set_title('500 Hz Sinusoid Component')
    sp2.set_ylabel('Amplitude')
    sp2.set_xlabel('Time (s)')

    # Combined signal (400 Hz + 500 Hz)
    sp3.plot(x_arr, s_comb, lw=1, color='red', marker='.')
    sp3.grid(True)
    sp3.set_title('Combined Sinusoid (400 Hz + 500 Hz)')
    sp3.set_ylabel('Amplitude')
    sp3.set_xlabel('Time (s)')

    figure.suptitle('Sinusoid Components and Combined Signal', fontsize=14, fontweight='bold')
    figure.tight_layout()

    _save(figure, filename)

def graph_float_fxp_conversion_error(x_arr,
                                    float_orig,
                                    float_conv,
                                    float_diff,
                                    average,
                                    filename):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_arr,
            float_orig,
            lw=4,
            markersize=15,
            color="green", marker=".", label="s_comb Original Float")
    ax.plot(x_arr,
            float_conv,
            lw=1, color="blue", marker=".", label="s_comb to FXP then to Float")
    ax.plot(x_arr,
            float_diff,
            lw=1, color="red", marker=".",
            label=f"Error (Avg:{average})")
    ax.grid(True)
    ax.set_title("Error from Float to FXP and FXP to Float Conversions")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.legend(loc="upper right")    
    _save(fig, filename)

def graph_group_delay_comp(x_arr,
                           float_s_400,
                           float_s_y,
                           float_s_400_grp_delay_comp,
                           filename):
    """Plot filtered output vs. shifted and original 400 Hz references."""

    figure, (sp1, sp2) = plt.subplots(2, 1, figsize=(20, 8))

    # Top subplot: filtered output vs. time-shifted 400 Hz reference
    sp1.plot(x_arr,
             float_s_y, 
             lw=1, color="green", marker=".", label="Filtered Output")
    sp1.plot(
        x_arr,
        float_s_400_grp_delay_comp,
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
    sp2.plot(x_arr,
             float_s_y,
             lw=1, color="green", marker=".", label="Filtered Output")
    sp2.plot(
        x_arr,
        float_s_400,
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

    _save(figure, filename)

# *** OLD STUFF BELOW ***

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
    """Convert floating point to Q1.9 fixed point"""
    # Scale and round
    scaled = round(value * SCALE)
    
    # Clamp to 10-bit signed range
    if scaled > 127:
        scaled = 127
    elif scaled < -128:
        scaled = -128
        
    return scaled

def q9_to_float(value):
    """Convert Q1.15 fixed point to floating point"""
    return value / SCALE

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

# *** Main Functions *** 
# 1. Create CSV with combined sinusoids as input file for RTL testbench


if __name__ == "__main__":
    import fir_verification as signal_data

    s_400 = signal_data.x_400
    s_500 = signal_data.x_500
    s_comb = signal_data.x_comb # Combined s400 and s500

    s_y    = signal_data.y # Python Result of FIR Filter

    # 1. Create CSV with combined sinusoids as input file for RTL testbench
    print("\n" + "=" * 60)
    print("1. Create input data CSV for RTL")
    print("=" * 60)
    fxp_s_comb = float_to_fxp(s_comb)
    write_array_to_csv(fxp_s_comb, "RTL_s400_500_input_signal.csv")
    
    # 2. Convert, check against TFilter, and write filter coefficients to CSV for RTL
    print("\n" + "=" * 60)
    print("2. Write filter coefficients to CSV for RTL")
    print("=" * 60)
    import TFilter_TAP63_double, TFilter_TAP63_fxp_Q1_8

    tfilter_float_taps = TFilter_TAP63_double.filt_coeff
    tfilter_q1_8_taps  = TFilter_TAP63_fxp_Q1_8.filt_coeff

    fxp_taps   = float_to_fxp(tfilter_float_taps)
    print(f"Correct Float to FXP for FIR Filter: {tfilter_q1_8_taps == fxp_taps}")

    write_array_to_csv(fxp_taps, "RTL_filter_taps.csv")

    # 3. Graph and save s400 and s500, then combining in float
    print("\n" + "=" * 60)
    print("3. Graph the sinusoids and their combined result")
    print("=" * 60)
    GRAPHING_TN = np.linspace(0,
                              signal_data.t_total,
                              int(signal_data.s_rate * signal_data.t_total))

    graph_sin_all(GRAPHING_TN, s_400, s_500, s_comb, "s_400_500hz_modulated.png")


    # 4. Convert float comb -> fxp -> back into float
    #    graph the comparison, losses from conversion?
    print("\n" + "=" * 60)
    print("4. Graph the error from conversions")
    print("=" * 60)

    b2b_s_comb = fxp_to_float(float_to_fxp(s_comb))
    diff_check = s_comb - b2b_s_comb
    # print(f"s_comb: {s_comb}")
    # print(f"b2b_s_comb: {b2b_s_comb}")
    # print(f"diff_check: {diff_check}")
    graph_float_fxp_conversion_error(GRAPHING_TN,
                                     s_comb,
                                     b2b_s_comb,
                                     diff_check,
                                     np.average(diff_check),
                                     "conversion_error.png")

    # 5. Graph the compensation from group delay all in float
    print("\n" + "=" * 60)
    print("5. Graph the comparison of having group delay compensated")
    print("=" * 60)

    s_shifted_400 = signal_data.shifted_400
    graph_group_delay_comp(GRAPHING_TN,
                           s_400,
                           s_y,
                           s_shifted_400,
                           "result_conv_overlay.png")

    # 6. Write Python input signal to CSV for RTL
    # need to grab the longer timespace + signal
    print("\n" + "=" * 60)
    print("6. Produce a longer input signal for RTL")
    print("=" * 60)

    # 0. Extend s_comb to a longer linspace
    t_total = 0.1 # in sec, longer than 0.08 from signal_data.t_total
    s_rate = signal_data.s_rate
    x_400, tn_400 = signal_data.create_sin(1, 400, 0, s_rate, t_total)
    x_500, tn_500 = signal_data.create_sin(1, 500, 0, s_rate, t_total)

    s_comb_longer = x_400 + x_500 # Combined sinusoid input data, but longer for later graphing

    fxp_s_comb_longer = float_to_fxp(s_comb_longer)
    write_array_to_csv(fxp_s_comb_longer, "RTL_s400_500_input_signal_longer.csv")

    # X. graph python vs. rtl
    # X. take fxp_comparison from other, and obtain impulses
    # X. compare and get error, rms



    # X. Compare sinusoids


    # write_filter_taps_to_csv("filter_taps.txt")

    # y_fxp = [float_to_q9(v) for v in data.y]
    # y_fxp = np.asarray(y_fxp)
    # # print(y_fxp)

    # write_py_s400_output_to_csv(y_fxp, "s400_py_output_fxp.csv")

    ## Code to process RTL csv output and save as a 
    # rtl_fxp = []
    # fxp_filename = "output.csv"
    # with open(fxp_filename, 'r') as f:
    #     for line in f:
    #         sign = 1
    #         line = line.strip()
    #         # print(line[0][0])
    #         if line[0][0] == '-':
    #             sign = -1
    #             # print('neg')
    #             line = line[1:] # strip the negative so its detected as a numeric
    #         if line.isnumeric():
    #             integer_line = int(line)
    #             value = sign * integer_line
    #             # print(f"numeric:{line}, sign:{sign}")
    #             rtl_fxp.append(value)
    #         else:
    #             rtl_fxp.append(0)
    # print(f"Read: {fxp_filename} as input data for rtl_fxp")
    # print(rtl_fxp)

    # # graph_sin_comb_fxp(y_fxp, rtl_fxp)

    # shift = 2
    # rtl_fxp_shift = rtl_fxp[shift:]
    # for i in range(shift):
    #     rtl_fxp_shift.append(0)
    # # rtl_fxp_shift = 2 * np.asarray(rtl_fxp_shift) # Test scaling to check if there's some weird conversion
    # graph_sin_comb_fxp(y_fxp, rtl_fxp_shift)

    # test_taps = [float_to_q9(v) for v in fir_TAP63.filt_coeff]
    # # print(test_taps)
    # write_py_s400_output_to_csv(test_taps, filename="test_taps.csv")

    # random_taps = []
    # with open("random_taps.csv", 'r') as f:
    #     for line in f:
    #         sign = 1
    #         line = line.strip()
    #         # print(line[0][0])
    #         if line[0][0] == '-':
    #             sign = -1
    #             # print('neg')
    #             line = line[1:] # strip the negative so its detected as a numeric
    #         if line.isnumeric():
    #             integer_line = int(line)
    #             value = sign * integer_line
    #             # print(f"numeric:{line}, sign:{sign}")
    #             random_taps.append(value)
    #         else:
    #             random_taps.append(0)
    # print(f"Read: random_taps.csv as input data for random_taps")

    # fig, ax = plt.subplots(figsize=(8, 5))
    # ax.plot(np.arange(0, 63, 1), random_taps)
    # ax.grid(True)
    # ax.set_title("Random Filter Taps")
    # ax.set_xlabel("Tap Index")
    # ax.set_ylabel("Tap Value")
    # _save(fig, "random_taps_plot.png")

    # graph_sin_all(data.x_comb, scaled_data, scaled_data, "compare_float_vs_scaled.png")
