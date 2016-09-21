#!/usr/bin/python
''' short test from the Theano website to see if Theano is working with CUDA
.theanrc contains

[global]
floatX = float32
device = gpu0

NOT WORKING under LiClipse

@author: richard lyman

'''
from theano import function, config, shared, sandbox
import theano.tensor as T
import theano
import numpy
import time
vlen = 10 * 30 * 768  # 10 x #cores x # threads per core
iters = 1000

rng = numpy.random.RandomState(22)
x = shared(numpy.asarray(rng.rand(vlen), config.floatX))
f = function([], T.exp(x))
print(f.maker.fgraph.toposort())
t0 = time.time()
for i in range(iters):
    r = f()
t1 = time.time()
print("Looping %d times took %f seconds" % (iters, t1 - t0))
print("Result is %s" % (r,))
if numpy.any([isinstance(x.op, T.Elemwise) for x in f.maker.fgraph.toposort()]):
    print('Used the cpu')
else:
    print('Used the gpu')