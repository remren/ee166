import matplotlib
from matplotlib import pyplot as plt
import numpy as np

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

y = x_400 + x_500

plt.plot(tn_400, x_400, lw="1", color="green", marker='.')
plt.plot(tn_500, x_500, lw="1", color="blue", marker='.')
plt.plot(tn_500, y, lw="1", color="red", marker='.')

plt.grid(True)
plt.show()