import logging
import numpy as np
import scipy.linalg as la

class SparseBayes(object):
    def __init__(self):
        self.appLogger = logging.getLogger('SparseBayes')
        if id(np.dot) == id(np.core.multiarray.dot):
            print "Not using blas/lapack!"
        self.GAUSSIAN_SNR_INIT = 0.1
        self.INIT_ALPHA_MAX = 1e3
        self.INIT_ALPHA_MIN = 1e-3
        self.ALIGNMENT_ZERO = 1e-3
        self.CONTROL_ZeroFactor = 1e-12
        self.CONTROL_MinDeltaLogAlpha = 1e-3
        self.CONTROL_MinDeltaLogBeta = 1e-6
        self.CONTROL_PriorityAddition = False
        self.CONTROL_PriorityDeletion = True
        self.CONTROL_BetaUpdateStart = 10
        self.CONTROL_BetaUpdateFrequency = 5
        self.CONTROL_BetaMaxFactor = 1e6
        self.CONTROL_PosteriorModeFrequency = 1
        self.CONTROL_BasisAlignmentTest = True
        self.CONTROL_AlignmentMax = 1 - self.ALIGNMENT_ZERO
        self.OPTION_iteration = 100#00
        self.SETTING_noiseStdDev = 0.1
        self.ACTION_REESTIMATE = 0
        self.ACTION_ADD = 1
        self.ACTION_DELETE = -1
        self.ACTION_TERMINATE = 10
        self.ACTION_NOISE_ONLY = 11
        self.ACTION_ALIGNMENT_SKIP = 12

    def preprocess(self,BASIS):
        N,M = BASIS.shape
        Scales = np.atleast_2d(np.sqrt((BASIS**2).sum(axis=0))).T
        Scales[Scales==0] = 1
        
        for m in range(M):
            BASIS[:,m] = BASIS[:,m]/Scales[m]
            
        return BASIS,Scales
    
    def initialize(self,BASIS,Targets):
        # preprocess
        BASIS,Scales = self.preprocess(BASIS)
        
        # beta
        if True:
            beta = 1/self.SETTING_noiseStdDev**2
        else:
            stdt = max([1e-6,np.std(Targets)])
            beta = 1/(stdt*self.GAUSSIAN_SNR_INIT)**2
            
        
        # PHI
        proj = np.dot(BASIS.T,Targets)
        Used = np.array([np.argmax(np.abs(proj))])
#        print Used
        PHI = BASIS[:,Used]
#        print BASIS
#        print PHI
        N,M = PHI.shape
        # Mu
        Mu = np.array([])
        
        # hyperparameters: Alpha
        s = np.diag(np.dot(PHI.T,PHI))*beta
        q = np.dot(PHI.T,Targets)*beta
        Alpha = s**2/(q**2-s)
        Alpha[Alpha<0] = self.INIT_ALPHA_MAX
        if M == 1:
            print 'Initial alpha = %g'%Alpha
            
        return BASIS,Scales,Alpha,beta,Mu,PHI,Used
    
    def full_statistics(self,BASIS,PHI,Targets,Used,Alpha,beta,BASIS_PHI,BASIS_Targets):
#        print 'full_statistics'
#        print BASIS,PHI,Targets,Used,Alpha,beta,Mu,BASIS_PHI,BASIS_Targets

        MAX_POSTMODE_ITS = 25
        try:
            N,M_full = BASIS.shape
        except ValueError:
            M_full = 1
        try:
            n,M = PHI.shape
        except ValueError:
            M = 1
    
#        print np.dot(PHI.T,PHI)*beta+np.diag(Alpha)
        # posterior
#        print PHI
#        print np.dot(PHI.T,PHI)*beta
#        print np.diag(Alpha.ravel(),k=0)
#        print np.dot(PHI.T,PHI)*beta+np.diag(Alpha.ravel(),k=0)
        U = la.cholesky(np.dot(PHI.T,PHI)*beta+np.diag(Alpha.ravel(),k=0))
#        print U
        Ui = la.inv(U)
#        print Ui
        SIGMA = np.dot(Ui,Ui.T)
        
        Mu = np.dot(SIGMA,np.dot(PHI.T,Targets))*beta
#        print Mu
        
        y = np.dot(PHI,Mu)
        e = Targets - y
        ED = np.dot(e.T,e)
        
        dataLikely = (N*np.log(beta) - beta*ED)/2
        
        # log marginal likelihood
        logdetHOver2 = np.atleast_2d(np.sum(np.log(np.diag(U)))).T
        logML = dataLikely - np.dot((Mu**2).T,Alpha)/2 + np.sum(np.log(Alpha))/2 - logdetHOver2
        
        # well-determinedness factors
        DiagC = np.atleast_2d(np.sum(Ui**2,1)).T
        Gamma = 1 - Alpha * DiagC #TBA
        
        # Q & S
        betaBASIS_PHI = beta*BASIS_PHI
        S_in = beta - np.atleast_2d(np.sum(np.dot(betaBASIS_PHI,Ui)**2,1)).T #TBA
        Q_in = beta * (BASIS_Targets - np.dot(BASIS_PHI,Mu))
#        print Q_in
        
        S_out = S_in.copy()
        Q_out = Q_in.copy()
        
        S_out[Used] = (Alpha * S_in[Used])/(Alpha - S_in[Used])
        Q_out[Used] = (Alpha * Q_in[Used])/(Alpha - S_in[Used])
        
        Factor = Q_out * Q_out - S_out

#        print SIGMA,Mu,S_in,Q_in,S_out,Q_out,Factor,logML,Gamma,betaBASIS_PHI,beta
        
        return SIGMA,Mu,S_in,Q_in,S_out,Q_out,Factor,logML,Gamma,betaBASIS_PHI,beta
        
    def sequential_update(self,Targets,Scales,BASIS,PHI,BASIS_PHI,BASIS_Targets,\
                               Used,Alpha,beta,Aligned_out,Aligned_in,align_defer_count,\
                               SIGMA,Mu,S_in,Q_in,S_out,Q_out,Factor,logML,Gamma,BASIS_B_PHI):
        # diagnosis
        update_count = 0
        add_count = 0
        delete_count = 0
        
        try:
            N,M_full = BASIS.shape
        except ValueError:
            M_full = 1
        try:
            n,M = PHI.shape
        except ValueError:
            M = 1

        i = 0;full_count = 0
        LAST_ITERATION = False
        
        while (not LAST_ITERATION):
#            print 'Main loop'
            i += 1
            
#            print Alpha
            # decision phase
            DeltaML = np.zeros((M_full,1))
            Action = self.ACTION_REESTIMATE*np.ones((M_full,1))
            UsedFactor = Factor[Used]
#            print UsedFactor
            
            # re-estimation: must be a positive 'factor' and already in the model
            iu = np.ravel(UsedFactor > self.CONTROL_ZeroFactor)
#            print self.CONTROL_ZeroFactor
#            print iu
            index = Used[iu]
#            print index
            new_Alpha = S_out[index]**2/Factor[index]
#            print new_Alpha
            Delta = 1/new_Alpha - 1/Alpha[iu]
#            print Delta
            # quick computation of change in log-likelihood given all re-estimations
            DeltaML[index] = (Delta * (Q_in[index]**2)/(Delta * S_in[index] + 1) - np.log(1 + S_in[index] * Delta))/2
#            print DeltaML
            # deletion: if negative factor and in model
            iu = np.logical_not(iu)
            index = Used[iu]
            any_to_delete = True if len(index) > 0 else False
            if any_to_delete:
                # quick computation of change in log-likelihood given all deletions
                DeltaML[index] = -(Q_out[index]**2/(S_out[index] - Alpha[iu]) - np.log(1 + S_out[index] / Alpha[iu]))/2
                Action[index] = self.ACTION_DELETE
            
            # addition: must be a positive factor and out of the model
#            GoodFactor = (Factor > self.CONTROL_ZeroFactor).copy()
            GoodFactor = Factor > self.CONTROL_ZeroFactor
#            print 'GoodFactor: %s'%str(GoodFactor)
            GoodFactor[Used] = False
#            print 'Used: %s'%str(Used)
#            print 'GoodFactor: %s'%str(GoodFactor)
            if self.CONTROL_BasisAlignmentTest:
                try:
#                    print 'Aligned_out: %s'%str(Aligned_out)
                    GoodFactor[Aligned_out] = False
#                    print 'GoodFactor: %s'%str(GoodFactor)
                except IndexError:
#                    print 'Index Error'
                    pass
            index = GoodFactor.nonzero()
            any_to_add = True if len(index) > 0 else False
            if any_to_add:
                # quick computation of change in log-likelihood given all additions
                quot = Q_in[index]**2/S_in[index]
                DeltaML[index] = (quot - 1 - np.log(quot))/2
                Action[index] = self.ACTION_ADD
#            print DeltaML
#            print Action
            # preference
            if (any_to_add and self.CONTROL_PriorityAddition) or \
            (any_to_delete and self.CONTROL_PriorityDeletion):
                # We won't perform re-estimation this iteration, which we achieve by
                # zero-ing out the delta
                DeltaML[Action==self.ACTION_REESTIMATE] = 0
                #Furthermore, we should enforce ADD if preferred and DELETE is not
                # - and vice-versa
                if any_to_add and self.CONTROL_PriorityAddition and not self.CONTROL_PriorityDeletion:
                    DeltaML[Action==self.ACTION_DELETE] = 0
                if any_to_delete and self.CONTROL_PriorityDeletion and not self.CONTROL_PriorityAddition:
                    DeltaML[Action==self.ACTION_ADD] = 0
#            print DeltaML
            # choose the action that results in the greatest change in likelihood
            delta_log_marginal,nu = DeltaML.max(axis=0),DeltaML.argmax(axis=0)
#            print delta_log_marginal
#            print nu
            selected_Action = Action[nu]
#            print selected_Action
            any_worthwhile_Action = delta_log_marginal > 0
#            print any_worthwhile_Action
            
            # need to note if basis nu is already in the model, and if so,
            # find its interior index, denoted by "j"
            if selected_Action == self.ACTION_REESTIMATE or selected_Action == self.ACTION_DELETE:
                j = (Used==nu).nonzero()
                j = j[0] if len(j) < 2 else j
#                print j
                
            
            # get the individual basis vector for update and compute its optimal alpha
            Phi = BASIS[:,nu]
#            print Phi
            new_Alpha = S_out[nu]**2/Factor[nu]
#            print new_Alpha
            
            # terminate conditions
            if not any_worthwhile_Action or\
            (selected_Action == self.ACTION_REESTIMATE and \
             np.abs(np.log(new_Alpha) - np.log(Alpha[j])) < self.CONTROL_MinDeltaLogAlpha and \
             not any_to_delete):
                print 'No worthwhile action'
                selected_Action = self.ACTION_TERMINATE
                
            # alignment checks
            if self.CONTROL_BasisAlignmentTest:
                if selected_Action == self.ACTION_ADD:
                    # rule out addition if the new basis vector is aligned too closely to
                    # one or more already in the model
#                    print 'Phi %s'%str(Phi)
#                    print 'PHI %s'%str(PHI)
                    p = np.dot(Phi.T,PHI)
#                    print 'p %s'%str(p)
                    find_Aligned = (p.ravel() > self.CONTROL_AlignmentMax).nonzero()
 #                   print 'find_Aligned %s'%str(find_Aligned)
                    num_Aligned = find_Aligned[0].size
 #                   print 'num_Aligned %d'%num_Aligned
                    if num_Aligned > 0:
                        # the added basis function is effectively indistinguishable from one present already
                        selected_Action = self.ACTION_ALIGNMENT_SKIP
                        align_defer_count += 1
                        print 'Aligned_out %s'%str(Aligned_out)
                        print 'nu %s'%str(nu)
                        print 'num_Aligned %d'%num_Aligned
                        print 'dot %s'%str(nu.repeat(num_Aligned))
#                        Aligned_out = np.concatenate((Aligned_out,np.dot(nu,np.ones((num_Aligned,1)))))
                        Aligned_out = np.concatenate((Aligned_out,nu.repeat(num_Aligned))).astype('int')
                        print 'Aligned_out %s'%str(Aligned_out)
#                        print 'Used[find_Aligned] %s'%str(Used[find_Aligned])
                        Aligned_in = np.concatenate((Aligned_in,Used[find_Aligned])).astype('int')
#                        print 'Aligned_in %s'%str(Aligned_in)
                if selected_Action == self.ACTION_DELETE:
                    # reinstate any previously deferred basis functions resulting from this basis function
                    find_Aligned = (Aligned_in == nu).nonzero()
                    num_Aligned = find_Aligned[0].size
                    if num_Aligned > 0:
                        print 'del Aligned_out %s'%str(Aligned_out)
                        print 'del find_Aligned %s'%str(find_Aligned)
                        reinstated = Aligned_out[find_Aligned]
                        Aligned_in = np.delete(Aligned_in,find_Aligned)
                        Aligned_out = np.delete(Aligned_out,find_Aligned)
#                        print 'del Aligned_out %s'%str(Aligned_out)
#                        print 'del Aligned_in %s'%str(Aligned_in)
            
            # action phase
            # note if we've made a change which necessitates later updating of the statistics
            UPDATE_REQUIRED = False
            
            if selected_Action == self.ACTION_REESTIMATE:
                # basis function 'nu' is already in the model,
                # and we're re-estimating its corresponding alpha
                old_Alpha = Alpha[j]
                Alpha[j] = new_Alpha
#                s_j = SIGMA[:,j].copy()
                s_j = SIGMA[:,j]
                deltaInv = 1/(new_Alpha - old_Alpha)
                kappa = 1/(SIGMA[j,j] + deltaInv)
                tmp = kappa * s_j
                SIGMANEW = SIGMA - np.dot(tmp,s_j.T)
                deltaMu = -Mu[j] * tmp
                Mu = Mu + deltaMu
                
                S_in = S_in + kappa * np.dot(BASIS_B_PHI,s_j)**2
                Q_in = Q_in - np.dot(BASIS_B_PHI,deltaMu)
                
                update_count += 1
                UPDATE_REQUIRED = True
            elif selected_Action == self.ACTION_ADD:
                # basis function nu is not in the model, and we're adding it in
                BASIS_Phi = np.dot(BASIS.T,Phi)
                BASIS_PHI = np.hstack((BASIS_PHI,BASIS_Phi))
                B_Phi = beta * Phi
                BASIS_B_Phi = beta * BASIS_Phi
                tmp = np.dot(np.dot(B_Phi.T,PHI),SIGMA).T
                Alpha = np.vstack((Alpha,new_Alpha))
                PHI = np.hstack((PHI,Phi))
                s_ii = 1/(new_Alpha + S_in[nu])
                s_i = -(s_ii * tmp)
                TAU = -np.dot(s_i,tmp.T)
                SIGMANEW = np.vstack((np.hstack((SIGMA+TAU,s_i)),np.hstack((s_i.T,s_ii))))
#                SIGMANEW = np.vstack((np.hstack((SIGMA+TAU,s_i)),np.hstack((s_i.T,np.atleast_2d(s_ii)))))
                mu_i = s_ii * Q_in[nu]
                deltaMu = np.vstack((-mu_i*tmp,mu_i))
                Mu = np.vstack((Mu,0)) + deltaMu
                
                mCi = BASIS_B_Phi - np.dot(BASIS_B_PHI,tmp)
                S_in = S_in - s_ii * mCi**2
#                print Q_in,mu_i,mCi
                Q_in = Q_in - mu_i * mCi
#                print Q_in
                
                Used = np.concatenate((Used,nu))
                
                add_count += 1
                UPDATE_REQUIRED = True
            elif selected_Action == self.ACTION_DELETE:
                # basis function nu is in the model, but we're removing it
                BASIS_PHI = np.delete(BASIS_PHI,j,1)
                PHI = np.delete(PHI,j,1)
                Alpha = np.delete(Alpha,j,0)
#                BASIS_PHI[:,j] = np.array([])
#                PHI[:,j] = np.array([])
#                Alpha[j] = np.array([])
#                s_jj = SIGMA[j,j].copy()
                s_jj = SIGMA[j,j]
#                s_j = SIGMA[:,j].copy()
                s_j = SIGMA[:,j]
                tmp = s_j/s_jj
                SIGMANEW = SIGMA - np.dot(tmp,s_j.T)
                SIGMANEW = np.delete(SIGMANEW,j,0)
                SIGMANEW = np.delete(SIGMANEW,j,1)
#                SIGMANEW[j,:] = np.array([])
#                SIGMANEW[:,j] = np.array([])
                deltaMu = -Mu[j] * tmp
#                mu_j = Mu[j].copy()
                mu_j = Mu[j]
                Mu = Mu + deltaMu
                Mu = np.delete(Mu,j,0)
#                Mu[j] = np.array([])
                
                jPm = np.dot(BASIS_B_PHI,s_j)
                S_in = S_in + jPm**2/s_jj
                Q_in = Q_in + (jPm * mu_j)/s_jj
                
                Used = np.delete(Used,j,0)
#               Used[j] = np.array([])

                delete_count += 1
                UPDATE_REQUIRED = True
                
            M = len(Used)
            if M == 0:
                raise RuntimeError
            
            # update statistics
            if UPDATE_REQUIRED:
                # S_in and S_out values were calculated earlier
                # Here update the S_out and Q_out values and relevance factors
                S_out = S_in.copy()
                Q_out = Q_in.copy()
                tmp = Alpha/(Alpha - S_in[Used])
                S_out[Used] = tmp * S_in[Used]
                Q_out[Used] = tmp * Q_in[Used]
#                print Q_in
                Factor = Q_out * Q_out - S_out
#                print Q_in
#                SIGMA = SIGMANEW.copy()
                SIGMA = SIGMANEW
                Gamma = 1 - np.ravel(Alpha) * np.diag(SIGMA)
                BASIS_B_PHI = beta * BASIS_PHI
            
            logML = logML + delta_log_marginal
            
            # Gaussian noise estimate
            betaZ1 = beta
            y = np.dot(PHI,Mu)
            e = Targets - y
            if not np.dot(e.T,e) == 0:
                beta = (N - np.sum(Gamma))/np.dot(e.T,e)
                # work-around zero-noise issue
                if np.var(Targets) > 0:
                    beta = np.min(np.vstack((beta,self.CONTROL_BetaMaxFactor/np.var(Targets))))
            else:
                beta = self.CONTROL_BetaMaxFactor

            delta_log_beta = np.log(beta) - np.log(betaZ1)
            
            if np.abs(delta_log_beta) > self.CONTROL_MinDeltaLogBeta:
#                print 'Update beta'
#                print BASIS,PHI,Targets,Used,Alpha,beta,Mu,BASIS_PHI,BASIS_Targets
                SIGMA,Mu,S_in,Q_in,S_out,Q_out,Factor,logML,Gamma,BASIS_B_PHI,beta = \
                self.full_statistics(BASIS,PHI,Targets,Used,Alpha,beta,BASIS_PHI,BASIS_Targets)
                full_count += 1
#                print SIGMA,Mu,S_in,Q_in,S_out,Q_out,Factor,logML,Gamma,BASIS_B_PHI,beta
#                print beta
#                print Factor
#                if selected_Action == self.ACTION_TERMINATE:
#                    selected_Action = self.ACTION_NOISE_ONLY
            
            if selected_Action == self.ACTION_TERMINATE:
                break
            
            # check for "natural" termination
            if i == self.OPTION_iteration:
                LAST_ITERATION = True
            
#            print '%5d> L = %.6f\t Gamma = %.2f (M = %d)\t s=%.3f'%(i,logML/N,np.sum(Gamma),M,np.sqrt(1/beta))
            pass
        # post-process
        self.appLogger.info('%5d> L = %.6f\t Gamma = %.2f (M = %d)\t s=%.3f'%(i,logML/N,np.sum(Gamma),M,np.sqrt(1/beta)))
        if selected_Action != self.ACTION_TERMINATE:
            self.appLogger.info('Iteration limit: algorithm did not converge')
        else:
            self.appLogger.info('** Stopping at iteration %d (Max_delta_ml=%g) **'%(i,delta_log_marginal))
                
        Relevant,index = np.sort(Used),np.argsort(Used)
        Mu = Mu[index] / Scales[Used[index]]
        Alpha = Alpha[index] / Scales[Used[index]]**2
        
        return Used,Alpha,beta,Aligned_out,Aligned_in,align_defer_count,\
            Relevant,Mu,Alpha,beta,update_count,add_count,delete_count,full_count    

    def learn(self,X,Targets,basis_func,extendable=True):
        BASIS = basis_func(X)
        
        # initialization
        print 'Initialization'
        BASIS,Scales,Alpha,beta,Mu,PHI,Used = self.initialize(BASIS,Targets)
#        print BASIS,Scales,Alpha,beta,Mu,PHI,Used
        
        BASIS_PHI = np.dot(BASIS.T,PHI)
        BASIS_Targets = np.dot(BASIS.T,Targets)
        
        # full computation
        print 'Full computation'
        SIGMA,Mu,S_in,Q_in,S_out,Q_out,Factor,logML,Gamma,BASIS_B_PHI,beta = \
        self.full_statistics(BASIS,PHI,Targets,Used,Alpha,beta,BASIS_PHI,BASIS_Targets)
        
        Aligned_out = np.array([])
        Aligned_in = np.array([])
        align_defer_count = 0

        Used,Alpha,beta,\
        Aligned_out,Aligned_in,align_defer_count,\
        Relevant,Mu,Alpha,beta,update_count,add_count,delete_count,full_count = \
        self.sequential_update(Targets,Scales,BASIS,PHI,BASIS_PHI,BASIS_Targets,\
                               Used,Alpha,beta,Aligned_out,Aligned_in,align_defer_count,\
                               SIGMA,Mu,S_in,Q_in,S_out,Q_out,Factor,logML,Gamma,BASIS_B_PHI)
        
        if extendable:
            self.X,self.Targets,self.BASIS,self.Used,\
            self.Alpha,self.beta,\
            self.Aligned_out,self.Aligned_in,self.align_defer_count =\
            X,Targets,BASIS,Used,\
            Alpha,beta,\
            Aligned_out,Aligned_in,align_defer_count
        
        return Relevant,Mu,Alpha,beta,update_count,add_count,delete_count,full_count
                
    def incremental_learn(self,new_X,new_T,inc_basis_func,extendable=True):

        try:
            X,Targets,BASIS,Used,\
            Alpha,beta,\
            Aligned_out,Aligned_in,align_defer_count = \
            self.X,self.Targets,self.BASIS,self.Used,\
            self.Alpha,self.beta,\
            self.Aligned_out,self.Aligned_in,self.align_defer_count
#        except NameError:
        except:
            return self.learn(new_X,new_T,inc_basis_func)
#            print "First, use 'learn' method with extendable=True"

#        X = np.vstack((X,new_X))
        X += new_X
        Targets = np.vstack((Targets,new_T))
        BASIS = inc_basis_func(X,BASIS)
            
        # pre-process
        print 'Pre-process'
        BASIS,Scales = self.preprocess(BASIS)
        
        PHI = BASIS[:,Used]
#        print BASIS,Scales,Alpha,beta,Mu,PHI,Used
        
        BASIS_PHI = np.dot(BASIS.T,PHI)
        BASIS_Targets = np.dot(BASIS.T,Targets)
        
        # full computation
        print 'Full computation'
        SIGMA,Mu,S_in,Q_in,S_out,Q_out,Factor,logML,Gamma,BASIS_B_PHI,beta = \
        self.full_statistics(BASIS,PHI,Targets,Used,Alpha,beta,BASIS_PHI,BASIS_Targets)
        
        Used,Alpha,beta,\
        Aligned_out,Aligned_in,align_defer_count,\
        Relevant,Mu,Alpha,beta,update_count,add_count,delete_count,full_count = \
        self.sequential_update(Targets,Scales,BASIS,PHI,BASIS_PHI,BASIS_Targets,\
                               Used,Alpha,beta,Aligned_out,Aligned_in,align_defer_count,\
                               SIGMA,Mu,S_in,Q_in,S_out,Q_out,Factor,logML,Gamma,BASIS_B_PHI)

        if extendable:
            self.X,self.Targets,self.BASIS,self.Used,\
            self.Alpha,self.beta,\
            self.Aligned_out,self.Aligned_in,self.align_defer_count =\
            X,Targets,BASIS,Used,\
            Alpha,beta,\
            Aligned_out,Aligned_in,align_defer_count
        
        return Relevant,Mu,Alpha,beta,update_count,add_count,delete_count,full_count
                
    def get_basis_size(self):
        try: 
            return len(self.X)
        except:
            return 0
    
    def get_basis_points(self):
        return self.X
