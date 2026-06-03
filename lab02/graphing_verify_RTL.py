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
def read_csv_to_array(filename: str):
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
    """
    graph_sin_all:
        - to graph all the sinusoids used for and the actual input signal
    """
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
    """
    graph_float_fxp_conversion_error:
        - to graph the conversion error between fxp/float and float/fxp 
    """
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
        label="Original 400 Hz sin (Shifted 30 Samples)",
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
        label="Original 400 Hz sin (Shifted 30 Samples)",
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

def graph_filter_output_comp(x_arr,
                             fxp_y_python,
                             fxp_y_rtl,
                             fxp_diff,
                             filename):
    """
    graph_filter_output_comp:
        - Graph the FIR filter output
        - Compare the Python output against the RTL
    """
    figure, (sp1, sp2) = plt.subplots(2, 1, figsize=(20, 8))

    # Top subplot: Python vs. RTL FIR Filter Results
    sp1.plot(x_arr,
             fxp_y_python,
             color="blue",
             lw=4,
             markersize=15,
             marker=".", label="Python Filtered Output")
    sp1.plot(x_arr,
             fxp_y_rtl,
             lw=1, color="orange", marker=".",
             label="RTL Filtered Output (Shift by 1 sample due to setup)")
    sp1.grid(True)
    sp1.set_title("Python Filtered Output vs. RTL Filtered Output, Fixed-point Q1.8")
    sp1.set_ylabel("Amplitude")
    sp1.set_xlabel("Time (s)")
    sp1.legend(loc="upper right")

    # Bottom subplot: Difference (error?), python - RTL
    sp2.plot(x_arr,
             np.abs(fxp_diff),
             lw=1, color="red", marker=".",
             label=f"Difference (Python - RTL), Avg. Error: {np.average(np.abs(fxp_diff))}")
    sp2.grid(True)
    sp2.set_title("Absolute Difference of Filtered Python Output vs. RTL Output in Fixed-point Q1.8, aka Error")
    sp2.set_ylabel("Amplitude")
    sp2.set_xlabel("Time (s)")
    sp2.legend(loc="upper right")

    figure.suptitle(
        "FIR Filter Output Comparison Python vs. RTL", fontsize=14, fontweight="bold"
    )
    figure.tight_layout()

    _save(figure, filename)

def graph_filter_impulse_response(fxp_filt_coeff, filename):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(np.arange(0,len(fxp_filt_coeff),1),
            fxp_filt_coeff,
            lw=1, color="green", marker=".", label="Filter TAPs ")
    ax.grid(True)
    ax.set_title("FIR Filter Impulse Response, Fixed-point Q1.8")
    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Samples, n")
    fig.tight_layout()
    _save(fig, filename)

def graph_float_s400_vs_rtl_out(x_arr,
                                float_rtl_out,
                                float_s_400_shifted,
                                float_diff,
                                start_transient_samples,
                                filename):
    figure, (sp1, sp2) = plt.subplots(2, 1, figsize=(20, 8))

    # Top subplot: RTL filtered output (float) vs. time-shifted 400 Hz reference
    sp1.plot(x_arr,
             float_rtl_out, 
             lw=1, color="green", marker=".", label="Filtered Output from RTL (Q1.8 to Float)")
    sp1.plot(x_arr,
             float_s_400_shifted,
             lw=1,
             color="red",
             marker=".",
             label="400 Hz (Shifted 30 Samples)")
    sp1.grid(True)
    sp1.set_title("Filtered Output vs. Time-Shifted 400 Hz Sinusoid")
    sp1.set_ylabel("Amplitude")
    sp1.set_xlabel("Time (s)")
    sp1.legend(loc="upper right")
    
    # Calculate average difference excluding transient samples
    avg_diff = np.mean(np.abs(float_diff[start_transient_samples:]))
    
    # Bottom subplot: Difference (s_400 - RTL Filtered Output)
    sp2.plot(x_arr,
             np.abs(float_diff),
             lw=1,
             color="blue",
             marker=".",
             label=f"Absolute Difference (400Hz sin - RTL Filtered Output in Float)")
    
    # Add the line for average difference in steady state
    sp2.axhline(y=avg_diff, color='red', linestyle='-', lw=1,
                label=f'Average Steady State Error: {avg_diff:.6f}')

    sp2.grid(True)
    sp2.set_title("Absolute Difference in Float, (400Hz sin - Filtered RTL Output)")
    sp2.set_ylabel("Amplitude")
    sp2.set_xlabel("Time (s)")
    sp2.legend(loc="upper right")

    figure.suptitle(
        "Original 400Hz Sin Signal vs. RTL Filtered Output", fontsize=14, fontweight="bold"
    )
    figure.tight_layout()

    _save(figure, filename)

def graph_discrete(arr, title, filename):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(np.arange(0,len(arr),1),
            arr,
            lw=1, color="green", marker=".", label="Signal")
    ax.grid(True)
    ax.set_title(title)
    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Samples, n")
    fig.tight_layout()
    _save(fig, filename)

## *** v Main Below v ***

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

    fxp_taps = float_to_fxp(tfilter_float_taps)

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
    print("\n" + "=" * 60)
    print("6. Produce a longer input signal for RTL")
    print("=" * 60)

    t_total = 0.1 # in sec, longer than 0.08 from signal_data.t_total
    s_rate = signal_data.s_rate
    x_400, tn_400 = signal_data.create_sin(1, 400, 0, s_rate, t_total)
    x_500, tn_500 = signal_data.create_sin(1, 500, 0, s_rate, t_total)

    s_comb_longer = x_400 + x_500 # Combined sinusoid input data, but longer for later graphing

    fxp_s_comb_longer = float_to_fxp(s_comb_longer)
    write_array_to_csv(fxp_s_comb_longer, "RTL_s400_500_input_signal_longer.csv")

    # 7. Graph the FIR filter results, comparing Python vs. RTL
    print("\n" + "=" * 60)
    print("7. Graph FIR filter results, compare Python vs. RTL")
    print("=" * 60)
    
    # Read in RTL output from CSV
    fxp_rtl_out = read_csv_to_array("RTL_output.csv")
    shift = 1 # 1 for fixed RTL, 2 for unfixed RTL
    fxp_rtl_out_trim = fxp_rtl_out[shift:shift+len(GRAPHING_TN)]
    # print(f"len:{len(fxp_rtl_out)}, len_trim:{len(fxp_rtl_out_trim)}")

    fxp_s_y = float_to_fxp(s_y) # Python output in Q1.8
    
    fxp_diff_s_y_rtl_out_trim =  np.abs(fxp_s_y) - np.abs(fxp_rtl_out_trim)

    graph_filter_output_comp(GRAPHING_TN,
                             fxp_s_y,
                             fxp_rtl_out_trim,
                             fxp_diff_s_y_rtl_out_trim,
                             "result_compare_filter_out.png")
    
    # 8. Graph the FIR Filter Impulse Response (fxp)
    print("\n" + "=" * 60)
    print("8. Graph FIR filter impulse response")
    print("=" * 60)

    graph_filter_impulse_response(fxp_taps, "fir_TAP63_impulse_response.png")

    # 9. Graph the error comparing the original s_400 float against the RTL output in float
    print("\n" + "=" * 60)
    print("9. Graph error comparing original s_400 vs. RTL filter output (to float)")
    print("=" * 60)

    float_rtl_out_trim = fxp_to_float(fxp_rtl_out_trim)
    float_diff = np.abs(s_shifted_400) - np.abs(float_rtl_out_trim)
    start_steady_state = 63

    graph_float_s400_vs_rtl_out(GRAPHING_TN,
                                float_rtl_out_trim,
                                s_shifted_400,
                                float_diff,
                                start_steady_state,
                                "result_compare_original_vs_rtl_out.png")
    
    # 10. Find repeating part of the input signal and graph it
    print("\n" + "=" * 60)
    print("10. Find repeating part of the input signal and graph it")
    print("=" * 60)

    test_signal_array = np.zeros(0)

    repeating_segment = fxp_s_comb[0:20]
    test_signal_array = np.append(test_signal_array, repeating_segment)
    test_signal_array = np.append(test_signal_array, repeating_segment)

    graph_discrete(test_signal_array,
                   "Graphing Repeating Signal Test",
                   "test_repeating_signal.png")

    # 11. Graph output from new testbench en_seq for Lab02
    print("\n" + "=" * 60)
    print("10. Graph output from new testbench en_seq for Lab02")
    print("=" * 60)

    tb_output = read_csv_to_array("RTL_output.csv")

    graph_discrete(tb_output,
                   "New Testbench Output for lab02",
                   "lab02_tb_output.png")