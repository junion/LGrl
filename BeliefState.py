'''
Classes that implement the belief state for name dialer dialog systems.

This modules contains the classes that implement the belief state ("Partition" and
"History" classes).  In addition, the BeliefState class provides a convenience
wrapper around the PartitionDistribution engine.

This module requires that global logging, configuration, and database have been
initialized.  See main README file.

Configuration options:

  [BeliefState]
  useHistory: if 'true', tracks dialog history in each partition.  If 'false',
  does not track any history information.

  [UserModel]
  request_silenceProb: when asked a 'request' question, probability that the user
  is silent

  request_directAnswerProb: when asked a 'request' question, probability that the user
  provides a direct answer (i.e., just the field that was asked for).

  request_allOverCompleteProb: when asked a 'request' question, probability that the
  user provides the field asked for PLUS one or more additional fields.

  request_oogProb: when asked a 'request' question, probability that the user
  says something out of grammar.

  confirm_directAnswerProb: when asked a 'confirm' question, probability that the user
  just says "yes" or "no" (as appropriate)

  confirm_silenceProb: when asked a 'confirm' question, probability that the user is
  silent

  confirm_oogProb: when asked a 'confirm' question, probability that the user says
  something out of grammar.

Part of the AT&T Statistical Dialog Toolkit (ASDT).

Jason D. Williams
jdw@research.att.com
www.research.att.com/people/Williams_Jason_D
'''

import os
from copy import deepcopy
import logging
import pickle
from GlobalConfig import GetConfig
from PartitionDistribution import PartitionDistribution
from DB import GetDB
from Utils import Combination

MY_ID = 'BeliefState'

class Partition(object):
    '''
    Tracks a partition of listings.

    This class tracks a partition of listings.
    '''
    def __init__(self,existingPartition=None,fieldToSplit=None,value=None):
        '''
        Constructor, and copy constructor.

        If called as Partition(), returns a new root partition.

        If called as Partition(existingPartition,fieldToSplit,value), this creates
        a new child partition of existingPartition, split on fieldToSplit=value.  Does
        not modify existingPartition.

        This constructor is not meant to be called directly by application code.
        Application code should use the BeliefState wrapper.
        '''
        self.appLogger = logging.getLogger('Learning')
#        self.appLogger.info('Partition init')
        self.config = GetConfig()
        self.useLearnedUserModel = self.config.getboolean(MY_ID,'useLearnedUserModel')
        self.confirmUnlikelyDiscountFactor = self.config.getfloat(MY_ID,'confirmUnlikelyDiscountFactor')
        self.ignoreNonunderstandingFactor = self.config.getboolean(MY_ID,'ignoreNonunderstandingFactor')
        self.num_route = self.config.getint(MY_ID,'numberOfRoute')
        self.num_place = self.config.getint(MY_ID,'numberOfPlace')
        self.num_time = self.config.getint(MY_ID,'numberOfTime')
        
        db = GetDB()
#        self.appLogger.info('Partition 1')
        if (existingPartition == None):
            #self.fieldList = db.GetFields()
            self.fieldList = ['route','departure_place','arrival_place','travel_time']
            self.fieldCount = len(self.fieldList)
            #self.totalCount = db.GetListingCount({})
            self.totalCount = self.num_route * self.num_place * self.num_place * self.num_time
            self.fields = {}
#            self.appLogger.info('Partition 2')
            for field in self.fieldList:
                self.fields[field] = _FieldEntry()
            self.count = self.totalCount
            self.prior = 1.0
#            self.appLogger.info('Partition 3')
            if not self.useLearnedUserModel:
                umFields = ['request_nonUnderstandingProb',
                            'request_directAnswerProb',
                            'request_allOverCompleteProb',
                            'request_oogProb',
                            'request_irrelevantAnswerProb',
                            'confirm_directAnswerProb',
                            'confirm_nonUnderstandingProb',
                            'confirm_oogProb']
                assert (not self.config == None), 'Config file required (UserModel parameters)'
                self.umParams = {}
                for key in umFields:
                    assert (self.config.has_option('UserModel', key)),'UserModel section missing field %s' % (key)
                    self.umParams[key] = self.config.getfloat('UserModel',key)
                overCompleteActionCount = 0
                for i in range(1,self.fieldCount):
                    overCompleteActionCount += Combination(self.fieldCount-1,i)
                self.appLogger.info('fieldCount = %d; overCompleteActionCount = %d' % (self.fieldCount,overCompleteActionCount))
                self.umParams['request_overCompleteProb'] = \
                  1.0 * self.umParams['request_allOverCompleteProb'] / overCompleteActionCount
                self.umParams['open_answerProb'] = \
                  (1.0 - self.umParams['request_nonUnderstandingProb'] - self.umParams['request_oogProb']) / \
                  overCompleteActionCount
            else:
                modelPath = self.config.get('Global','modelPath')
#                self.appLogger.info('Partition 4')
                self.userModelPath = self.config.get(MY_ID,'userModelPath')
#                self.appLogger.info('Partition 5')
                self.userModel = pickle.load(open(os.path.join(modelPath,self.userModelPath),'rb'))
#                self.appLogger.info('Partition 6')
                self.irrelevantUserActProb = self.config.getfloat(MY_ID,'irrelevantUserActProb')
                self.minRelevantUserActProb = self.config.getfloat(MY_ID,'minRelevantUserActProb')
#                self.appLogger.info('Partition 7')
        else:
            assert not fieldToSplit == None,'arg not defined'
            assert not value == None,'arg not defined'
            self.fieldList = existingPartition.fieldList
            self.fieldCount = existingPartition.fieldCount
            if not self.useLearnedUserModel:
                self.umParams = existingPartition.umParams
            else:
                self.userModel = existingPartition.userModel
                self.irrelevantUserActProb = existingPartition.irrelevantUserActProb
                self.minRelevantUserActProb = existingPartition.minRelevantUserActProb
            self.totalCount = existingPartition.totalCount
            self.fields = {}
            self.count = 1
            for field in self.fieldList:
                if (field == fieldToSplit):
                    self.fields[field] = _FieldEntry(type='equals', equals=value)
                else:
                    self.fields[field] = existingPartition.fields[field].Copy()
                    
                if self.fields[field].type == 'equals':
                    self.count *= 1
                elif field == 'route':
                    self.count *= (self.num_route - len(self.fields[field].excludes.keys()))
                elif field in ['departure_place','arrival_place']:
                    self.count *= (self.num_place - len(self.fields[field].excludes.keys()))
                elif field == 'travel_time':
                    self.count *= (self.num_time - len(self.fields[field].excludes.keys()))
                else:
                    raise RuntimeError,'Invalid field %s'%field

            #self.count = db.GetListingCount(self.fields)
            self.prior = 1.0 * self.count / self.totalCount

    def Split(self,userAction):
        '''
        Attempts to split the partition on userAction.  Returns a list of zero
        or more child partitions, modifying this partition as appropriate.
        '''
        newPartitions = []
        if (userAction.type == 'non-understanding'):
                # silent doesn't split
            pass
        else:
            for field in userAction.content.keys():
                if (field == 'confirm'):
                    continue
                val = userAction.content[field]
                if (self.fields[field].type == 'equals'):
                    # Cant split this partition -- field already equals something
                    pass
                elif (val in self.fields[field].excludes):
                    # Cant split this partition -- field exludes this value already
                    pass
                else:
                    newPartition = Partition(existingPartition=self,fieldToSplit=field,value=val)
                    if (newPartition.count > 0):
                        self.fields[field].excludes[val] = True
                        self.count -= newPartition.count
                        self.prior = 1.0 * self.count / self.totalCount
                        newPartitions.append(newPartition)
        return newPartitions

    # This will only be called on a child with no children
    def Recombine(self,child):
        '''
        Attempts to recombine child partition with this (parent) partition.  If
        possible, does the recombination and returns True.  If not possible,
        makes no changes and returns False.
        '''
        fieldsToRecombine = []
        for field in self.fields:
            if (self.fields[field].type == 'excludes'):
                if (child.fields[field].type == 'equals'):
                # parent excludes, child equals
                    value = child.fields[field].equals
                    if (value in self.fields[field].excludes):
                        fieldsToRecombine.append((field,value))
                    else:
                        raise RuntimeError, 'Error: field %s: child equals %s but parent doesnt exclude it' % (field,value)
                else:
                    # parent excludes, child excludes
                    # ensure they exclude the same things
                    if (not len(self.fields[field].excludes) == len(child.fields[field].excludes)):
                        return False
                    for val in self.fields[field].excludes:
                        if (val not in child.fields[field].excludes):
                            return False
                    pass
            else:
                if (child.fields[field].type == 'equals'):
                    # parent equals, child equals (must be equal)
                    pass
                else:
                    raise RuntimeError,'Error: field %s: parent equals %s but child excludes this field' % (field,value)
        if (len(fieldsToRecombine) == 0):
            raise RuntimeError,'Error: parent and child are identical'
        if (len(fieldsToRecombine) > 1):
            raise RuntimeError,'Error: parent and child differ by more than 1 field: %s' % (fieldsToRecombine)
        self.count += child.count
        self.prior = 1.0 * self.count / self.totalCount
        del self.fields[fieldsToRecombine[0][0]].excludes[ fieldsToRecombine[0][1] ]
        return True

    def __str__(self):
        '''
        Renders this partition as a string.  Example:

          city x();state x();last x(WILLIAMS);first=JASON;count=386

        This is the partition of 386 listings which have first name
        JASON, and do NOT have last name WILLIAMS (located in any city
        and any state).
        '''
        s = ''
        if (len(self.fields) > 0):
            elems = []
            for conceptName in self.fieldList:
                if (self.fields[conceptName].type == 'equals') :
                    elems.append('%s=%s' % (conceptName,self.fields[conceptName].equals))
                elif (len(self.fields[conceptName].excludes) <= 2):
                    elems.append('%s x(%s)' % (conceptName,','.join(self.fields[conceptName].excludes.keys())))
                else:
                    elems.append('%s x([%d entries])' % (conceptName,len(self.fields[conceptName].excludes)))
            elems.append('count=%d' % (self.count))
            s = ';'.join(elems)
        else:
            s = "(all)"
        return s

    def _getClosestUserAct(self,userAction):
        if userAction.type == 'non-understanding':
            return 'non-understanding'
      
        acts = [['I:ap','I:bn','I:dp','I:tt'],\
                      ['I:ap','I:bn','I:dp'],\
                      ['I:ap','I:dp','I:tt'],\
                      ['I:bn','I:dp','I:tt'],\
                      ['I:ap','I:dp'],\
                      ['I:bn','I:tt'],\
                      ['I:bn'],\
                      ['I:dp'],\
                      ['I:ap'],\
                      ['I:tt'],\
                      ['yes'],\
                      ['no']]
        ua = []
        for field in userAction.content:
            if field == 'confirm':
                ua.append('yes' if userAction.content[field] == 'YES' else 'no')
            elif field == 'route':
                ua.append('I:bn')
            elif field == 'departure_place':
                ua.append('I:dp')
            elif field == 'arrival_place':
                ua.append('I:ap')
            elif field == 'travel_time':
                ua.append('I:tt')
        
        score = [float(len(set(act).intersection(set(ua))))/len(set(act).union(set(ua))) for act in acts] 
        closestUserAct = ','.join(acts[score.index(max(score))])
#        self.appLogger.info('Closest user action %s'%closestUserAct) 
        return closestUserAct

    def UserActionLikelihood(self, userAction, history, sysAction):
        '''
        Returns the probability of the user taking userAction given dialog
        history, sysAction, and that their goal is within this partition.
        '''
#        if (sysAction.type == 'ask'):
#            if (sysAction.force == 'request'):
#                if (userAction.type == 'non-understanding'):
#                    result = self.umParams['request_nonUnderstandingProb']
#                else:
#                    targetFieldIncludedFlag = False
#                    overCompleteFlag = False
#                    allFieldsMatchGoalFlag = True
#                    askedField = sysAction.content
#                    for field in userAction.content:
#                        if field == 'confirm':
#                            allFieldsMatchGoalFlag = False
#                            continue
#                        val = userAction.content[field]
#                        if (self.fields[field].type == 'equals' and self.fields[field].equals == val):
#                            if (field == askedField):
#                                targetFieldIncludedFlag = True
#                            else:
#                                overCompleteFlag = True
#                        else:
#                            allFieldsMatchGoalFlag = False
#                    if (not allFieldsMatchGoalFlag):
#                        # This action doesn't agree with this partition
#                        result = 0.0
#                    elif (askedField == 'all'):
#                        # A response to the open question
#                        result = self.umParams['open_answerProb']
#                    elif (not targetFieldIncludedFlag):
#                        # This action doesn't include the information that was asked for
#                        # This user model doesn't ever do this
#                        result = 0.0
#                    elif (overCompleteFlag):
#                        # This action include extra information - this happens
#                        # request_overCompleteProb amount of the time
#                        result = self.umParams['request_overCompleteProb']
#                    else:
#                        # This action just answers the question that was asked
#                        result = self.umParams['request_directAnswerProb']
#            elif (sysAction.force == 'confirm'):
#                if (userAction.type == 'non-understanding'):
#                    result = self.umParams['confirm_nonUnderstandingProb']
#                else:
#                    allFieldsMatchGoalFlag = True
#                    for field in sysAction.content:
#                        val = sysAction.content[field]
#                        if (self.fields[field].type == 'excludes' or not self.fields[field].equals == val):
#                            allFieldsMatchGoalFlag = False
#                    if (allFieldsMatchGoalFlag):
#                        if (userAction.content['confirm'] == 'YES'):
#                            result = self.umParams['confirm_directAnswerProb']
#                        else:
#                            result = 0.0
#                    else:
#                        if (userAction.content['confirm'] == 'NO'):
#                            result = self.umParams['confirm_directAnswerProb']
#                        else:
#                            result = 0.0
#            else:
#                raise RuntimeError, 'Dont know sysAction.force = %s' % (sysAction.force)
        if not self.useLearnedUserModel:
            result = 0.0
            if (sysAction.type == 'ask'):
                if (userAction.type == 'non-understanding'):
                    if (sysAction.force == 'confirm'):
                        result = self.umParams['confirm_nonUnderstandingProb']
                    else: 
                        result = self.umParams['request_nonUnderstandingProb']
                else:
                    targetFieldIncludedFlag = False
                    overCompleteFlag = False
                    allFieldsMatchGoalFlag = True
                    askedField = sysAction.content
                    for field in userAction.content:
                        if field == 'confirm':
                            if sysAction.force == 'request':
                                allFieldsMatchGoalFlag = False
                                continue
                            for field in sysAction.content:
                                val = sysAction.content[field]
                                if (self.fields[field].type == 'excludes' or not self.fields[field].equals == val):
                                    allFieldsMatchGoalFlag = False
                            if (allFieldsMatchGoalFlag):
                                if (userAction.content['confirm'] == 'YES'):
                                    result = self.umParams['confirm_directAnswerProb']
                                    targetFieldIncludedFlag = True
                                else:
                                    result = self.umParams['request_irrelevantAnswerProb']
                            else:
                                if (userAction.content['confirm'] == 'NO'):
                                    result = self.umParams['confirm_directAnswerProb']
                                    targetFieldIncludedFlag = True
                                else:
                                    result = self.umParams['request_irrelevantAnswerProb']
                        else:
                            val = userAction.content[field]
                            if (self.fields[field].type == 'equals' and self.fields[field].equals == val):
                                if (field == askedField):
                                    targetFieldIncludedFlag = True
                                else:
                                    overCompleteFlag = True
                            else:
                                allFieldsMatchGoalFlag = False
                    if (not allFieldsMatchGoalFlag):
                        # This action doesn't agree with this partition
                        result = self.umParams['request_irrelevantAnswerProb']
                    elif (askedField == 'all'):
                        # A response to the open question
                        result = self.umParams['open_answerProb']
                    elif (not targetFieldIncludedFlag):
                        # This action doesn't include the information that was asked for
                        # This user model doesn't ever do this
                        result = self.umParams['request_irrelevantAnswerProb']
                    elif (overCompleteFlag):
                        # This action include extra information - this happens
                        # request_overCompleteProb amount of the time
                        result = self.umParams['request_overCompleteProb']
                    else:
                        # This action just answers the question that was asked
                        result = result if result > 0 else self.umParams['request_directAnswerProb']
            else:
                raise RuntimeError, 'Dont know sysAction.type = %s' % (sysAction.type)
        else:
            self.appLogger.info('Apply learned user model')
            if sysAction.type != 'ask':
                raise RuntimeError, 'Cannot handle sysAction %s'%str(sysAction)
            result = self.irrelevantUserActProb
            allFieldsMatchGoalFlag = True
            directAnswer = False
            if sysAction.force == 'confirm':
                askedField = sysAction.content.keys()[0]
                if userAction.type != 'non-understanding':
                    for ua_field in userAction.content:
                        self.appLogger.info('User action field: %s:%s'%(ua_field,userAction.content[ua_field]))
                        if ua_field == 'confirm' and userAction.content[ua_field] == 'YES':
                            val = sysAction.content[askedField]
                            if self.fields[askedField].type == 'excludes' or not self.fields[askedField].equals == val:
                                self.appLogger.info('Mismatched YES')
                                allFieldsMatchGoalFlag = False
                        elif ua_field == 'confirm' and userAction.content[ua_field] == 'NO':
                            val = sysAction.content[askedField]
                            if (self.fields[askedField].type == 'equals' and self.fields[askedField].equals == val) or\
                            (self.fields[askedField].type == 'excludes' and val not in self.fields[askedField].excludes):
                                self.appLogger.info('Mismatched NO')
                                allFieldsMatchGoalFlag = False
                        elif askedField == ua_field:
                            directAnswer = True
#                            val = sysAction.content[askedField]
#                            if self.fields[askedField].type != 'excludes' and \
#                            self.fields[askedField].equals == userAction.content[askedField]:
#                                self.appLogger.info('Matched %s'%userAction.content[askedField])
#                                allFieldsMatchGoalFlag = True
                            if self.fields[askedField].type == 'excludes' or \
                            self.fields[askedField].equals != userAction.content[askedField]:
                                self.appLogger.info('Mismatched %s'%userAction.content[askedField])
                                allFieldsMatchGoalFlag = False
                        else:
                            val = userAction.content[ua_field]
                            if self.fields[ua_field].type == 'excludes' or not self.fields[ua_field].equals == val:
                                self.appLogger.info('Mismatched %s for irrelevant field to confirmation'%userAction.content[ua_field])
                                allFieldsMatchGoalFlag = False
                elif self.ignoreNonunderstandingFactor:
                    allFieldsMatchGoalFlag = False
                if allFieldsMatchGoalFlag:
                    self.appLogger.info('All fields matched')
                    if (userAction.content != None and 'confirm' in userAction.content and userAction.content['confirm'] == 'YES') or\
                    directAnswer:
                        result = self.userModel['C-o'][self._getClosestUserAct(userAction)]
                    else:
                        if 'confirm' in userAction.content and directAnswer:
                            del userAction.content['confirm']
                        result = self.userModel['C-x'][self._getClosestUserAct(userAction)]
                    self.appLogger.info('User action likelihood %g'%result)
                    result = self.minRelevantUserActProb if result < self.minRelevantUserActProb else result
                    self.appLogger.info('Set minimum user action likelihood %g'%result)
            elif sysAction.force == 'request':
                askedField = sysAction.content
                if userAction.type != 'non-understanding':
                    for ua_field in userAction.content:
                        if ua_field != 'confirm':
                            val = userAction.content[ua_field]
                            if self.fields[ua_field].type == 'excludes' or not self.fields[ua_field].equals == val:
                                allFieldsMatchGoalFlag = False
                elif self.ignoreNonunderstandingFactor:
                    allFieldsMatchGoalFlag = False
                if allFieldsMatchGoalFlag:
                    if askedField == 'route':
#                        print self.userModel['R-bn']
                        result = self.userModel['R-bn'][self._getClosestUserAct(userAction)]
                    elif askedField == 'departure_place':
#                        print self.userModel['R-dp']
                        result = self.userModel['R-dp'][self._getClosestUserAct(userAction)]
                    elif askedField == 'arrival_place':
#                        print self.userModel['R-ap']
                        result = self.userModel['R-ap'][self._getClosestUserAct(userAction)]
                    elif askedField == 'travel_time':
#                        print self.userModel['R-tt']
                        result = self.userModel['R-tt'][self._getClosestUserAct(userAction)]
                    elif askedField == 'all':
#                        print self.userModel['R-open']
                        result = self.userModel['R-open'][self._getClosestUserAct(userAction)]
                    result = self.minRelevantUserActProb if result < self.minRelevantUserActProb else result
        return result
    
    def UserActionUnlikelihood(self, userAction, history, sysAction):
        '''
        Returns the probability of the user not taking userAction given dialog
        history, sysAction, and that their goal is within this partition.
        '''
        if sysAction.type != 'ask':
            raise RuntimeError, 'Dont know sysAction.type = %s' % (sysAction.type)

        self.appLogger.info('Apply confirmUnlikelyDiscountFactor %f'%self.confirmUnlikelyDiscountFactor)
        if sysAction.force == 'request':
            result = self.prior
            reason = 'request'
        elif sysAction.force == 'confirm':
            result = self.confirmUnlikelyDiscountFactor * self.prior
            reason = 'confirm'
        self.appLogger.info('UserActionUnlikelihood by (%s): %g'%(reason,result))
        return result

class History(object):
    '''
    Implements a simple dialog history, which tracks the number of times
    each field has been said by the user.
    '''
    def __init__(self):
        '''
        Constructor - returns a new history.
        '''
        self.prior = 1.0
        self.db = GetDB()
        #self.fields = self.db.GetFields()
        self.fields = ['route','departure_place','arrival_place','travel_time']
        self.counts = {}
        for field in self.fields:
            self.counts[field] = 0

    def __eq__(self,otherHistory):
        '''
        Tests if two histories are equal to each other.
        '''
        for field in self.fields:
            if (not self.counts[field] == otherHistory.counts[field]):
                return False
        return True

    def Update(self,partition,userAction,sysAction):
        '''
        Updates this dialog history given the user's goal is in partition,
        that they have taken userAction, and the system has taken
        sysAction.
        '''
        if (userAction == None):
            pass
        elif (userAction.type == 'ig'):
            for field in userAction.content:
                if (field in self.fields):
                    self.counts[field] += 1
        return

    def Copy(self):
        '''
        Copies this dialog history, returning a new History object.
        '''
        newHistory = History()
        for field in self.fields:
            newHistory.counts[field] = self.counts[field]
        return newHistory

    def __str__(self):
        '''
        Renders this dialog history as a string.  Example:

          first: 2, last: 1, city: 0, state: 0

        The first name field has been said 2 times, the last name
        one time, and city and state zero times.
        '''
        result = ', '.join(['%s:%d' % (field,self.counts[field]) for field in self.fields])
        return result

class _FieldEntry(object):
    '''
    Helper class for Partitions.
    '''
    __slots__ = ['type','equals','excludes','count']
    def __init__(self,type='excludes',equals=None):
        self.type = type
        if (type == 'equals'):
            self.equals = equals
        else:
            self.excludes = {}

    def Copy(self):
        return deepcopy(self)

    def __str__(self):
        if (self.type == 'equals'):
            result = '=%s' % (self.equals)
        elif (len(self.excludes) < 2):
            result = 'x(%s)' % (','.join(self.excludes.keys()))
        else:
            result = 'x([%d entries])' % (len(self.excludes))
        return result


class BeliefState(object):
    '''
    Belief state over listings.

    This class wraps PartitionDistribution, using the name dialing classes
    Partition and History in this module.

    Typical usage:

      from BeliefState import BeliefState
      beliefState = BeliefState()

      # Call at the beginning of each dialog
      beliefState.Init()

      # system takes action sysAction, gets asrResult
      # Update belief state to account for this information
      beliefState.Update(asrResult,sysAction)

      # print out the belief state
      print '%s' % (beliefState)

    '''
    def __init__(self):
        '''
        Creates a new partitionDistribution object, using the classes in this
        module.
        '''
        self.config = GetConfig()
        self.appLogger = logging.getLogger('Learning')
        self.db = GetDB()
            
        #self.fields = self.db.GetFields()
        self.fields = ['route','departure_place','arrival_place','travel_time']
        def PartitionSeed():
            return [ Partition() ]
        def HistorySeed(partition):
            return [ History() ]
        if (self.config.getboolean(MY_ID,'useHistory')):
            self.partitionDistribution = PartitionDistribution(PartitionSeed,HistorySeed)
        else:
            self.partitionDistribution = PartitionDistribution(PartitionSeed,None)

    def Init(self):
        '''
        Calls partitionDistribution.Init() method.  Call this at the beginning of
        each dialog.
        '''
        self.partitionDistribution.Init()
        self.marginals = None

    def Update(self,asrResult,sysAction):
        '''
        Calls partitionDistribution.Update(asrResult,sysAction).  Call this after each
        asrResult is received.
        '''
        self.partitionDistribution.Update(asrResult,sysAction)
        self.marginals = None

    def GetTopUserGoalBelief(self):
        return self.partitionDistribution.partitionEntryList[-1].belief

    def GetTopUserGoal(self):
        return self.partitionDistribution.partitionEntryList[-1].partition.fields

    def GetTopUniqueMandatoryUserGoal(self):
        partitionEntry = self.partitionDistribution.partitionEntryList[-1]
        if (partitionEntry.partition.fields['departure_place'].type == 'equals' and \
            partitionEntry.partition.fields['arrival_place'].type == 'equals' and \
            partitionEntry.partition.fields['travel_time'].type == 'equals'):
            return partitionEntry.belief
        else:
            return 0.0


    def GetTopUniqueUserGoal(self):
        '''
        Returns (callee,belief) for the top unique user goal (i.e., goal with
        count == 1), or (None,None) if one doesnt exist.
        '''
        spec = None
        belief = None
        for partitionEntry in reversed(self.partitionDistribution.partitionEntryList):
#            if (partitionEntry.partition.count == 1):
                #dbReturn = self.db.GetListingsByQuery(partitionEntry.partition.fields)
            if (partitionEntry.partition.fields['departure_place'].type == 'equals' and \
                partitionEntry.partition.fields['arrival_place'].type == 'equals' and \
                partitionEntry.partition.fields['travel_time'].type == 'equals'):
                spec = {'departure_place':partitionEntry.partition.fields['departure_place'].equals,\
                        'arrival_place':partitionEntry.partition.fields['arrival_place'].equals,\
                        'travel_time':partitionEntry.partition.fields['travel_time'].equals,\
                        'route':partitionEntry.partition.fields['route'].equals \
                        if partitionEntry.partition.fields['route'].type == 'equals'\
                        else ''}
                belief = partitionEntry.belief
                break
        return (spec,belief)

    def GetTopFullyInstantiatedUserGoal(self):
        '''
        Returns (callee,belief) for the top user goal for which all fields are
        instantiated (i.e., equals to something, rather than excluding something)
        or (None,None) if none exists.
        '''
        callee = {}
        for partitionEntry in reversed(self.partitionDistribution.partitionEntryList):
            allEquals = True # tentative
            for field in partitionEntry.partition.fields:
                if (not partitionEntry.partition.fields[field].type == 'equals'):
                    allEquals = False
                    break
                callee[field] = partitionEntry.partition.fields[field].equals
            if (allEquals == True):
                return (callee,partitionEntry.belief)
        return (None,None)

    def GetMarginals(self):
        '''
        Returns a dict with marginals over each field; example:

        {
          'first' : [
            { 'equals' : 'JASON', 'belief': 0.6 },
            { 'equals' : 'JOHN', 'belief': 0.3 }
          ],
          'last' : [
            { 'equals' : 'WILLIAMS', 'belief': 0.9 }
          ],
          'city' : [],
          'state' : []
        }

        '''
        if (self.marginals == None):
            # Not computed yet; compute them now
            self.marginals = {}
            for field in self.fields:
                self.marginals[field] = []
            for field in self.fields:
                marginalTotals = {}
                for partitionEntry in self.partitionDistribution.partitionEntryList:
                    if (partitionEntry.partition.fields[field].type == 'equals'):
                        val = partitionEntry.partition.fields[field].equals
                        if (val not in marginalTotals):
                            marginalTotals[val] = partitionEntry.belief
                        else:
                            marginalTotals[val] += partitionEntry.belief
                for val in marginalTotals:
                    self.marginals[field].append({'equals': val, 'belief': marginalTotals[val]})
                self.marginals[field].sort(lambda x, y: cmp(x['belief'], y['belief']))
        return deepcopy(self.marginals)

    def __str__(self):
        '''
        Returns self.partitionDistribution.__str__()

        Example:

        ( id,pid) belief  logBel  [logPri ] description
        (   ,  -) 0.00009  -9.295 [ -0.004] city x();state x();last x();first x(JASON);count=99613
                  0.00009  -9.295           -
        (  1,  0) 0.99991  -0.000 [ -5.555] city x();state x();last x();first=JASON;count=387
                  0.99991  -0.000           -
        '''
        return self.partitionDistribution.__str__()
