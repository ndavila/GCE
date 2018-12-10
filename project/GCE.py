import sys
import Rappture
import numpy as np
from scipy.integrate import odeint
from scipy import optimize

def f(y, x, formula):
    return eval(formula)

def calc(x, a, formula):
    y = odeint(f, -a, [0,x], args=(formula,))
    return y[1] 

def main():

    io = Rappture.library(sys.argv[1])

    xmin = float(io.get('input.number(min).current'))
    xmax = float(io.get('input.number(max).current'))
    a = float(io.get('input.number(a).current'))
    y0 = float(io.get('input.number(Y0).current'))
    npts = int(io.get('input.number(Npts).current'))
    formula = io.get('input.string(formula).current')

    x = np.linspace(xmin, xmax, npts)
    sol = odeint(calc, y0, x, args=(formula,))

    io.put('output.curve(result0).about.label','f(X) vs X',append=0)
    io.put('output.curve(result0).yaxis.label','f(X)')
    io.put('output.curve(result0).xaxis.label','X')

    io.put('output.curve(result1).about.label','Integral of f(X) vs X',append=0)
    io.put('output.curve(result1).yaxis.label','Integral of f(X)')
    io.put('output.curve(result1).xaxis.label','X')

    for i in range(npts):
        io.put(
                'output.curve(result0).component.xy',
                '%g %g\n' % (x[i],f(x[i],formula)), append=1
              )
        io.put(
                'output.curve(result1).component.xy',
                '%g %g\n' % (x[i],sol[i][0]), append=1
              )      

    my_str_base = 'int_0^root (' + formula + ') dx - ' + str(a)

    root = optimize.brentq(calc, xmin, xmax, args=(a, formula))

    my_str = '\nRoot of ' + my_str_base + ' in [' + str(xmin) + \
            ', ' + str(xmax) + '] is ' + str(root)

    io.put('output.string(result1).about.label', 'Root')
    io.put('output.string(result1).current', my_str)

    check = calc(root, a, formula)

    my_str2 = '\nCheck: ' + my_str_base + ' = ' + str(check[0])

    io.put('output.string(result2).about.label', 'Diagnostic')
    io.put('output.string(result2).current', my_str2)

    Rappture.result(io)


if __name__ == "__main__":
    main()
