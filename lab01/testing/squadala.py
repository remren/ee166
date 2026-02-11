import matplotlib
# matplotlib.use('gtk3agg') 
from matplotlib import pyplot as plt

import numpy as np
from fxpmath import Fxp

import fir_TAP63

x = Fxp(-7.25)
x.info()

# k = Fxp(-1.24032, signed=True, n_word=10, n_frac=7, n_int=3)
k = Fxp(-1., signed=True, n_word=10, n_frac=7, n_int=3)

k.info()
k.bin(frac_dot=True)
print(k.bin())
# print(k.bin())
print(x.bin())

# Result of this value (5.07397461)_{10} should be (0101000100101111)_2
lec_test_num = Fxp(5.07397461, signed=True, n_word=16, n_frac=12, n_int=3)
print(f"Lecture Number Test: {lec_test_num.bin() == 0b0101000100101111}") # Taken from slides, so this should agree.

# TODO: UNDERSTAND HOW FIXED POINT NUMBER WORKS (convert back and forth easily in head)

## Test: single sinusoidal
# N = 10000   # number of samples (original signal)
## sampling rate = 2000 Hz, 2000 times a second, so in 1 second, should be fs * 1
s_rate = 2000   # Hz
T_total = 0.03  # seconds
f_1 = 400       # 400 Hz
T_1 = 2*np.pi*f_1*T_total, # timing for equispaced samples??
N = s_rate * T_total  # number of samples
tn_1 = np.linspace(0, T_1, int(N - 1)) # N equispaced samples over T (instead of N-1, also do endpoint=false)

ex_sin1 = 1 * np.sin(2 * np.pi * f_1 * tn_1 + 0) # sinusoid with amplitude 1, frequency = 400 Hz, phase = 0

## Test: two sinusoidals sum
f_2 = 500   # 500 Hz
T_2 = 2*np.pi*f_2*T_total, # timing for equispaced samples??
tn_2 = np.linspace(0, T_2, int(N-1)) # N equispaced samples over T (instead of N-1, also do endpoint=false)
ex_sin2 = 1 * np.sin(2 * np.pi * f_2 * tn_2)
ex_sin3 = ex_sin1 + ex_sin2
# print(ex_sin3)

## Test: Fxp sinusoids
# n = Fxp(list(range(N))) # sample indicies
s1 = Fxp(None, signed=True, n_word=10, n_frac=7, n_int=2)
s1.info()
s1(1 * np.sin(2 * np.pi * f_1 * tn_1))
# print(s1)
# print("[", end="")
# for i in s1:
#     print(i,end=", ")
# print("]")

val_1 = Fxp(1, signed=True, n_word=10, n_frac=7, n_int=2)
for i in ex_sin1:
    if i == 1.0:
        print("T_ex1")
for i in s1:
    if i == val_1:
        print("T")


## Test: Multiple Fxp sinusoid
s2 = Fxp(None, signed=True, n_word=10, n_frac=7, n_int=2)
s2(1 * np.sin(2 * np.pi * f_2 * tn_2))

s3 = Fxp(None, signed=True, n_word=10, n_frac=7, n_int=2)

s3 = s1 + s2

## conv - NOT USING FIXED POINT
fir_coeff = fir_TAP63.filt_coeff
# print(fir_coeff)

y = np.convolve(ex_sin3, fir_coeff)

print(y)
# print(f"length y={len(y)}")

# Graphing
figure, (subplot1, subplot2) = plt.subplots(1, 2, figsize=(15,10))
subplot1.plot(tn_1, ex_sin1, linestyle='-', lw='1', color='red', label='ex_sin1', marker=".")
subplot1.plot(tn_2, ex_sin2, linestyle='-', lw='1', color='green', label='ex_sin2', marker=".")
subplot1.set_xlabel(f'tn, N Vector of Time Instants over T={T}s')
subplot1.set_ylabel('Outputs from ex_sin1 and ex_sin2')
subplot1.set_title(f'Sinusoid Outputs of f_1={f_1} and f_2={f_2} Hz, Samples={N}')
subplot1.grid(True)

subplot2.plot(tn_1, ex_sin3, linestyle='-', lw='1', color='blue', label='ex_sin3', marker=".")
subplot2.set_xlabel(f'tn, N Vector of Time Instants over T={T}s')
subplot2.set_ylabel('Outputs from ex_sin3')
subplot2.set_title(f'Combined Sinusoid Output, Samples={N}')
subplot2.grid(True)
plt.figure(1)

figure, (subplot1, subplot2) = plt.subplots(1, 2, figsize=(15,10))
subplot1.plot(tn_1, s1, linestyle='-', lw='1', color='orange', label='s1', marker=".")
subplot1.plot(tn_2, s2, linestyle='-', lw='1', color='black', label='s2', marker=".")
subplot1.set_xlabel(f'tn, N Vector of Time Instants over T={T}s')
subplot1.set_ylabel('Fxp Outputs from s1 and s2')
subplot1.set_title(f'Sinusoid Fxp of f_1={f_1} and f_2={f_2} Hz, Samples={N}')
subplot1.grid(True)

subplot2.plot(tn_1, ex_sin3, linestyle='-', lw='1', color='purple', label='s3', marker=".")
subplot2.set_xlabel(f'tn, N Vector of Time Instants over T={T}s')
subplot2.set_ylabel('Fxp Outputs from s3')
subplot2.set_title(f'Combined Sinusoid Fxp Output, Samples={N}')
subplot2.grid(True)
plt.figure(2)

## FILTERING GRAPHS
figure, (subplot1, subplot2) = plt.subplots(2, 1, figsize=(20,8))
subplot1.plot(tn_1, ex_sin3, linestyle='-', lw='1', color='green', label='s3_not_filtered', marker=".")
subplot1.set_xlabel(f'tn, N Vector of Time Instants over T={T}s')
subplot1.set_ylabel('Outputs from s3, not filtered')
subplot1.set_title(f'Combined Sinusoid Output, Samples={N}')
subplot1.grid(True)

subplot2.plot(np.linspace(0, T, int(len(y)), endpoint="false"), y, linestyle='-', lw='1', color='blue', label='y', marker=".")
subplot2.set_xlabel(f'tn, N Vector of Time Instants over T={T}s')
subplot2.set_ylabel('Outputs from Y')
subplot2.set_title(f'Filtered Combined Sinusoid Output, Samples={N}')
subplot2.grid(True)
plt.figure(3)

# plt.tight_layout()

plt.show()

