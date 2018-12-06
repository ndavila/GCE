import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def model (y,t):
    k = 1
    dydt = (-0.03 * y) + (k + t)**(-1)
    return dydt

y0 = 5

t = np.linspace(0,20)

y = odeint(model,y0,t)

plt.plot(t,y)
plt.xlabel('time')
plt.ylabel('$M_{g}(t)$')
plt.show()
