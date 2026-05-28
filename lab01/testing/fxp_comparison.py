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

# Plotting Helpers
def _save(fig, filename):
    """Save figure to images/ and close."""
    os.makedirs(SAVE_DIR, exist_ok=True)
    path = os.path.join(SAVE_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")

# Conversion Helpers

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

# Graphing Helpers

def graph_impulse_compare(float_orig, float_convert, fxp_orig, fxp_convert, 
                          filename="impulse_compare.png"):
    """Compare impulse responses of FIR filter."""

    taps = np.arange(0, TAPS, 1)

    figure, (sp1, sp2) = plt.subplots(2, 1, figsize=(20, 8))

    import TFilter_TAP63_fxp_Q1_6, TFilter_TAP63_fxp_Q1_8
    # Top subplot: filtered output vs. time-shifted 400 Hz reference
    sp1.plot(
        taps,
        fxp_to_float(TFilter_TAP63_fxp_Q1_8.filt_coeff),
        lw=5,
        markersize=20,
        color="gray",
        marker=".",
        label="Fxp to float (TFilter Q1.8)",
    )
    sp1.plot(taps, 
             float_orig, lw=1, color="green", marker=".", label="Float Original (TFilter Double)")
    sp1.plot(
        taps,
        float_convert,
        lw=1,
        color="red",
        marker=".",
        label="Fxp to Float (TFilter Q1.7)",
    )
    sp1.plot(
        taps,
        fxp_to_float(TFilter_TAP63_fxp_Q1_6.filt_coeff),
        lw=1,
        color="orange",
        marker=".",
        label="Fxp to float (TFilter Q1.6)",
    )
    sp1.grid(True)
    sp1.set_title("Floating-point Impulse Resp. - FIR Filt.")
    sp1.set_ylabel("Magnitude")
    sp1.set_xlabel("n")
    sp1.legend(loc="upper right")

    # Bottom subplot: filtered output vs. original 400 Hz component
    sp2.plot(
        taps,
        TFilter_TAP63_fxp_Q1_8.filt_coeff,
        lw=5,
        markersize=20,
        color="gray",
        marker=".",
        label="TFilter Q1.8",
    )
    sp2.plot(
        taps,
        fxp_convert,
        lw=1,
        color="blue",
        marker=".",
        label="Float to Fxp (Q2.8)",
    )
    sp2.plot(taps, 
             fxp_orig, lw=1, color="green", marker=".", label="TFilter Q1.7 (Misunderstood as 8 frac bits)")
    sp2.plot(
        taps,
        TFilter_TAP63_fxp_Q1_6.filt_coeff,
        lw=1,
        color="red",
        marker=".",
        label="TFilter Q1.6",
    )
    sp2.grid(True)
    sp2.set_title("Fxp Impulse Resp. - FIR Filt.")
    sp2.set_ylabel("Magnitude")
    sp2.set_xlabel("n")
    sp2.legend(loc="upper right")

    figure.suptitle(
        "FIR Filter Impulse Response Comparisons", fontsize=14, fontweight="bold"
    )
    figure.tight_layout()

    _save(figure, filename)

if __name__ == "__main__":
    import TFilter_TAP63_double, TFilter_TAP63_fxp_Q1_7
    float_TFilter_TAP63_double = TFilter_TAP63_double.filt_coeff
    fxp_TFilter_TAP63_fxp8bits = TFilter_TAP63_fxp_Q1_7.filt_coeff

    fxp_TFilter_TAP63_double = float_to_fxp(float_TFilter_TAP63_double)
    float_TFilter_TAP63_fxp8bits = fxp_to_float(fxp_TFilter_TAP63_fxp8bits)

    # print(f"fxp_TFilter_TAP63_fxp8bits: {fxp_TFilter_TAP63_fxp8bits}")
    # print(f"fxp_TFilter_TAP63_double: {fxp_TFilter_TAP63_double}")

    # print(f"float_TFilter_TAP63_double: {float_TFilter_TAP63_double}")
    # print(f"float_TFilter_TAP63_fxp8bits: {float_TFilter_TAP63_fxp8bits}")

    # print(f"float to float check: {float_TFilter_TAP63_double == float_TFilter_TAP63_fxp8bits}")
    # print(f"fxp to fxp check: {fxp_TFilter_TAP63_fxp8bits == fxp_TFilter_TAP63_double}")

    graph_impulse_compare(float_TFilter_TAP63_double, float_TFilter_TAP63_fxp8bits,
                          fxp_TFilter_TAP63_fxp8bits, fxp_TFilter_TAP63_double,
                          "fir_filt_impulse_compare.png")
    
    print(f"Average fxp diff: {np.average(fxp_TFilter_TAP63_fxp8bits - fxp_TFilter_TAP63_double)}")
    print(f"Average float diff: {np.average(float_TFilter_TAP63_double - float_TFilter_TAP63_fxp8bits)}")

    print(f"Float to Fxp: {fxp_TFilter_TAP63_double}")
