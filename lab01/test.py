# EE125 Project 1 - Part 4, Sinusoids
# Sept. 16, 2024

import numpy as np
import matplotlib.pyplot as plt

# 1. Create a function that calculates the output s(t_n) = Asin(2*pi*f_0*t_n + phi), given A, f_0, phi, and
#    vector of time instants t_n as inputs


def s_calculate(A, f_0, phi, t_n):
    # f_0 in Hz, phi is phase in radians, t_n is vector of time instants in N
    # if t_n is not type(np.linspace):
    #     print("t_n is not np.linspace")
    #     exit
    t_n = np.asarray(t_n)
    test = A * np.sin(2 * np.pi * f_0 * t_n + phi)
    return test

# 2. Create 3 subplots 1st subplot having s_1(t) = sin( 2 pi t), plotting over 1 second
# Ensure spacing between samples is sufficient to produce a smooth, continuous plot.
# A = 1, f_0 = 1, phi = 0
N = 1000 # Number of samples
T = 1 # T is s
tn = np.linspace(0, T, N-1) # N Equispaced samples over T
s_1 = s_calculate(1, 1, 0, tn)

figure, (subplot1, subplot2, subplot3) = plt.subplots(1, 3, figsize=(15,10))
subplot1.plot(tn, s_1, linestyle='-', lw='1', color='red', label='s_1 sinusoid')

subplot1.set_xlabel('tn, N Vector of Time Instants over T=1s')
subplot1.set_ylabel('Output from s_1[tn]')
subplot1.set_title('Sinusoid Output of s_1[tn], over N=0,...,999')
subplot1.grid(True)

# Second subplot: s_2(t) = 2sin(6 pi t + pi / 2)
# A = 2, f_0 = 3, phi = pi/2
s_2 = s_calculate(2, 3, np.pi/2, tn)

subplot2.plot(tn, s_2, linestyle='-', lw='1', color='g', label='s_2 sinusoid')

subplot2.set_xlabel('tn, N Vector of Time Instants over T=1s')
subplot2.set_ylabel('Output from s_2[tn]')
subplot2.set_title('Sinusoid Output of s_2[tn], N=0,...,999')
subplot2.grid(True)

# Third subplot: s_3(t) = s_1(t) + s_2(t)
s_3 = s_1 + s_2

subplot3.plot(tn, s_3, linestyle='-', lw='1', color='b', label='s_3 sinusoid')

subplot3.set_xlabel('tn, N Vector of Time Instants over T=1s')
subplot3.set_ylabel('Output from s_3[tn]')
subplot3.set_title('Sinusoid Output of s_3[tn]= s_1[tn] + s_2[tn]')
subplot3.grid(True)

plt.tight_layout()
plt.show()

# 3. Calculate mean-square value of s_1(t), s_2(t), and s_1(t) + s_2(t)
s_1_meansquareval = np.mean(s_1 ** 2)
s_2_meansquareval = np.mean(s_2 ** 2)
s_3_meansquareval = np.mean(s_3 ** 2)

print(f"Mean Square Value, s_1: {s_1_meansquareval}, s_2: {s_2_meansquareval}, s_3: {s_3_meansquareval}")
# Mean Square Value, s_1: 0.4994994994994996, s_2: 2.002002002002002, s_3: 2.5015015015015014
print(f"Sum of s_1 and s_2 mean square value: {s_1_meansquareval + s_2_meansquareval}")
# Sum of s_1 and s_2 mean square value: 2.501501501501502

# What is the relationship between these three values?
# It seems as if the Mean Square Value of s_3 is the sum of s_1 and s_2, which follows s_3 = s_1 + s_2

# Is this relationship true for any arbitrary functions s_1(t) and s_2(t)
# No, as Mean Square Value is non-linear operation. For example, if s_1(t) and s_2(t)
# contain any scaling factors that depend on t, then this relationship will fail.