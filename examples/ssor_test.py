import math, time
import numpy as np
from pysparse.sparse import spmatrix
from pysparse.itsolvers.krylov import pcg
from pysparse.precon import precon
from poisson2dvec import poisson2d_vec_sym_blk

N = 200
TOL = 1e-8
MAXIT = 800
SSOR_STEPS = 2

L = poisson2d_vec_sym_blk(N)
S = L.to_sss()

b = np.ones(N*N, 'd')

print 'Solving 2D-Laplace equation using PCG and SSOR preconditioner with variable omega'
print
print 'omega    nit    time       resid' 
print '--------------------------------' 

for omega in [0.1*(i+1) for i in range(20)]:

    K_ssor = precon.ssor(S, omega, SSOR_STEPS)
    t1 = time.clock()

    x = np.empty(N*N, 'd')
    info, iter, relres = pcg(S, b, x, TOL, MAXIT, K_ssor)

    elapsed_time = time.clock() - t1

    r = np.zeros(N*N, 'd')
    S.matvec(x, r)
    r = b - r
    res_nrm2 = np.linalg.norm(r)

    if info == 0:
        iter_str = str(iter)
    else:
        iter_str = '---'
    print '%5.1f  %5s  %6.2f  %10.3e' % (omega, iter_str, elapsed_time, res_nrm2)
