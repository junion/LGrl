
import numpy as np
from math import exp
import SparseBayes as sb
from GlobalConfig import *

InitConfig()
config = GetConfig()
config.read(['LGrl.conf'])

noiseFactor = 1e12

dimension = 1
noiseToSignal = 0.2
N = 20.0
basisWidth = 0.05
pSparse = 0.90
iterations = 500
basisWidth = basisWidth**(1/dimension)
    

def dist_squared(X,Y):
    nx = X.shape[0]
    ny = Y.shape[0]
    
    return np.dot(np.atleast_2d(np.sum((X**2),1)).T,np.ones((1,ny))) + \
        np.dot(np.ones((nx,1)),np.atleast_2d(np.sum((Y**2),1))) - 2*np.dot(X,Y.T);

def basis_func(X):
    C = X.copy()
    BASIS = np.exp(-dist_squared(X,C)/(basisWidth**2))
    return BASIS

def inc_basis_func(X,BASIS=None):
    C = X.copy()
    BASIS = np.exp(-dist_squared(X,C)/(basisWidth**2))
    return BASIS
    
def sb_eval(iter=1):
    m = sb.SparseBayes()
    
    total_ED = 0
    
    for i in range(iter):
        X = np.atleast_2d(np.arange(N)/N).T
#        print X
        X = np.array([[0.],[0.0500],[0.1000],[0.1500],[0.2000],[0.2500],[0.3000],[0.3500],[0.4000],[0.4500],[0.5000],\
                      [0.5500],[0.6000],[0.6500],[0.7000],[0.7500],[0.8000],[0.8500],[0.9000],[0.9500]])
         
        BASIS = basis_func(X)
        
        #np.random.seed(1)
        M = BASIS.shape[1]
        w = (np.random.randn(M,1) * 100)/(M * (1 - pSparse))
        sparse = (np.random.rand(M,1) < pSparse).nonzero()
        w[sparse] = 0
        
        z = np.dot(BASIS,w)
        
        noise = np.std(z) * noiseToSignal
        Outputs = z + noise * np.random.randn(N,1)
#        print Outputs
        
        Outputs = np.array([[44.2582],[-2.5095],[-48.4976],[-18.7149],[-0.1074],[1.5062],[0.3183],[0.9407],[1.8032],[-5.1377],\
                            [2.0350],[2.1565],[0.0426],[-4.6794],[-15.3740],[-28.1786],[-8.6593],[3.9288],[-3.1340],[-3.7421]])
           
 
        try:      
            Relevant,Mu,Alpha,beta,update_count,add_count,delete_count,full_count = \
            m.learn(X.copy(),Outputs.copy(),basis_func)
        except RuntimeError:
            print 'RuntimeError'
            continue
        
        w_infer = np.zeros((BASIS.shape[1],1))
        w_infer[Relevant] = Mu 
        
        y = np.dot(BASIS.T,w_infer)
        e = y - Outputs
        ED = np.dot(e.T,e)
        total_ED += ED
        
        #print BASIS[:,0]
#        print w_infer
        #print Outputs
#        print y
#        print ED
#        print update_count
#        print add_count
#        print delete_count
#        print full_count
    print total_ED/iter

def inc_sb_eval(iter=1):
    m = sb.SparseBayes()
    
    total_ED = 0
    succ = 0
    
    for i in range(iter):
        X = np.atleast_2d(np.arange(N)/N).T
#        print X
#        X = np.array([[0.],[0.0500],[0.1000],[0.1500],[0.2000],[0.2500],[0.3000],[0.3500],[0.4000],[0.4500],[0.5000],\
#                      [0.5500],[0.6000],[0.6500],[0.7000],[0.7500],[0.8000],[0.8500],[0.9000],[0.9500]])
         
        BASIS = basis_func(X)
        
        #np.random.seed(1)
        M = BASIS.shape[1]
        w = (np.random.randn(M,1) * 100)/(M * (1 - pSparse))
        sparse = (np.random.rand(M,1) < pSparse).nonzero()
        w[sparse] = 0
        
        z = np.dot(BASIS,w)
        
        noise = np.std(z) * noiseToSignal
        Outputs = z + noise * np.random.randn(N,1)
#        print Outputs
        
#        Outputs = np.array([[44.2582],[-2.5095],[-48.4976],[-18.7149],[-0.1074],[1.5062],[0.3183],[0.9407],[1.8032],[-5.1377],\
#                            [2.0350],[2.1565],[0.0426],[-4.6794],[-15.3740],[-28.1786],[-8.6593],[3.9288],[-3.1340],[-3.7421]])
           

        try: 
            for i in range(X.shape[0]):
                print i
                if i == 0:     
                    Relevant,Mu,Alpha,beta,update_count,add_count,delete_count,full_count = \
                    m.learn(np.atleast_2d(X[i,:]).copy(),np.atleast_2d(Outputs[i,:]).copy(),basis_func)
                else:
                    Relevant,Mu,Alpha,beta,update_count,add_count,delete_count,full_count = \
                    m.incremental_learn(np.atleast_2d(X[i,:]).copy(),np.atleast_2d(Outputs[i,:]).copy(),inc_basis_func)
        except RuntimeError:
            print 'RuntimeError'
            print i
            print X
            print Outputs
                
        
        w_infer = np.zeros((BASIS.shape[1],1))
        w_infer[Relevant] = Mu 
        
        y = np.dot(BASIS.T,w_infer)
        e = y - Outputs
        ED = np.dot(e.T,e)
        total_ED += ED
        succ += 1
        
        #print BASIS[:,0]
#        print w_infer
        #print Outputs
#        print y
#        print ED
#        print update_count
#        print add_count
#        print delete_count
#        print full_count
    print succ
    print total_ED/succ

def rl_basis_func(X,BASIS=None):
#        print X
    BASIS = np.zeros((len(X),len(X)))
#        print BASIS
    for i, x1 in enumerate(X):
#            print 'x1: %s'%str(x1)
        for j, x2 in enumerate(X):
#                print 'x2: %s'%str(x2)
#                if x1[1] == x2[1] and x1[2] == x2[2]:
#            if x1[2] == x2[2]:
#                BASIS[j,i] = (np.dot(x1[0],x2[0]) + 0.1)**2
#            ua_kernel = 0.5 if xi[1] != X[-1][1] else 1.0
            ua_kernel = 1.0
            if x1[2] == x2[2]:
                BASIS[j,i] += np.exp(-(np.sum(x1[0]**2) + np.sum(x2[0]**2) - 2*np.dot(x1[0],x2[0]))/(0.25**2)) * ua_kernel
#        print BASIS
    return BASIS

def sb_rl_test(iter=1):
    from copy import deepcopy 
    m = sb.SparseBayes()
    
    total_ED = 0
    
    for i in range(iter):
#        X =[[np.array([ 1.,  0.0000001,  0.00000002,  0.,  0.0000005]), 'None', '[ask] request departure_place'],\
#            [np.array([ 1.,  0.00000002,  0.0000001,  0.0000005,  0.]), '[non-understanding]', '[ask] request all'],\
#            [np.array([ 1.,  0.00000002,  0.0000005,  0.,  0.0000001]), '[non-understanding]', '[ask] request all']]
#        Outputs = np.array([[-1.0000001],[-1.00000002],[-1.0000005]])
        X =[[np.array([ 1.,  0.,  0.,  0.,  0.]), 'None', '[ask] request departure_place'],\
            [np.array([ 1.,  0.,  0.,  0.,  0.]), '[non-understanding]', '[ask] request all'],\
            [np.array([ 1.,  0.,  0.,  0.,  0.]), '[non-understanding]', '[ask] request all']]
        Outputs = np.array([[-1.],[-1.],[-1.]])
         
        BASIS = rl_basis_func(X)
        print 'BASIS: %s'%str(BASIS)
        
        try:      
            Relevant,Mu,Alpha,beta,update_count,add_count,delete_count,full_count = \
            m.incremental_learn(X,Outputs,rl_basis_func)
#            m.incremental_learn(deepcopy(X),Outputs.copy(),rl_basis_func)
        except RuntimeError:
            print 'RuntimeError'
            continue
        
        w_infer = np.zeros((BASIS.shape[1],1))
        w_infer[Relevant] = Mu 
        
        y = np.dot(BASIS.T,w_infer)
        e = y - Outputs
        ED = np.dot(e.T,e)
        total_ED += ED
        
        #print BASIS[:,0]
#        print w_infer
        print Outputs
        print y
        print ED
#        print update_count
#        print add_count
#        print delete_count
#        print full_count
    print total_ED/iter

def rl_inc_basis_func(X,BASIS=None):
#    noise = np.atleast_2d(np.random.standard_normal(len(X))/noiseFactor).T
    if (len(X) == 1):
        noise = np.array([[-9.46011e-13]])
    else:
        noise = np.array([[1.63086e-13],[-8.74124e-13]])
    for i in range(len(X)):
        print '%d) %g'%(i,noise[i])

    basis = np.zeros((len(X),1)) #+ noise
    for i, xi in enumerate(X):
#            ua_kernel = 0.5 if xi[1] != X[-1][1] else 1.0
        ua_kernel = 1.0
        if xi[2] == X[-1][2]:
            basis[i,0] += np.exp(-(np.sum(xi[0]**2) + np.sum(X[-1][0]**2) - 2*np.dot(xi[0],X[-1][0]))/(0.25**2)) * ua_kernel
    
#        self.appLogger.info('basis %s'%str(basis))

    if BASIS != None:
#            print basis[:-1,0].T
        BASIS = np.vstack((BASIS,np.atleast_2d(basis[:-1,0].T)))
#            print 'BASIS %s'%str(BASIS)
        BASIS = np.hstack((BASIS,basis))
#            print 'BASIS %s'%str(BASIS)
    else:
        BASIS = basis
#        print 'BASIS %s'%str(BASIS)
    return BASIS

def inc_sb_rl_test(iter=1):
    from copy import deepcopy 
    m = sb.SparseBayes()
    
    total_ED = 0
    
    for i in range(iter):
        print i
#        X =[[np.array([ 1.,  0.,  0.,  0.,  0.]), 'None', '[ask] request departure_place'],\
#            [np.array([ 1.,  0.,  0.,  0.,  0.]), '[non-understanding]', '[ask] request all'],\
#            [np.array([ 1.,  0.,  0.,  0.,  0.]), '[non-understanding]', '[ask] request all']]
#        Outputs = np.array([[-1.],[-1.],[-1.]])
#        X =[[np.array([ 1.,  0.0000001,  0.00000002,  0.,  0.0000005]), 'None', '[ask] request departure_place'],\
#            [np.array([ 1.,  0.00000002,  0.0000001,  0.0000005,  0.]), '[non-understanding]', '[ask] request all'],\
#            [np.array([ 1.,  0.00000002,  0.0000005,  0.,  0.0000001]), '[non-understanding]', '[ask] request all']]
#        Outputs = np.array([[-1.0000001],[-1.00000002],[-1.0000005]])

        X =[[np.array([ 1.,  0.,  0.,  0.,  0.]), 'None', '[ask] request all'],\
            [np.array([ 1.,  0.,  0.,  0.,  0.]), '[ig] confirm', '[ask] request all']]
        Outputs = np.array([[-1.],[-1.]]) #+ np.atleast_2d(np.random.standard_normal(len(X))/noiseFactor).T
         
        raw_BASIS = rl_basis_func(X)
        print 'raw_BASIS: %s'%str(raw_BASIS)
#        BASIS = rl_basis_func(X)
#        print 'BASIS: %s'%str(BASIS)
        
        for xi in X:
            Relevant,Mu,Alpha,beta,update_count,add_count,delete_count,full_count = \
            m.incremental_learn([xi],np.atleast_2d(Outputs[i,:]),rl_inc_basis_func)
        
#        print 'BASIS: %s'%str(BASIS)
        print 'raw_BASIS: %s'%str(raw_BASIS)
        w_infer = np.zeros((raw_BASIS.shape[1],1))
#        w_infer = np.zeros((BASIS.shape[1],1))
        w_infer[Relevant] = Mu 
        
#        y = np.dot(BASIS.T,w_infer)
        y = np.dot(raw_BASIS.T,w_infer)
        e = y - Outputs
        ED = np.dot(e.T,e)
        total_ED += ED
        
        #print BASIS[:,0]
#        print w_infer
        print Outputs
        print y
        print ED
#        print update_count
#        print add_count
#        print delete_count
#        print full_count
    print total_ED/iter
        
import timeit
#t = timeit.Timer(stmt="sb_eval(iter=1)", setup="from __main__ import sb_eval")  
#print t.timeit(number=1)
t = timeit.Timer(stmt="inc_sb_rl_test(iter=1)", setup="from __main__ import inc_sb_rl_test")  
print t.timeit(number=10000)
