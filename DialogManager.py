'''
Two simple dialog managers.

This modules contains two simple dialog managers:

  RigidDialogManager: Asks for each field, one a time, regardless of
  input received so far.  This is useful for running simulations where
  it is necessary that all dialogs follow the same flow.

  DirectedDialogManager: This dialog manager asks for each field one
  at a time.  If it receives no evidence for a field, it stops and asks
  the field again.  As soon as there is sufficient belief in a single
  listing, it transfers the call.  If it asks for all of the slots and
  it has not obtained sufficient belief in a single listing, it proceeds
  by asking for the field with the lowest marginal belief.

  OpenDialogManager: This dialog manager starts by asking "Which listing?"
  If it has low belief in all the slots, it asks the same qustion again.
  If it has high belief in one field but low belief in others, it asks
  specifically for the low belief slots.

A dialog manager implements 2 methods:

  Init(): called to begin a new dialog.  Returns the first system
  action (the system always provides the first action).

  TakeTurn(asrResult): called after the user has taken a turn.  Returns
  the next system action.

For the demonstration, dialog managers also implement GetDisplayJSON(),
which returns JSON used to display dialog state on the demonstration
webpage.

This module requires that global logging, configuration, and database have been
initialized.  See main README file.

Configuration options:

  [DialogManager]
  useAllGrammar: if 'true', always uses the 'all' grammar which recognizes
  any field (and any combination of fields).  If 'false', then for field-specific
  questions (such as "First name?"), uses field-specific grammars, which only
  recognize elements of that field.  Used by all dialog managers.

  acceptThreshold: if belief in the top unique (i.e., count=1) partition is
  higher than this value, the call is transferred.  Otherwise, the system continues
  to ask questions.  Used by DirectedDialogManager and OpenDialogManager.

  openQuestionThreshold: if the maximum marginal belief in any field is below this
  value, the system asks the open question.  Otherwise, it asks slot-specific
  questions.  Only used by the OpenDialogManager.

Part of the AT&T Statistical Dialog Toolkit (ASDT).

Jason D. Williams
jdw@research.att.com
www.research.att.com/people/Williams_Jason_D
'''

import logging
from GlobalConfig import GetConfig
from BeliefState import BeliefState
from DB import GetDB
from DialogModules import SystemAction

MY_ID = 'DialogManager'

class DialogManager(object):
    '''
    Base class.  Not meant to be instantiated on its own.
    '''
    def __init__(self):
        self.appLogger = logging.getLogger('Results')
        self.config = GetConfig()
        self.beliefState = BeliefState()
        self.db = GetDB()
#        self.fields = self.db.GetFields()
        self.prompts = LetsGoPrompts()

    def Init(self):
        pass

    def TakeTurn(self,asrResult):
        pass

    def GetDisplayJSON(self):
        '''
        Returns JSON for displaying the current belief state in the
        web-based demo.
        '''
        result = {
          'joint' : [],
          'marginal': [],
        }
        totalBelief = 0.0
        for (i,partitionEntry) in enumerate(reversed(self.beliefState.partitionDistribution.partitionEntryList)):
            textArray = []
            for field in self.fields:
                if (partitionEntry.partition.fields[field].type == 'equals'):
                    textArray.append(partitionEntry.partition.fields[field].equals)
                else:
                    textArray.append('*')
            textArray.append('(%d)' % partitionEntry.partition.count)
            text = ' '.join(textArray)
            belief = partitionEntry.belief
            totalBelief += belief
            json = {'text': text, 'prob': belief,}
            result['joint'].append(json)
        marginals = self.beliefState.GetMarginals()
        for field in self.db.GetFields():
            if (len(marginals[field]) == 0):
                bestValue = '[empty]'
                bestBelief = 0.0
            else:
                bestValue = marginals[field][-1]['equals']
                bestBelief = marginals[field][-1]['belief']
            json = {'text': '%s: %s' % (field,bestValue), 'prob': bestBelief}
            result['marginal'].append(json)
        return result

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
    def __init__(self):
        DialogManager.__init__(self)
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

    def Init(self):
        self.beliefState.Init()
        self.fieldCounts = dict([(field,0) for field in self.fields])
        self.fieldCounts['all'] = 0
        self.routeConfirmCount = 0
        sysAction = self._ChooseAction()
        self.prevSysAction = sysAction
        return sysAction

    def TakeTurn(self,asrResult):
        self.beliefState.Update(asrResult,self.prevSysAction)
        sysAction = self._ChooseAction(asrResult)
        self.prevSysAction = sysAction
        return sysAction

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
                    print '%s: %s(%f)'%(field,marginals[field][-1]['equals'],marginals[field][-1]['belief'])            
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
                print asrResult.userActions[0].content
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

import numpy as np
from SparseBayes import SparseBayes
class SBSarsaDialogManager(DialogManager):
    '''
    See module header for a description.
    '''
    def __init__(self):
        DialogManager.__init__(self)
        self.fields = ['route','departure_place','arrival_place','travel_time']
        self.rewardDiscountFactor = self.config.getfloat(MY_ID,'rewardDiscountFactor')
        self.taskSuccessReward = self.config.getfloat(MY_ID,'taskSuccessReward')
        self.taskFailureReward = self.config.getfloat(MY_ID,'taskFailureReward')
        self.taskProceedReward = self.config.getfloat(MY_ID,'taskProceedReward')
        self.acceptThreshold = self.config.getfloat(MY_ID,'acceptThreshold')
        self.basisWidth = self.config.getfloat(MY_ID,'basisWidth')
        self.sb = SparseBayes()

    def Init(self,userGoal=None):
        self.userGoal = userGoal
        self.beliefState.Init()
        self.fieldCounts = dict([(field,0) for field in self.fields])
        self.fieldCounts['all'] = 0
        self.routeConfirmCount = 0
        sysAction,Qval = self._ChooseAction()
        self.prevSysAction = sysAction
        self.prevAsrResult = None
        self.dialogResult = False
        return sysAction
    
    def DialogResult(self):
        return self.dialogResult

    def TakeTurn(self,asrResult):
        from copy import deepcopy
#       prevBeliefState = deepcopy(self.beliefState)
        prevTopBelief = self.beliefState.GetTopUserGoalBelief()
        prevTopFields = deepcopy(self.beliefState.GetTopUserGoal())
        prevMarginals = deepcopy(self.beliefState.GetMarginals())
        reward = self._GetReward(self.beliefState,self.prevSysAction)
        self.beliefState.Update(asrResult,self.prevSysAction)
        sysAction,Qval = self._ChooseAction(asrResult)
        self._SBSarsa(prevTopBelief,prevTopFields,prevMarginals,self.prevSysAction,reward,Qval,self.prevAsrResult)
        self.prevSysAction = sysAction
        self.prevAsrResult = asrResult
        # terminal case
        if sysAction.type == 'inform':
            reward = self._GetReward(self.beliefState,sysAction)
            self._SBSarsa(self.beliefState.GetTopUserGoalBelief(),self.beliefState.GetTopUserGoal(),\
                          self.beliefState.GetMarginals(),sysAction,reward,0,asrResult)
            if reward == self.taskSuccessReward:
                self.dialogResult = True
        return sysAction

    def _GetReward(self,beliefState,sysAction):
        if sysAction.type == 'inform':
            field = beliefState.GetTopUserGoal()
            if self.userGoal['Bus number'] == '' and field['route'].type == 'equals':
                return self.taskFailureReward
            if self.userGoal['Bus number'] != '' and field['route'].type != 'equals':
                return self.taskFailureReward
            if self.userGoal['Bus number'] != '' and self.userGoal['Bus number'] != field['route'].equals:
                return self.taskFailureReward
            if self.userGoal['Departure place'] == '' and field['departure_place'].type == 'equals':
                return self.taskFailureReward
            if self.userGoal['Departure place'] != '' and field['departure_place'].type != 'equals':
                return self.taskFailureReward
            if self.userGoal['Departure place'] != '' and self.userGoal['Departure place'] != field['departure_place'].equals:
                return self.taskFailureReward
            if self.userGoal['Arrival place'] == '' and field['arrival_place'].type == 'equals':
                return self.taskFailureReward
            if self.userGoal['Arrival place'] != '' and field['arrival_place'].type != 'equals':
                return self.taskFailureReward
            if self.userGoal['Arrival place'] != '' and self.userGoal['Arrival place'] != field['arrival_place'].equals:
                return self.taskFailureReward
            if self.userGoal['Travel time'] == '' and field['travel_time'].type == 'equals':
                return self.taskFailureReward
            if self.userGoal['Travel time'] != '' and field['travel_time'].type != 'equals':
                return self.taskFailureReward
            if self.userGoal['Travel time'] != '' and self.userGoal['Travel time'] != field['travel_time'].equals:
                return self.taskFailureReward
            return self.taskSuccessReward
        else:
            return self.taskProceedReward

    def _polynomial_basis_vector(self,XN,x):
        BASIS = np.zeros((len(XN),1))
        for i, xi in enumerate(XN):
#            if xi[1] == x[1] and xi[2] == x[2]:
            if xi[2] == x[2]:
                BASIS[i] = (np.dot(xi[0],x[0]) + 0.1)**2
        return BASIS
    
    def _polynomial_basis_matrix(self,X,BASIS=None):
#        print X
#        BASIS = np.zeros((len(X),len(X)))
##        print BASIS
#        for i, x1 in enumerate(X):
##            print 'x1: %s'%str(x1)
#            for j, x2 in enumerate(X):
##                print 'x2: %s'%str(x2)
##                if x1[1] == x2[1] and x1[2] == x2[2]:
#                if x1[2] == x2[2]:
#                    BASIS[j,i] = (np.dot(x1[0],x2[0]) + 0.1)**2
#        print 'BASIS %s'%str(BASIS)

        basis = np.zeros((len(X),1)) + np.atleast_2d(np.random.standard_normal(len(X))/1e10).T
        for i, xi in enumerate(X):
#            if xi[1] == X[-1][1] and xi[2] == X[-1][2]:
            if xi[2] == X[-1][2]:
                basis[i,0] += (np.dot(xi[0],X[-1][0]) + 0.1)**2
#        print basis
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

    def _gaussian_basis_vector(self,XN,x):
        BASIS = np.zeros((len(XN),1))
        for i, xi in enumerate(XN):
            ua_kernel = 0.5 if xi[1] != x[1] else 1.0
#            ua_kernel = 1.0
            if xi[2] == x[2]:
                BASIS[i] = np.exp(-(np.sum(xi[0]**2) + np.sum(x[0]**2) - 2*np.dot(xi[0],x[0]))/(self.basisWidth**2)) * ua_kernel
        return BASIS
        
    def _gaussian_basis_matrix(self,X,BASIS=None):
        basis = np.zeros((len(X),1)) + np.atleast_2d(np.random.standard_normal(len(X))/1e10).T
        for i, xi in enumerate(X):
            ua_kernel = 0.5 if xi[1] != X[-1][1] else 1.0
#            ua_kernel = 1.0
            if xi[2] == X[-1][2]:
                basis[i,0] += np.exp(-(np.sum(xi[0]**2) + np.sum(X[-1][0]**2) - 2*np.dot(xi[0],X[-1][0]))/(self.basisWidth**2)) * ua_kernel
#        print basis
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
        
    def _SBSarsa(self,topBelief,topFields,marginals,sysAction,reward,nextQval,asrResult):
        self.appLogger.info('reward %d'%reward)
        self.appLogger.info('nextQval %f'%nextQval)
        y = reward + nextQval * self.rewardDiscountFactor + np.random.standard_normal(1)[0]/1e10
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
            self.sb.incremental_learn([X],np.atleast_2d(y),self._gaussian_basis_matrix)
            self.appLogger.info('Number of data points: %d'%self.sb.get_basis_size())
#            self._TraceQval()
        except RuntimeError,(XN,Y,raw_BASIS):
            self.appLogger.info('BASIS:\n %s'%str(raw_BASIS))
#            print 'BASIS:\n %s'%str(BASIS)
            self.sb = SparseBayes()
            self.Relevant,self.Mu,Alpha,beta,update_count,add_count,delete_count,full_count = \
            self.sb.incremental_learn(XN,Y,self._gaussian_basis_matrix,raw_BASIS)
            
    def StoreModel(self):
        import pickle
        pickle.dump(self.Relevant,open('Relevant.model','w'))
        pickle.dump(self.Mu,open('Mu.model','w'))
        pickle.dump(self.sb.get_basis_points(),open('DataPoints.model','w'))        
        
    def _TraceQval(self):
        import operator
        
        acts = ['[ask] request all','[ask] request route','[ask] request departure_place',\
                '[ask] request arrival_place','[ask] request travel_time',\
                '[ask] confirm route','[ask] confirm departure_place',\
                '[ask] confirm arrival_place','[ask] confirm travel_time',\
                '[inform]']
        
        w_infer = np.zeros((self.sb.get_basis_size(),1))
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
                Qvals.append((act,np.dot(self._gaussian_basis_vector(self.sb.get_basis_points(),X).T,w_infer)[0,0]))
            Qvals = sorted(Qvals,key=lambda q:q[1],reverse=True)
            for Qval in Qvals:
                self.appLogger.info('%s:%f'%(Qval[0],Qval[1]))
                
    def _ChooseAction(self,asrResult=None):
        import random
        
        # action list
        acts = ['[ask] request all','[ask] request route','[ask] request departure_place',\
                '[ask] request arrival_place','[ask] request travel_time',\
                '[ask] confirm route','[ask] confirm departure_place',\
                '[ask] confirm arrival_place','[ask] confirm travel_time',\
                '[inform]']

        if self.beliefState.GetTopUniqueMandatoryUserGoal() == 0.0:
            acts = acts[:-1]
            self.appLogger.info('Exclude inform because of low top belief %f'%self.beliefState.GetTopUniqueMandatoryUserGoal())
        
        act = ''        
        if asrResult == None or self.sb.get_basis_size() == 0:
            act = random.choice(acts[:5])
        elif random.random() < 0.1:
            act = random.choice(acts)
            self.appLogger.info('Exploration act: %s'%act)
#        elif self.beliefState.GetTopUniqueMandatoryUserGoal() > self.acceptThreshold:
#            act = acts[-1]
#            self.appLogger.info('Choose inform because of high top belief %f'%self.beliefState.GetTopUniqueMandatoryUserGoal())
        
        contX = [self.beliefState.GetTopUserGoalBelief()]
        marginals = self.beliefState.GetMarginals()
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
            w_infer = np.zeros((self.sb.get_basis_size(),1))
            w_infer[self.Relevant] = self.Mu 
            if act == '':
                ys = np.array([])
                for act in acts:
                    X = [np.array(contX),str(asrResult.userActions[0]).split('=')[0],act]
#                    print 'choose X:%s'%str(X)
    #                print ys
    #                print np.dot(self._basis_vector(self.sb.get_basis_points(),X).T,w_infer).flatten()
                    ys = np.concatenate((ys,np.dot(self._gaussian_basis_vector(self.sb.get_basis_points(),X).T,w_infer).ravel()))
                    
                self.appLogger.info('Qvals: %s'%str(ys))
                act = acts[ys.argmax(0)]
                Qval = ys.max(0)
            else:
                X = [np.array(contX),str(asrResult.userActions[0]).split('=')[0],act]
                Qval = np.dot(self._gaussian_basis_vector(self.sb.get_basis_points(),X).T,w_infer)[0,0]
        except:
            Qval = 0.0
            
        self.appLogger.info('Act %s, Qval: %f'%(act,Qval))
        
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
        return sysAction,Qval

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
