import sys
import Rappture
import numpy as np
from scipy.integrate import odeint
from scipy import optimize
from math import *

def f(t, formula):
    return eval(formula)

def gas_mass(y, t, formula, omega):
    return -omega * y[0] + f(t, formula)

def mass(y, t, formula):
    return f(t, formula)

def gas_fraction(omega, t0, f0, MG_0, formula):
    M_G = odeint(gas_mass, MG_0, [0,t0], args=(formula, omega))
    M = odeint(mass, MG_0, [0,t0], args=(formula,))
    return M_G[1] / M[1] - f0


def main():

    # Load library--create object

    io = Rappture.library(sys.argv[1])

    # Get input

    tmin = float(io.get('input.number(min).current'))
    tmax = float(io.get('input.number(max).current'))
    t0 = float(io.get('input.number(t0).current'))
    f0 = float(io.get('input.number(f0).current'))
    MG_0 = float(io.get('input.number(MG_0).current'))
    npts = int(io.get('input.number(Npts).current'))
    formula = io.get('input.string(formula).current')

    t = np.linspace(tmin, tmax, npts)

    omega = optimize.brentq(
               gas_fraction, 0, 100., args = (t0, f0, MG_0, formula)
            )

    MG = odeint(gas_mass, MG_0, t, args=(formula, omega))
    
    M = odeint(mass, MG_0, t, args=(formula,))

    io.put('output.curve(result0).about.label','f(t) vs t',append=0)
    io.put('output.curve(result0).yaxis.label','f(t)')
    io.put('output.curve(result0).xaxis.label','t')

    io.put('output.curve(result1).about.label', 'Gas Mass vs t',append=0)
    io.put('output.curve(result1).yaxis.label', 'MG(t)')
    io.put('output.curve(result1).xaxis.label','t')

    io.put('output.curve(result2).about.label', 'Total Mass vs t',append=0)
    io.put('output.curve(result2).yaxis.label', 'M(t)')
    io.put('output.curve(result2).xaxis.label','t')

    for i in range(npts):
        io.put(
                'output.curve(result0).component.xy',
                '%g %g\n' % (t[i],f(t[i],formula)), append=1
              )
        io.put(
                'output.curve(result1).component.xy',
                '%g %g\n' % (t[i],MG[i][0]), append=1
              )
        io.put(
                'output.curve(result2).component.xy',
                '%g %g\n' % (t[i],M[i][0]), append=1
              )

    my_str_base = 'Star formation rate to get a gas fraction of '

    my_str = my_str_base + str(f0) + ' is ' + str(omega) + ' per Gyr.'

    io.put('output.string(result4).about.label', 'Star formation rate')
    io.put('output.string(result4).current', my_str)


    Rappture.result(io)


if __name__ == "__main__":
    main()
