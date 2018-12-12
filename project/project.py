import sys
import Rappture
import numpy as np
from scipy.integrate import odeint
from scipy import optimize
from math import *

def f(t, formula):
    return eval(formula)

def total_mass(y, t, formula):
    return f(t, formula)

def gas_mass(y, t, formula, omega):
    return -omega * y[0] + f(t, formula)

def calc(y0, t, formula, gas_mass, omega):
    x = odeint(gas_mass[0], y0, t, args = (formula,omega))
    return x[1] - gas_mass[0]

def main():

    # Load library--create object

    io = Rappture.library(sys.argv[1])

    # Get input

    tmin = float(io.get('input.number(min).current'))
    tmax = float(io.get('input.number(max).current'))
#    a = float(io.get('input.number(a).current'))
    y0 = float(io.get('input.number(Y0).current'))
    npts = int(io.get('input.number(Npts).current'))
    formula = io.get('input.string(formula).current')

    t = np.linspace(tmin, tmax, npts)

    omega = 0.3

    y = odeint(gas_mass, y0, t, args=(formula,omega))
    
#    z = odeint(total_mass, y0, t, args=(formula,))

    io.put('output.curve(result0).about.label','f(t) vs t',append=0)
    io.put('output.curve(result0).yaxis.label','f(t)')
    io.put('output.curve(result0).xaxis.label','t')

    io.put('output.curve(result2).about.label',
            'Integral of dMG/dt vs t',append=0)
    io.put('output.curve(result2).yaxis.label',
            'Integral of dMG/dt')
    io.put('output.curve(result2).xaxis.label','t')

    for i in range(npts):
        io.put(
                'output.curve(result0).component.xy',
                '%g %g\n' % (t[i],f(t[i],formula)), append=1
              )
        io.put(
                'output.curve(result2).component.xy',
                '%g %g\n' % (t[i],y[i][0]), append=1
              )

#    root = optimize.brentq(calc, y0, tmin, tmax,
#            args =  (omega, formula, gas_mass))

    my_str_base = 'int_0^root (' + formula + ')dx '

    my_str = '\nRoot of ' + my_str_base + '' 

    io.put('output.string(result1).about.label', 'Root')
    io.put('output.string(result1).current', my_str)


    Rappture.result(io)


if __name__ == "__main__":
    main()
