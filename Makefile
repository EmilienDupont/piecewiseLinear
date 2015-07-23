all:
	./SimpleServer.py

test:
	./piecewiseLinear.py

clean:
	-rm gurobi.log *.pyc *.lp
