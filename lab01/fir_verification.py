import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from scipy import signal

import fir_TAP63

"""Create a sin function based on the following param values:
      - A = amplitude
      - f_Hz = frequency in Hz
      - phase = phase shift in rad
      - f_s = sampling frequency in Hz
      - t_total = total time spent sampling
"""
def create_sin(A, f_Hz, phase, f_s, t_total):
    n_samp = int(f_s * t_total)
    w = 2 * np.pi * f_Hz
    tn = np.linspace(0, w * t_total, int(f_s * t_total), endpoint=False)  # Discrete sampling times
    x = A * np.sin(tn + phase)
    return (x, tn)

t_total = 0.08 # in sec
s_rate = 2000 # Hz, sampling rate set by lab instructions
x_400, tn_400 = create_sin(1, 400, 0, s_rate, t_total)
x_500, tn_500 = create_sin(1, 500, 0, s_rate, t_total)

# Combined sinusoid input data
x_comb = x_400 + x_500

# "Ideal" convolution using lfilter from SciPy
b_fir = fir_TAP63.filt_coeff
y = signal.lfilter(b_fir, 1, x_comb)

freq_grpdelay_fir, grpdelay_fir = signal.group_delay([b_fir, 1], fs=s_rate)
print(grpdelay_fir)

## From EE125, recall...
## An FIR filter of length 63 or has 63 TAPs aka 62nd-order
## has a latency or group delay of order/2, so 62/2... however here,
## For some reason, need to use a shift of 30 to perfectly align signals.
## Could be due to off by 1 error?
## SHOULD ASK PROF ABOUT THIS.
print(len(b_fir))
shifted, tn_shift = create_sin(1, 400, 30, s_rate, t_total)


# plt.plot(tn_500, y)
# plt.show()