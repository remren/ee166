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
    tn = np.arange(n_samp) / f_s  # Discrete sampling times
    x = A * np.sin(w * tn + phase)
    return (x, tn)

x, tn = create_sin(1, 400, 0, 2000, 0.08)

## Ideal sinusoid:
f_1 = 400 # Hz
t_test = 0.08
t = np.linspace(0, 0.08 * f_1 * 2 * np.pi, int(16000 * 0.08), endpoint=False)
x1 = 1*np.sin(t) # ideal

s_rate = 2000
t2 = np.linspace(0, t_test *f_1 * 2 * np.pi, int(s_rate * t_test), endpoint=False)
x2 = 1*np.sin(t2)

# Print max value to verify
print(f"Maximum amplitude: {np.max(np.abs(x)):.6f}")

# plt.plot(tn, x, lw="1", color="green", marker='.')
plt.plot(t, x1, lw="1", color="green", marker='.')
plt.plot(t2, x2, lw="1", color="blue", marker='.')

plt.grid(True)
plt.show()