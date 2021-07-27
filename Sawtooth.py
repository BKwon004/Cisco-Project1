from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
t = np.linspace(0, 1, 500)
plt.plot(t, signal.sawtooth(2 * np.pi * 5 * t))
plt.show()