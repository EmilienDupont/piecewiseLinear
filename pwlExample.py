#!/usr/bin/env python

from gurobipy import *
import math
import StringIO

def mycallback(model, where):
    if where == GRB.callback.MESSAGE:
        print >>model.__output, model.cbGet(GRB.callback.MSG_STRING),

def f(x, limithours, penalty):
    if x < limithours:
        return 0
    else:
        return (x-limithours)*penalty

def optimize(rate, profit, limit, hours, output=False):
    n = len(rate) # number of products
    limithours = hours[0]; maxhours = hours[1]; penalty = hours[2];

    m = Model()

    if not output:
        m.params.OutputFlag = 0

    m.setParam('TimeLimit', 10)

    # Add variables
    x = {}

    for i in range(n):
        x[i] = m.addVar(ub = limit[i], vtype=GRB.CONTINUOUS, name="x%d" % i)

    y = m.addVar(vtype=GRB.CONTINUOUS, name="y")

    m.update()

    # Add constraints
    m.addConstr(y == quicksum( x[j]/rate[j] for j in range(n)))

    # Set objective
    m.setObjective( quicksum(profit[i]*x[i] for i in range(n)), GRB.MAXIMIZE)

    # Set piecewise linear objective
    nPts = 101
    yi = []
    fi = []
    lb = 0
    ub = maxhours;

    for i in range(nPts):
        yi.append(lb + (ub - lb) * i / (nPts - 1))
        fi.append(-f(yi[i], limithours, penalty))

    m.setPWLObj(y, yi, fi)

    output = StringIO.StringIO()
    m.__output = output

    m.optimize(mycallback)

    if (m.status != 2):
        return ["error"]

    solution = []

    for i in range(n):
        solution.append(x[i].X)

    return [solution, output.getvalue()]

rate = [200, 140]; profit = [25,30]; limit = [6000,4000];
limithours = 40; maxhours = 50; penalty = 100; hours = [limithours, maxhours,penalty];

solution = optimize(rate, profit, limit, hours);

def handleoptimize(jsdict):
    if 'rate' in jsdict and 'profit' in jsdict and 'limit' in jsdict and 'hours' in jsdict:
        solution = optimize(jsdict['rate'], jsdict['profit'], jsdict['limit'],
                            jsdict['hours'])
        return {'solution': solution }

if __name__ == '__main__':
    import json
    jsdict = json.load(sys.stdin)
    jsdict = handleoptimize(jsdict)
    print 'Content-Type: application/json\n\n'
    print json.dumps(jsdict)
