'''

'''

import os
import logging
from GlobalConfig import GetConfig
from BeliefState import BeliefState
from DB import GetDB
from DialogModules import SystemAction
import numpy as np
import pickle
from SparseBayes import SparseBayes

MY_ID = 'DialogManager'

class DialogManager(object):
    '''
    Base class.  Not meant to be instantiated on its own.
    '''
    def __init__(self):
        self.appLogger = logging.getLogger('Learning')
        self.appLogger.info('DialogManager init')
        self.config = GetConfig()
        self.beliefState = BeliefState()
#        self.appLogger.info('DialogManager init2')
        self.db = GetDB()
#        self.fields = self.db.GetFields()
#        self.appLogger.info('DialogManager init3')
        self.prompts = LetsGoPrompts()
        self.appLogger.info('DialogManager init done')


    def Init(self):
        pass

    def TakeTurn(self,asrResult):
        pass

class SBSarsaDialogManager(DialogManager):
    '''
    See module header for a description.
    '''
    def __init__(self):
        DialogManager.__init__(self)
        self.appLogger.info('SBSarsaDialogManager init')
        self.fields = ['route','departure_place','arrival_place','travel_time']
#        self.rewardDiscountFactor = self.config.getfloat(MY_ID,'rewardDiscountFactor')
#        self.taskSuccessReward = self.config.getfloat(MY_ID,'taskSuccessReward')
#        self.taskFailureReward = self.config.getfloat(MY_ID,'taskFailureReward')
#        self.taskProceedReward = self.config.getfloat(MY_ID,'taskProceedReward')
#        self.acceptThreshold = self.config.getfloat(MY_ID,'acceptThreshold')
#        self.basisWidth = self.config.getfloat(MY_ID,'basisWidth')
#        self.confidenceScoreCalibration = self.config.getboolean(MY_ID,'confidenceScoreCalibration')
        self._LoadConfig()
#        self.appLogger.info('SBSarsaDialogManager init 1')
        
        if self.basisFunction == 'gaussian':
            self._basis_matrix = self._gaussian_basis_matrix
            self._basis_vector = self._gaussian_basis_vector
        elif self.basisFunction == 'polynomial':
            self._basis_matrix = self._polynomial_basis_matrix
            self._basis_vector = self._polynomial_basis_vector
            
        self.sb = SparseBayes()
#        self.appLogger.info('SBSarsaDialogManager init 2')
        modelPath = self.config.get('Global','modelPath')
        if self.confidenceScoreCalibration:
            self.appLogger.info('Apply confidence score calibration')
            self.sbr_model = {'route':pickle.load(open(os.path.join(modelPath,'_calibrated_confidence_score_sbr_bn.model'),'rb')),\
                              'departure_place':pickle.load(open(os.path.join(modelPath,'_calibrated_confidence_score_sbr_dp.model'),'rb')),\
                              'arrival_place':pickle.load(open(os.path.join(modelPath,'_calibrated_confidence_score_sbr_ap.model'),'rb')),\
                              'travel_time':pickle.load(open(os.path.join(modelPath,'_calibrated_confidence_score_sbr_tt.model'),'rb')),\
                              'affirm':pickle.load(open(os.path.join(modelPath,'_calibrated_confidence_score_sbr_yes.model'),'rb')),\
                              'deny':pickle.load(open(os.path.join(modelPath,'_calibrated_confidence_score_sbr_no.model'),'rb')),\
                              'multi2':pickle.load(open(os.path.join(modelPath,'_calibrated_confidence_score_sbr_multi2.model'),'rb')),\
                              'multi3':pickle.load(open(os.path.join(modelPath,'_calibrated_confidence_score_sbr_multi3.model'),'rb')),\
                              'multi4':pickle.load(open(os.path.join(modelPath,'_calibrated_confidence_score_sbr_multi4.model'),'rb'))
                              }
#        self.appLogger.info('SBSarsaDialogManager init 3')

        if not self.dialogStrategyLearning:
            self.Relevant = pickle.load(open(os.path.join(modelPath,'Relevant.model'),'r'))
            self.Mu = pickle.load(open(os.path.join(modelPath,'Mu.model'),'r'))
            self.X = pickle.load(open(os.path.join(modelPath,'DataPoints.model'),'r'))
            self.sizeX = len(self.X)
        self.appLogger.info('SBSarsaDialogManager init done')

    def Init(self,userFirst=False):
        from copy import deepcopy
        
#        self.userGoal = userGoal
        self.beliefState.Init()
        self.fieldCounts = dict([(field,0) for field in self.fields])
        self.fieldCounts['all'] = 0
        self.routeConfirmCount = 0
        self.sysActHistory = []
        sysAction,Qval = self._ChooseAction(userFirst=userFirst)
        self.prevSysAction = sysAction
#        self.appLogger.info('prevSysAction %s'%str(self.prevSysAction))
        self.prevAsrResult = None
#        self.dialogResult = False
#        self.dialogReward = 0
        return deepcopy(sysAction)

    def _LoadConfig(self):
        self.dialogStrategyLearning = self.config.getboolean(MY_ID,'dialogStrategyLearning')
        self.fieldAcceptThreshold = self.config.getfloat(MY_ID,'fieldAcceptThreshold')
        self.fieldRejectThreshold = self.config.getfloat(MY_ID,'fieldRejectThreshold')
        self.rewardDiscountFactor = self.config.getfloat(MY_ID,'rewardDiscountFactor')
        self.taskSuccessReward = self.config.getfloat(MY_ID,'taskSuccessReward')
        self.taskFailureReward = self.config.getfloat(MY_ID,'taskFailureReward')
        self.taskProceedReward = self.config.getfloat(MY_ID,'taskProceedReward')
        self.acceptThreshold = self.config.getfloat(MY_ID,'acceptThreshold')
        self.basisFunction = self.config.get(MY_ID,'basisFunction')
        self.basisWidth = self.config.getfloat(MY_ID,'basisWidth')
        self.confidenceScoreCalibration = self.config.getboolean(MY_ID,'confidenceScoreCalibration')
        self.preferNaturalSequence = self.config.getboolean(MY_ID,'preferNaturalSequence')
        self.useDirectedOpenQuestion = self.config.getboolean(MY_ID,'useDirectedOpenQuestion')
         
    def ReloadConfig(self):
        self._LoadConfig()
        self.sb.reload_config()
    
#    def DialogResult(self):
#        return (self.dialogResult,self.dialogReward)

    def Calibrate(self,asrResult):
        def dist_squared(X,Y):
            nx = X.shape[0]
            ny = Y.shape[0]
            return np.dot(np.atleast_2d(np.sum((X**2),1)).T,np.ones((1,ny))) + \
                np.dot(np.ones((nx,1)),np.atleast_2d(np.sum((Y**2),1))) - 2*np.dot(X,Y.T);
    
        def basis_vector(X,x,basisWidth):
            BASIS = np.exp(-dist_squared(x,X)/(basisWidth**2))
            return BASIS

        sbr_model = None
        if len(asrResult.userActions) == 1:
            try:
                if asrResult.userActions[0].content.keys()[0] == 'confirm':
                    if asrResult.userActions[0].content['confirm'] == 'YES':
                        sbr_model = self.sbr_model['affirm']
                    else:
                        sbr_model = self.sbr_model['deny']
                else:
                    sbr_model = self.sbr_model[asrResult.userActions[0].content.keys()[0]]
            except:
                pass
        elif len(asrResult.userActions) == 2:
            sbr_model = self.sbr_model['multi2']
        elif len(asrResult.userActions) == 3:
            sbr_model = self.sbr_model['multi3']
        else:
            sbr_model = self.sbr_model['multi4']
        
        if sbr_model:
            asrResult.probs[0] = np.dot(basis_vector(sbr_model['data_points'],\
                                                     np.array([[asrResult.probs[0]]]),\
                                                     sbr_model['basis_width']),\
                                        sbr_model['weights'])[0,0]
            if asrResult.probs[0] < 0: asrResult.probs[0] = 0
         
    def TakeTurn(self,asrResult,reward=0):
        from copy import deepcopy
        # terminal case
        if asrResult == None:
#            reward = self._GetReward(self.beliefState,sysAction)
#            self.dialogReward += reward
            if self.dialogStrategyLearning:
                self._SBSarsa(self.prevTopBelief,self.prevTopFields,self.prevMarginals,\
                              self.prevSysAction,reward,0,self.prevAsrResult)
#            if reward == self.taskSuccessReward:
#                self.dialogResult = True
            return None
            
        if self.confidenceScoreCalibration:
            self.appLogger.info('asrResult %s'%asrResult)
#            asrResult = deepcopy(asrResult)
            self.Calibrate(asrResult)
            self.appLogger.info('Calibrated asrResult %s'%asrResult)
        if self.dialogStrategyLearning:
            self.prevTopBelief = self.beliefState.GetTopUserGoalBelief()
            self.prevTopFields = deepcopy(self.beliefState.GetTopUserGoal())
            self.prevMarginals = deepcopy(self.beliefState.GetMarginals())
    #        reward = self._GetReward(self.beliefState,self.prevSysAction)
#        self.dialogReward += reward
#        self.appLogger.info('prevSysAction for update %s'%str(self.prevSysAction))
        self.beliefState.Update(asrResult,self.prevSysAction)
        self.appLogger.info('** PartitionDistribution: **\n%s'%(self.beliefState))
        sysAction,Qval = self._ChooseAction(asrResult)
        if self.dialogStrategyLearning:
            self._SBSarsa(self.prevTopBelief,self.prevTopFields,self.prevMarginals,\
                          self.prevSysAction,reward,Qval,self.prevAsrResult)
        self.prevSysAction = sysAction
#        self.appLogger.info('new prevSysAction %s'%str(self.prevSysAction))

        if self.dialogStrategyLearning:
            self.prevAsrResult = asrResult
        # terminal case
#        if sysAction.type == 'inform':
#            reward = self._GetReward(self.beliefState,sysAction)
#            self.dialogReward += reward
#            self._SBSarsa(self.beliefState.GetTopUserGoalBelief(),self.beliefState.GetTopUserGoal(),\
#                          self.beliefState.GetMarginals(),sysAction,reward,0,asrResult)
#            if reward == self.taskSuccessReward:
#                self.dialogResult = True
        return deepcopy(sysAction)

#    def _GetReward(self,beliefState,sysAction):
#        if sysAction.type == 'inform':
#            field = beliefState.GetTopUserGoal()
#            if self.userGoal['Bus number'] == '' and field['route'].type == 'equals':
#                return self.taskFailureReward
#            if self.userGoal['Bus number'] != '' and field['route'].type != 'equals':
#                return self.taskFailureReward
#            if self.userGoal['Bus number'] != '' and self.userGoal['Bus number'] != field['route'].equals:
#                return self.taskFailureReward
#            if self.userGoal['Departure place'] == '' and field['departure_place'].type == 'equals':
#                return self.taskFailureReward
#            if self.userGoal['Departure place'] != '' and field['departure_place'].type != 'equals':
#                return self.taskFailureReward
#            if self.userGoal['Departure place'] != '' and self.userGoal['Departure place'] != field['departure_place'].equals:
#                return self.taskFailureReward
#            if self.userGoal['Arrival place'] == '' and field['arrival_place'].type == 'equals':
#                return self.taskFailureReward
#            if self.userGoal['Arrival place'] != '' and field['arrival_place'].type != 'equals':
#                return self.taskFailureReward
#            if self.userGoal['Arrival place'] != '' and self.userGoal['Arrival place'] != field['arrival_place'].equals:
#                return self.taskFailureReward
#            if self.userGoal['Travel time'] == '' and field['travel_time'].type == 'equals':
#                return self.taskFailureReward
#            if self.userGoal['Travel time'] != '' and field['travel_time'].type != 'equals':
#                return self.taskFailureReward
#            if self.userGoal['Travel time'] != '' and self.userGoal['Travel time'] != field['travel_time'].equals:
#                return self.taskFailureReward
#            return self.taskSuccessReward
#        else:
#            return self.taskProceedReward

    def _polynomial_basis_vector(self,XN,x):
        BASIS = np.zeros((len(XN),1))
        for i, xi in enumerate(XN):
            if xi[1] == x[1] and xi[2] == x[2]:
#            if xi[2] == x[2]:
                BASIS[i] = (np.dot(xi[0],x[0]) + 0.1)**2
        return BASIS
    
    def _polynomial_basis_matrix(self,X,BASIS=None):
        basis = np.zeros((len(X),1)) #+ np.atleast_2d(np.random.standard_normal(len(X))/1e10).T
        for i, xi in enumerate(X):
            if xi[1] == X[-1][1] and xi[2] == X[-1][2]:
#            if xi[2] == X[-1][2]:
                basis[i,0] += (np.dot(xi[0],X[-1][0]) + 0.1)**2
        if BASIS != None:
            BASIS = np.vstack((BASIS,np.atleast_2d(basis[:-1,0].T)))
            BASIS = np.hstack((BASIS,basis))
        else:
            BASIS = basis
        return BASIS

    def _gaussian_basis_vector(self,XN,x):
        BASIS = np.zeros((len(XN),1))
        for i, xi in enumerate(XN):
            ua_kernel = 0.5 if xi[1] != x[1] else 1.0
#            ua_kernel = 1.0
            if xi[2] == x[2]:
                BASIS[i] = np.exp(-(np.sum(xi[0]**2) + np.sum(x[0]**2) - 2*np.dot(xi[0],x[0]))/(self.basisWidth**2)) * ua_kernel
        return BASIS
        
    def _gaussian_basis_matrix(self,X,BASIS=None):
        basis = np.zeros((len(X),1)) #+ np.atleast_2d(np.random.standard_normal(len(X))/1e10).T
        for i, xi in enumerate(X):
            ua_kernel = 0.5 if xi[1] != X[-1][1] else 1.0
#            ua_kernel = 1.0
            if xi[2] == X[-1][2]:
                try:
                    basis[i,0] += np.exp(-(np.sum(xi[0]**2) + np.sum(X[-1][0]**2) - 2*np.dot(xi[0],X[-1][0]))/(self.basisWidth**2)) * ua_kernel
                except:
                    raise RuntimeError
        if BASIS != None:
            BASIS = np.vstack((BASIS,np.atleast_2d(basis[:-1,0].T)))
            BASIS = np.hstack((BASIS,basis))
        else:
            BASIS = basis
        return BASIS
        
    def GetBasisSize(self):
        if self.dialogStrategyLearning:
            return self.sb.get_basis_size()
        else:
            return self.sizeX

    def GetBasisPoints(self):
        if self.dialogStrategyLearning:
            return self.sb.get_basis_points()
        else:
            return self.X
        
    def _SBSarsa(self,topBelief,topFields,marginals,sysAction,reward,nextQval,asrResult):
        self.appLogger.info('reward %d'%reward)
        self.appLogger.info('nextQval %f'%nextQval)
        y = reward + nextQval * self.rewardDiscountFactor #+ np.random.standard_normal(1)[0]/1e10
        contX = [0.0] if topBelief == None else [topBelief]
        for field in self.fields:
            if (len(marginals[field]) > 0):
                contX.append(marginals[field][-1]['belief'])
            else:
                contX.append(0.0)
#        for field in self.fields: 
#            if topFields[field].type == 'equals':
#                contX.append(0.0)
#            else:
#                contX.append(1.0)
        userAct = 'None' if asrResult == None else str(asrResult.userActions[0]).split('=')[0]
        X = [np.array(contX),userAct,str(sysAction).split('=')[0]]
        try:
            self.Relevant,self.Mu,Alpha,beta,update_count,add_count,delete_count,full_count = \
            self.sb.incremental_learn([X],np.atleast_2d(y),self._basis_matrix)
            self.appLogger.info('Number of data points: %d'%self.GetBasisSize())
#            self._TraceQval()
        except RuntimeError,(XN,Y,raw_BASIS):
            self.appLogger.info('BASIS:\n %s'%str(raw_BASIS))
#            print 'BASIS:\n %s'%str(BASIS)
            self.sb = SparseBayes()
            self.Relevant,self.Mu,Alpha,beta,update_count,add_count,delete_count,full_count = \
            self.sb.incremental_learn(XN,Y,self._basis_matrix,raw_BASIS)
            
    def StoreModel(self,tag=''):
        import pickle
        pickle.dump(self.Relevant,open('Relevant-%s.model'%tag,'w'))
        pickle.dump(self.Mu,open('Mu-%s.model'%tag,'w'))
        pickle.dump(self.GetBasisPoints(),open('DataPoints-%s.model'%tag,'w'))        
    
    def GetPresentLearningStatus(self):
        return self.sb.get_present_learning_status()
    
    def SetLearningStatus(self,X,Targets,raw_BASIS,BASIS,Used,Alpha,beta,Aligned_out,Aligned_in,Relevant,Mu):
        self.Relevant,self.Mu = Relevant,Mu
        self.sb.set_learning_status(X,Targets,raw_BASIS,BASIS,Used,Alpha,beta,Aligned_out,Aligned_in,Relevant,Mu)
          
    def _TraceQval(self):
        import operator
        
        acts = ['[ask] request all','[ask] request route','[ask] request departure_place',\
                '[ask] request arrival_place','[ask] request travel_time',\
                '[ask] confirm route','[ask] confirm departure_place',\
                '[ask] confirm arrival_place','[ask] confirm travel_time',\
                '[inform]']
        
        w_infer = np.zeros((self.GetBasisSize(),1))
        w_infer[self.Relevant] = self.Mu 

        Bs = [np.array([0.25,0.25,0.25,0.25,0.25]),\
              np.array([0.5,0.5,0.5,0.5,0.5]),\
              np.array([0.75,0.75,0.75,0.75,0.75]),\
              np.array([0.99,0.99,0.99,0.99,0.99]),\
              np.array([0.5,0.25,0.5,0.5,0.5]),\
              np.array([0.75,0.25,0.75,0.75,0.75]),\
              np.array([0.99,0.25,0.99,0.99,0.99]),\
              ]
        self.appLogger.info('TraceQval:')
        for B in Bs:
            self.appLogger.info('%s'%str(B))
            Qvals = []
            for act in acts:
                X = [B,'',act]
                Qvals.append((act,np.dot(self._basis_vector(self.GetBasisPoints(),X).T,w_infer)[0,0]))
            Qvals = sorted(Qvals,key=lambda q:q[1],reverse=True)
            for Qval in Qvals:
                self.appLogger.info('%s:%f'%(Qval[0],Qval[1]))
                
    def _ChooseAction(self,asrResult=None,userFirst=False):
        import random
        
        # action list
        acts = ['[ask] request all','[ask] request departure_place',\
                '[ask] request arrival_place','[ask] request travel_time',\
                '[ask] confirm route','[ask] confirm departure_place',\
                '[ask] confirm arrival_place','[ask] confirm travel_time',\
                '[ask] confirm_immediate route','[ask] confirm_immediate departure_place',\
                '[ask] confirm_immediate arrival_place','[ask] confirm_immediate travel_time',\
                '[inform]']

        if self.useDirectedOpenQuestion:
            acts.remove('[ask] request all')
            self.appLogger.info('Exclude request all because of directed open question option')
        elif self.beliefState.GetTopUserGoalBelief() != 1.0:
            acts.remove('[ask] request all')
            self.appLogger.info('Exclude request all because it is allowed only as an initial act')

        if self.beliefState.GetTopUniqueMandatoryUserGoal() == 0.0:
            acts.remove('[inform]')
            self.appLogger.info('Exclude inform because of low top belief %f'%self.beliefState.GetTopUniqueMandatoryUserGoal())

        marginals = self.beliefState.GetMarginals()
        if self.preferNaturalSequence:
            if self.fieldCounts['departure_place'] == 0:
                if len(marginals['arrival_place']) == 0:
                    acts.remove('[ask] request arrival_place')
                    self.appLogger.info('Exclude request arrival_place for a natural sequence') 
                if len(marginals['travel_time']) == 0:
                    acts.remove('[ask] request travel_time')
                    self.appLogger.info('Exclude request travel_time for a natural sequence') 
            elif self.fieldCounts['arrival_place'] == 0:
                if len(marginals['travel_time']) == 0:
                    acts.remove('[ask] request travel_time')
                    self.appLogger.info('Exclude request travel_time for a natural sequence') 
        
        for field in self.fields: 
            if len(marginals[field]) == 0 or marginals[field][-1]['belief'] < self.fieldRejectThreshold:
                acts.remove('[ask] confirm %s'%field)
                acts.remove('[ask] confirm_immediate %s'%field)
                self.appLogger.info('Exclude confirm(_immediate) %s because of no value or very low marginal'%field)
            elif marginals[field][-1]['belief'] > self.fieldAcceptThreshold:
                if field != 'route':
                    acts.remove('[ask] request %s'%field)
                acts.remove('[ask] confirm %s'%field)
                acts.remove('[ask] confirm_immediate %s'%field)
                self.appLogger.info('Exclude request and confirm(_immediate) %s because of high belief'%field)
                self.appLogger.info('Max marginal of %s: %f'%(field,marginals[field][-1]['belief']))
            else:
                self.appLogger.info('Max marginal of %s: %f'%(field,marginals[field][-1]['belief']))

        for field in self.fields:
            if asrResult == None or asrResult.userActions[0].type != 'ig' or field not in asrResult.userActions[0].content:
                try:
                    acts.remove('[ask] confirm_immediate %s'%field)
                    self.appLogger.info('Exclude confirm_immediate %s because of no immediate value'%field)
                except:
                    self.appLogger.info('Exception while removing confirm_immediate %s'%field)

        if len(self.sysActHistory) > 1 and self.sysActHistory[-1] == self.sysActHistory[-2]:
            try:
                acts.remove(self.sysActHistory[-1])
                self.appLogger.info('Exclude %s because of repetition',self.sysActHistory[-1])
                if self.sysActHistory[-1].find('confirm') > -1:
                    acts.remove(self.sysActHistory[-1].replace('confirm','confirm_immediate'))
                    self.appLogger.info('Exclude %s because of repetition',self.sysActHistory[-1])
            except:
                self.appLogger.info('Exception while removing %s',self.sysActHistory[-1])
 
        if len(acts) == 0:
            acts = ['[ask] request departure_place',\
                    '[ask] request arrival_place','[ask] request travel_time']
            self.appLogger.info('Length of acts becomes zero')
                                                    
        act = ''
        if userFirst:
            act = '[ask] request all' 
            self.appLogger.info('Choose request all as an implicit start action')
        elif self.dialogStrategyLearning and self.GetBasisSize() == 0:
            act = random.choice(acts[:4])
        elif self.dialogStrategyLearning and random.random() < 0.1:
            act = random.choice(acts)
            self.appLogger.info('Exploration act: %s'%act)
#        elif self.beliefState.GetTopUniqueMandatoryUserGoal() > self.acceptThreshold:
#            act = acts[-1]
#            self.appLogger.info('Choose inform because of high top belief %f'%self.beliefState.GetTopUniqueMandatoryUserGoal())

#        if self.beliefState.GetTopUserGoalBelief() == 1.0:
#            act = '[ask] request all'
#            self.appLogger.info('Only request all is allowed as an initial act')

        contX = [self.beliefState.GetTopUserGoalBelief()]
        for field in self.fields:
            if (len(marginals[field]) > 0):
                contX.append(marginals[field][-1]['belief'])
            else:
                contX.append(0.0)
        
#        fields = self.beliefState.GetTopUserGoal()
#        for field in self.fields: 
#            if fields[field].type == 'equals':
#                contX.append(0.0)
#            else:
#                contX.append(1.0)
        try:
            w_infer = np.zeros((self.GetBasisSize(),1))
            w_infer[self.Relevant] = self.Mu 
            userAction = 'None' if not asrResult else str(asrResult.userActions[0]).split('=')[0]
            if act == '':
                strQvals = 'Q-values: [ '
                ys = np.array([])
                for act in acts:
                    X = [np.array(contX),userAction,act]
#                    print 'choose X:%s'%str(X)
    #                print ys
    #                print np.dot(self._basis_vector(self.GetBasisPoints(),X).T,w_infer).flatten()
                    ys = np.concatenate((ys,np.dot(self._basis_vector(self.GetBasisPoints(),X).T,w_infer).ravel()))
                    strQvals += '%s:%g '%(act,ys[-1])
                strQvals += ']'
                self.appLogger.info(strQvals)
                act = acts[ys.argmax(0)]
                Qval = ys.max(0)
            else:
                X = [np.array(contX),userAction,act]
                Qval = np.dot(self._basis_vector(self.GetBasisPoints(),X).T,w_infer)[0,0]
        except:
            self.appLogger.info('Cannot perform SBR inference')
            Qval = -1.0
            
        self.appLogger.info('Act %s, Qval: %g'%(act,Qval))
        
        if act == '[inform]':
#            belief = self.beliefState.GetTopUserGoalBelief()
            destination = ''
            surface = self.prompts.BusSchedule(None)
            sysAction = SystemAction('inform',content=None,surface=surface,destination=destination)
        else:
            type,force,field = act.split(' ')
            if force == 'request':
                surface = self.prompts.WHQuestion(field,self.fieldCounts[field])
                sysAction = SystemAction('ask','request',field,surface=surface,grammarName=field)
                self.fieldCounts[field] += 1
            elif force == 'confirm':
                surface = 'Is this right?'
                value = '' if len(marginals[field]) == 0 else marginals[field][-1]['equals']
                sysAction = SystemAction('ask','confirm',{field:value},surface=surface,grammarName='')
                self.fieldCounts[field] += 1
            elif force == 'confirm_immediate':
                surface = 'Is this right?'
                value = asrResult.userActions[0].content[field]
                sysAction = SystemAction('ask','confirm',{field:value},surface=surface,grammarName='')
                self.fieldCounts[field] += 1
        
        self.sysActHistory.append(str(sysAction).split('=')[0])
        return sysAction,Qval

class OpenDialogManager(DialogManager):
    '''
    See module header for a description.
    '''
    def __init__(self):
        DialogManager.__init__(self)
        self.fields = ['route','departure_place','arrival_place','travel_time']
        self.useAllGrammar = self.config.getboolean(MY_ID,'useAllGrammar')
        self.acceptThreshold = self.config.getfloat(MY_ID,'acceptThreshold')
        self.openQuestionThreshold = self.config.getfloat(MY_ID,'openQuestionThreshold')
        self.confirmRouteLowThreshold = self.config.getfloat(MY_ID,'confirmRouteLowThreshold')
        self.confirmRouteHighThreshold = self.config.getfloat(MY_ID,'confirmRouteHighThreshold')
        self.confirmDeparturePlaceHighThreshold = self.config.getfloat(MY_ID,'confirmDeparturePlaceHighThreshold')
        self.confirmArrivalPlaceHighThreshold = self.config.getfloat(MY_ID,'confirmArrivalPlaceHighThreshold')
        self.confirmTravelTimeHighThreshold = self.config.getfloat(MY_ID,'confirmTravelTimeHighThreshold')

    def Init(self,userFirst=False):
        from copy import deepcopy

        self.beliefState.Init()
        self.fieldCounts = dict([(field,0) for field in self.fields])
        self.fieldCounts['all'] = 0
        self.routeConfirmCount = 0
        sysAction = self._ChooseAction()
        self.prevSysAction = sysAction
        return deepcopy(sysAction)

    def TakeTurn(self,asrResult):
        from copy import deepcopy

        self.beliefState.Update(asrResult,self.prevSysAction)
        self.appLogger.info('** PartitionDistribution: **\n%s'%(self.beliefState))
        sysAction = self._ChooseAction(asrResult)
        self.prevSysAction = sysAction
        return deepcopy(sysAction)

    def _ChooseAction(self,asrResult=None):
        (travelSpec,belief) = self.beliefState.GetTopUniqueUserGoal()
        if (belief > self.acceptThreshold):
            destination = '%s' % (travelSpec)
            surface = self.prompts.BusSchedule(travelSpec)
            sysAction = SystemAction('inform',content=travelSpec,surface=surface,destination=destination)
            return sysAction
        else:
            marginals = self.beliefState.GetMarginals()
            for field in self.fields:
                if (len(marginals[field]) > 0):
                    self.appLogger.info('%s: %s(%f)'%(field,marginals[field][-1]['equals'],marginals[field][-1]['belief']))         
            askField = confirmField = None
            if (sum([len(marginals[elem]) for elem in marginals]) == 0):
                askField = 'all'
            if (askField == None):
                maxMarginals = []
                for field in self.fields:
                    if (len(marginals[field]) > 0):
                        maxMarginals.append(marginals[field][-1]['belief'])
                if (max(maxMarginals) < self.openQuestionThreshold):
                    askField = 'all'
            if (askField == None):
                if self.routeConfirmCount < 2 and len(marginals['route']) > 0 and\
                marginals['route'][-1]['belief'] > self.confirmRouteLowThreshold and\
                marginals['route'][-1]['belief'] < self.confirmRouteHighThreshold:
                    confirmField = 'route' 
                    self.routeConfirmCount += 1
            if (askField == None and confirmField == None and asrResult.userActions[0].type != 'non-understanding'):
#                print asrResult.userActions[0].content
                if len(marginals['departure_place']) > 0 and\
                'departure_place' in asrResult.userActions[0].content and marginals['departure_place'][-1]['belief'] < self.confirmDeparturePlaceHighThreshold:
                    confirmField = 'departure_place' 
                elif len(marginals['arrival_place']) > 0 and\
                'arrival_place' in asrResult.userActions[0].content and marginals['arrival_place'][-1]['belief'] < self.confirmArrivalPlaceHighThreshold:
                    confirmField = 'arrival_place' 
                elif len(marginals['travel_time']) > 0 and\
                'travel_time' in asrResult.userActions[0].content and marginals['travel_time'][-1]['belief'] < self.confirmTravelTimeHighThreshold:
                    confirmField = 'travel_time' 
            if (confirmField != None):
                surface = 'Is this right?' #self.prompts.YNQuestion(confirmField,self.fieldCounts[confirmField])
                sysAction = SystemAction('ask','confirm',{confirmField:marginals[confirmField][-1]['equals']},surface=surface,grammarName='')
                return sysAction
            
            if (askField == None):
                for field in self.fields:
                    if (len(marginals[field]) == 0 and field != 'route'):
                        askField = field
                        break
            if (askField == None):
                minBelief = 1.1
                for field in self.fields:
                    if (field != 'route' and marginals[field][-1]['belief'] < minBelief ):
                        askField = field
                        minBelief = marginals[field][-1]['belief']
            if (askField == None):
                # should never be here; case added as a check
                self.appLogger.warn('LOGIC ERROR')
                askField = self.fields[0]
            surface = self.prompts.WHQuestion(askField,self.fieldCounts[askField])
            self.fieldCounts[askField] += 1
            if (self.useAllGrammar):
                grammarName = 'all'
            else:
                grammarName = askField
            sysAction = SystemAction('ask','request',askField,surface=surface,grammarName=grammarName)
            return sysAction

class RigidDialogManager(DialogManager):
    '''
    See module header for a description.
    '''
    def __init__(self,iterations=1):
        DialogManager.__init__(self)
        self.prevSysAction = None
        self.useAllGrammar = self.config.getboolean(MY_ID,'useAllGrammar')
        self.iterations = iterations

    def Init(self):
        self.beliefState.Init()
        self.prevSysAction = None
        self.actionsToTake = []
        for i in range(self.iterations):
            for field in self.fields:
                surface = self.prompts.WHQuestion(field)
                if (self.useAllGrammar):
                    grammarName = 'all'
                else:
                    grammarName = field
                sysAction = SystemAction('ask','request',field,surface=surface,grammarName=grammarName)
                self.actionsToTake.append(sysAction)
        sysAction = self.actionsToTake.pop(0)
        self.prevSysAction = sysAction
        return sysAction

    def TakeTurn(self,asrResult):
        self.beliefState.Update(asrResult,self.prevSysAction)
        if (len(self.actionsToTake)==0):
            (travelSpec,belief) = self.beliefState.GetTopUniqueUserGoal()
            if (not travelSpec == None):
                destination = '%s' % (travelSpec)
                surface = self.prompts.BusSchedule(travelSpec)
                result = SystemAction('transfer',content=travelSpec,surface=surface,destination=destination)
            else:
                result = SystemAction('hangup',surface='Sorry, I didnt find anyone matching your request.')
        else:
            result = self.actionsToTake.pop(0)
        self.prevSysAction = result
        return result

class DirectedDialogManager(DialogManager):
    '''
    See module header for a description.
    '''
    def __init__(self,useLearnedUserModel=None):
        DialogManager.__init__(self,useLearnedUserModel)
        self.useAllGrammar = self.config.getboolean(MY_ID,'useAllGrammar')
        self.acceptThreshold = self.config.getfloat(MY_ID,'acceptThreshold')

    def Init(self):
        self.beliefState.Init()
        self.fieldCounts = dict([(field,0) for field in self.fields])
        sysAction = self._ChooseAction()
        self.prevSysAction = sysAction
        return sysAction

    def TakeTurn(self,asrResult):
        self.beliefState.Update(asrResult,self.prevSysAction)
        sysAction = self._ChooseAction()
        self.prevSysAction = sysAction
        return sysAction

    def _ChooseAction(self):
        (travelSpec,belief) = self.beliefState.GetTopUniqueUserGoal()
        if (belief > self.acceptThreshold):
            destination = '%s' % (travelSpec)
            surface = self.prompts.BusSchedule(travelSpec)
            sysAction = SystemAction('transfer',content=travelSpec,surface=surface,destination=destination)
        else:
            marginals = self.beliefState.GetMarginals()
            askField = None
            for field in self.fields:
                if (len(marginals[field]) == 0):
                    askField = field
                    break
            if (askField == None):
                minBelief = 1.1
                for field in self.fields:
                    if (marginals[field][-1]['belief'] < minBelief):
                        askField = field
                        minBelief = marginals[field][-1]['belief']
            if (askField == None):
                # should never be here; case added as a check
                self.appLogger.warn('LOGIC ERROR')
                askField = self.fields[0]
            surface = self.prompts.WHQuestion(askField,self.fieldCounts[askField])
            self.fieldCounts[askField] += 1
            if (self.useAllGrammar):
                grammarName = 'all'
            else:
                grammarName = askField
            sysAction = SystemAction('ask','request',askField,surface=surface,grammarName=grammarName)
        return sysAction

class LetsGoPrompts(object):
    '''
    Renders sysActions as TTS-playable prompts.  This is the only
    place (outside of the database) with references to the values of
    the fields ('first','last',etc.)
    '''
    def __init__(self):
        pass

    def WHQuestion(self,field,count=0):
        '''
        Ask for "field", e.g.,

          >>> ndp = NameDialerPrompts()
          >>> ndp.WHQuestion('first')
          What is the first name?
          >>> ndp.WHQuestion('city',1)
          Sorry, what is the city?

        '''
        if (count > 0):
            prefix = 'sorry, '
        else:
            prefix = ''
        if field == 'all':
            body = '%show may I help you?'%prefix
        elif field == 'departure_place':
            body = '%swhat is the departure place?'%prefix
        elif field == 'arrival_place':
            body = '%swhat is the arrival place?'%prefix
        elif field == 'route':
            body = '%swhich bus do you want?'%prefix
        else:
            body = '%swhen are you going to travel?'%prefix
        result = '%s%s' % (body[0].upper(),body[1:])
        return result

    def BusSchedule(self,travelSpec):
        '''
        Prompt to transfer the call to travelSpec (which is a dict)
        '''
        return 'Your bus information is here'# %s, %s, %s, %s' % (travelSpec['route'],travelSpec['departure_place'],travelSpec['arrival_place'],travelSpec['travel_time'])
