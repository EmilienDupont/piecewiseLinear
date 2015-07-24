#!/usr/bin/env python

def f1(x, a1, a2):
    return a1*math.exp(a2*x)

def f2(x, b1, b2):
    return b1*math.log(b2*(x+1))

def f3(x, c1, c2):
    return c1*(x/2 - c2)*(x/2 - c2)*(x/2 - c2)

def f4(x, d1, d2):
    return d1*math.sin(d2*x)

from gurobipy import *
import math

def optimize(params):

    a1 = params[0]; a2 = params[1];
    b1 = params[2]; b2 = params[3];
    c1 = params[4]; c2 = params[5];
    d1 = params[6]; d2 = params[7];
    n = params[8]; # Number of points - 1

    m = Model()

    lb = 0.0

    ub = 5.0

    x = m.addVar(lb ,ub , name='x')

    m.update()

    xi = [] # Sample points

    fi = [] # Function value at sample points

    for i in range(n + 1):
        xi.append(lb + (ub - lb) * i / n)
        fi.append(f1(xi[i], a1, a2) +
                  f2(xi[i], b1, b2) +
                  f3(xi[i], c1, c2) +
                  f4(xi[i], d1, d2))

    print xi
    print fi

    m.setPWLObj(x, xi, fi)

    m.optimize()

    return x.X

params = [1,1,1,1,1,1,1,1,10];

x0 = optimize(params)

print x0
