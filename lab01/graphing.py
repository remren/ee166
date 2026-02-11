import matplotlib
from matplotlib import pyplot as plt
import numpy as np

import fir_verification as data

graphing_tn = np.linspace(0, data.t_total, int(data.s_rate * data.t_total))

# Graphing combining sinusoids for test data.
## TODO: [] add labels
s_400 = data.x_400
s_500 = data.x_500
s_comb = data.x_comb
s_y = data.y
figure, (sp1, sp2, sp3) = plt.subplots(3, 1, figsize=(20,8))
sp1.plot(graphing_tn, s_400, lw='1', color='green', marker='.')
sp1.grid(True)
sp2.plot(graphing_tn, s_500, lw='1', color='blue', marker='.')
sp2.grid(True)
sp3.plot(graphing_tn, s_comb, lw='1', color='red', marker='.')
sp3.grid(True)
plt.figure(1)

# Comparing the 400 Hz result to the filtered result (Convolved result, and both results overlayed)
figure, (sp1, sp2) = plt.subplots(2, 1, figsize=(20,8))
sp1.plot(graphing_tn, s_y, lw='1', color='green', marker='.')
sp1.plot(graphing_tn, data.shifted, lw='1', color='red', marker='.')
sp1.grid(True)

sp2.plot(graphing_tn, s_y, lw='1', color='green', marker='.')
sp2.plot(graphing_tn, s_400, lw='1', color='blue', marker='.')
sp2.grid(True)
plt.figure(2)


plt.grid(True)
plt.show()