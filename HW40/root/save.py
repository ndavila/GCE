import Rappture
import sys
from math import *
import numpy as np
from scipy.integrate import odeint
from scipy import optimize

def f(x, a, formula):
    return eval(formula)

def calc(y, x, a, formula):
    return eval(formula)

def main():
    io = Rappture.library(sys.argv[1])

    xmin = float(io.get('input.number(min).current'))
    xmax = float(io.get('input.number(max).current'))
    y0 = float(io.get('input.number(Y0).current'))
    npts = int(io.get('input.number(Npts).current'))
    formula = io.get('input.string(formula).current')

    x = np.linspace(xmin, xmax, npts)
    sol = odeint(calc, y0, x, args=(1, formula))

    root = optimize.brentq(
               f, xmin, xmax, args=(1, formula)
           )

    my_str = 'Root of f(x) in the range' + str(xmin) +  ' to' + \
            str(xmax) + ' is ' + str(root)


    io.put('output.string(result1).about.label', 'Root')
    io.put('output.string(result1).current', my_str)

    Rappture.result(io)

if __name__ == "__main__":
    main()

