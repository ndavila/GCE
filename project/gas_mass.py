import sys
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def model (m,t):
    k = 1
    dmdt = (-0.3 * m) + k*(1 + t)**(-1)
    return dmdt

m0 = 0.1

t = np.linspace(0,50, 500)

m = odeint(model,m0,t)

plt.plot(t,m)
plt.xlabel('time')
plt.ylabel('$M_{g}(t)$')
plt.show()
