'''

'''

import copy
from math import log,log10,trunc
#import resource
import logging
from GlobalConfig import GetConfig

MY_ID = 'PartitionDistribution'

class PartitionDistribution(object):
    '''
    Implements a distribution over partitions of dialog states.

    Each partition corresponds to one partition of user goals,
    and a set of dialog histories.

    Set configuration using the GlobalConfig module, provided
    with this distribution.

    Configuration parameters:

      [PartitionDistribution]
      defaultResetFraction: the default likelihood that the user's
      goal will revert to the prior.  This can be made system-action-
      specific by setting systemAction.resetFraction.  Default value
      is 0.0.

      maxNBest: maximum number of NBest entries to consider (additional
      entries on the NBest list, if present, are ignored).  0 means
      consider all NBest entries.  Default value is 0.

      maxPartitions: maximum number of partitions to maintain.  After
      each NBest entry is incorporated, partitions are repeatedly
      recombined until there are at most maxPartitions.  0 means not
      to attempt any recombination - allow number of partitions to grow
      without bound. Default value is 0.

      maxHistories: maximum number of histories to maintain for each
      partition.  At the end of each update, low probability histories
      are deleted until there are at most maxHistories histories for
      each partition.  0 means not to do any deleting - allow number of
      histories to grow without bound. Default value is 0.
    '''

    def __init__(self,partitionSeed,historySeed=None):
        '''
        Creates a new partitionDIstribution object.

        - partitionSeed: a function, which when called as
          partitionSeed(), returns a list of root partitions.
        - historySeed: a function, which when called as
          historySeed(partition), returns a list of starter
          dialog histories.  If None, then no dialog history
          will be tracked.

        After creation, partitionDistributionObject.Init() method
        is called.
        '''
        self.appLogger = logging.getLogger('Learning')
        self.maxNBest = 0
        self.maxPartitions = 0
        self.defaultResetFraction = 0.0
        self.maxHistories = 0
        self.useAggregateUserActionLikelihoods = False
        self.offListBeliefUpdateMethod = 'unlikelihood'
        config = GetConfig()
        if (not config == None):
            if (config.has_option(MY_ID, 'defaultResetFraction')):
                self.defaultResetFraction = config.getfloat(MY_ID,'defaultResetFraction')
            if (config.has_option(MY_ID, 'maxNBest')):
                self.maxNBest = config.getint(MY_ID,'maxNBest')
            if (config.has_option(MY_ID, 'maxPartitions')):
                self.maxPartitions = config.getint(MY_ID,'maxPartitions')
            if (config.has_option(MY_ID, 'maxHistories')):
                self.maxHistories = config.getint(MY_ID,'maxHistories')
            if (config.has_option(MY_ID, 'useAggregateUserActionLikelihoods')):
                self.useAggregateUserActionLikelihoods = config.getboolean(MY_ID,'useAggregateUserActionLikelihoods')
            if (config.has_option(MY_ID, 'offListBeliefUpdateMethod')):
                self.offListBeliefUpdateMethod = config.get(MY_ID,'offListBeliefUpdateMethod')
            self.num_route = config.getint('BeliefState','numberOfRoute')
            self.num_place = config.getint('BeliefState','numberOfPlace')
            self.num_time = config.getint('BeliefState','numberOfTime')
            self.totalCount = self.num_route * self.num_place * self.num_place * self.num_time
            self.numberOfPossibleActionsForConfirmation = config.getint('BeliefState','numberOfPossibleActionsForConfirmation')
            self.conservativeUpdateFactor = config.getfloat(MY_ID,'conservativeUpdateFactor')
            self.minPartitionProbability = config.getfloat(MY_ID,'minPartitionProbability')
            self.compactByPruningFieldValuePair = config.getboolean(MY_ID,'compactByPruningFieldValuePair')
            self.resetFractionApplyThreshold = config.getfloat(MY_ID,'resetFractionApplyThreshold')
            self.applyResetFractionPerField = config.getboolean(MY_ID,'applyResetFractionPerField')

        self.appLogger.info('Config: defaultResetFraction = %f' % (self.defaultResetFraction))
        self.appLogger.info('Config: maxNBest = %d' % (self.maxNBest))
        self.appLogger.info('Config: maxPartitions = %d' % (self.maxPartitions))
        self.appLogger.info('Config: maxHistories = %d' % (self.maxHistories))
        self.appLogger.info('Config: useAggregateUserActionLikelihoods = %s' % (self.useAggregateUserActionLikelihoods))
        self.partitionSeed = partitionSeed
        if (historySeed == None):
            self.historySeed = _DefaultHistory.Seed
        else:
            self.historySeed = historySeed
        self.stats = _Stats()
        self.Init()

    def Init(self):
        '''
        Initializes a partitionDistributionObject, for example
        at the beginning of a dialog.

        Calls partitionSeed() to obtain a list of root partitions,
        and for each calls historySeed(partition) to obtain a list
        of starter dialog histories.
        '''
#        self.appLogger.info('!')
        self.partitionEntryList = []
#        self.appLogger.info('!!')
        self.nextPartitionEntryID = [0]  # use a list so that _PartitionEntry can modify this
#        self.appLogger.info('!!!')
        for partition in self.partitionSeed():
#            self.appLogger.info('1')
            partitionEntry = _PartitionEntry( partition=partition, belief=partition.prior, parent=None, nextPartitionEntryID=self.nextPartitionEntryID )
#            self.appLogger.info('2')
            for history in self.historySeed(partition):
#                self.appLogger.info('3')
                historyEntry = _HistoryEntry()
#                self.appLogger.info('4')
                historyEntry.history = history
                historyEntry.belief = history.prior
                historyEntry.origBelief = historyEntry.belief
                historyEntry.userActionLikelihoodTotal = 0.0
                historyEntry.belief = history.prior
#                self.appLogger.info('5')
                partitionEntry.historyEntryList.append(historyEntry)
#                self.appLogger.info('6')
            self.partitionEntryList.append(partitionEntry)
#            self.appLogger.info('7')

    def _OffListUserActionASRLikelihood(self,offListASRProb,userAction):
        if userAction.type == 'non-understanding':
            return offListASRProb
        count = 1
        confirmExist = False
        for field in userAction.content:
            if field == 'confirm':
                confirmExist = True
            elif field == 'route':
                count *= self.num_route
            elif field == 'departure_place':
                count *= self.num_place
            elif field == 'arrival_place':
                if not ('departure_place' in userAction.content and \
                userAction.content['departure_place'] == userAction.content['arrival_place']):
                    count *= self.num_place
            elif field == 'travel_time':
                count *= self.num_time
            else:
                raise RuntimeError,'Invalid field %s'%field
        if confirmExist and count == 1:
            count *= self.numberOfPossibleActionsForConfirmation
        return offListASRProb/count
    
    def _MinUserActionLikelihood(self,userAction):
        if userAction.type == 'non-understanding':
            return 0.0
        count = 1
        confirmExist = False
        for field in userAction.content:
            if field == 'confirm':
                confirmExist = True
            elif field == 'route':
                count *= self.num_route
            elif field == 'departure_place':
                count *= self.num_place
            elif field == 'arrival_place':
                if not ('departure_place' in userAction.content and \
                userAction.content['departure_place'] == userAction.content['arrival_place']):
                    count *= self.num_place
            elif field == 'travel_time':
                count *= self.num_time
            else:
                raise RuntimeError,'Invalid field %s'%field
        if confirmExist and count == 1:
            count *= self.numberOfPossibleActionsForConfirmation
        return 1.0/count
        
    def Update(self,asrResult,sysAction):
        '''
        Updates a partitionDistributionObject object with
        a system action and the resulting asrResult.
        '''
        #
        # Init
        #
        
        if asrResult.userActions[0].type == 'non-understanding':
            return

        self._CompactByProbability(self.minPartitionProbability)
        if self.compactByPruningFieldValuePair:
            self._CompactByMaxPartitions(self.maxPartitions)
        
#        self.stats.InitUpdate()

#        self.stats.StartClock('mainUpdate')
        rawOnlistBeliefTotal = 0.0
        rawOfflistBeliefTotal = 0.0

        # Account for "resetFraction" -- the likelihood of the user's goal
        # reverting to the original prior distribution
        try:
            resetFraction = sysAction.resetFraction
        except:
            resetFraction = self.defaultResetFraction
        if (resetFraction > 0.0):
            for field in self.partitionEntryList[0].partition.fields:
                marginalTotal = 0.0
                for partitionEntry in self.partitionEntryList:
                    if (partitionEntry.partition.fields[field].type == 'equals'):
                        marginalTotal += partitionEntry.belief
                if marginalTotal > self.resetFractionApplyThreshold:
                    self.appLogger.info("Applying resetFraction of %f for high marginal of %s"%(resetFraction,field))
                    self.appLogger.info('** PartitionDistribution: **\n%s'%self)
                    if not self.applyResetFractionPerField:
                        for partitionEntry in self.partitionEntryList:
                            for historyEntry in partitionEntry.historyEntryList:
                                if (historyEntry.belief > 0.0):
                                    historyFraction = historyEntry.belief / partitionEntry.belief
                                    historyEntry.belief = historyEntry.belief - resetFraction*(historyEntry.belief - historyFraction * partitionEntry.partition.prior)
                                    historyEntry.origBelief = historyEntry.belief
                            partitionEntry.belief = partitionEntry.belief - resetFraction*(partitionEntry.belief - partitionEntry.partition.prior)
                    else:
                        partitionGroup = {}
                        for partitionEntry in self.partitionEntryList:
#                            groupKey = trunc(log10(partitionEntry.partition.prior/partitionEntry.partition.priorOfField[field]))
                            groupKey = ''
                            for otherField in partitionEntry.partition.fields:
                                if otherField != field:
                                    groupKey += otherField
                                    groupKey += '='
                                    if partitionEntry.partition.fields[otherField].type == 'equals':
                                        groupKey += partitionEntry.partition.fields[otherField].equals
                                    elif partitionEntry.partition.fields[otherField].type == 'excludes':
                                        groupKey += 'x('
                                        groupKey += ','.join(partitionEntry.partition.fields[otherField].excludes)
                                        groupKey += ')'
                                    groupKey += ' '
                            self.appLogger.info("Partition %d assigned to group %s"%(partitionEntry.id,groupKey))
                            if groupKey in partitionGroup:
                                partitionGroup[groupKey].append(partitionEntry)
                            else:
                                partitionGroup[groupKey] = [partitionEntry]
                        for groupKey in partitionGroup:
                            groupTotal = 0.0
                            for partitionEntry in partitionGroup[groupKey]:
                                groupTotal += partitionEntry.belief
                            self.appLogger.info("Group (%s) total belief %f"%(groupKey,groupTotal))
                            for partitionEntry in partitionGroup[groupKey]:
                                self.appLogger.info("Apply reset fraction to partition %d in group %s"%(partitionEntry.id,groupKey))
                                for historyEntry in partitionEntry.historyEntryList:
                                    if (historyEntry.belief > 0.0):
                                        historyFraction = historyEntry.belief / partitionEntry.belief
                                        historyEntry.belief = historyEntry.belief - resetFraction*(historyEntry.belief - historyFraction * partitionEntry.partition.priorOfField[field] * groupTotal)
                                        historyEntry.origBelief = historyEntry.belief
                                partitionEntry.belief = partitionEntry.belief - resetFraction*(partitionEntry.belief - partitionEntry.partition.priorOfField[field] * groupTotal)
                    self.appLogger.info('** PartitionDistribution: **\n%s'%self)
                    break
                
        # Initialize update
        # Add initial estimate of off-list probs
        self.appLogger.info('Start of update:')
        for (i,partitionEntry) in enumerate(self.partitionEntryList):
            partitionEntry.newBelief = 0.0
            for (j,historyEntry) in enumerate(partitionEntry.historyEntryList):
                partitionEntry.newBelief += historyEntry.belief
            rawOfflistBeliefTotal += partitionEntry.newBelief

        #
        # Main loop
        #

        # Iterate over items on the NBest list
        partitionCount = len(self.partitionEntryList)
        for (n,(userAction,asrLikelihood,asrUnseenActionLikelihood)) in enumerate(asrResult):
            self.appLogger.info('working on userAction=%s (n=%d,asrProb=%f)' % (userAction,n,asrLikelihood))
            if (self.maxNBest > 0 and n >= self.maxNBest):
                break
            rawOfflistBeliefTotal = 0.0
            i = 0
            # 1. Grow tree through splitting
            while (i < partitionCount):
                self.appLogger.info(' Trying to split partition %s ...' % (self.partitionEntryList[i].partition))

                # 1A. Do splitting (belief refinement)
                existingPartitionEntry=self.partitionEntryList[i]
                self.stats.StartClock('split')
                newPartitions = existingPartitionEntry.partition.Split(userAction)
                self.stats.EndClock('split')
                if (len(newPartitions)>0):
                    newBeliefFractionTotal = 0.0
                    self.appLogger.info('  Split!  Parent (id %d) is now: %s' % (existingPartitionEntry.id,existingPartitionEntry.partition))
                    for newPartition in newPartitions:
                        self.stats.lastUpdateSplits += 1
                        partitionCount += 1
                        newPartitionEntry = _PartitionEntry(partition=newPartition, belief=None, parent=existingPartitionEntry, nextPartitionEntryID=self.nextPartitionEntryID )
                        self.appLogger.info('   Created child id %d: %s' % (newPartitionEntry.id,newPartition))
                        existingPartitionEntry.children.append(newPartitionEntry)
                        if (newPartition.prior== 0.0 and existingPartitionEntry.partition.prior == 0.0):
                            # The child has been split from a parent with zero belief
                            newBeliefFraction = 0.0
                        else:
                            newBeliefFraction = newPartition.prior / (newPartition.prior + existingPartitionEntry.partition.prior)
                            if (newBeliefFraction > 1.0):
                                s =  'newBeliefFraction > 1.0\n'
                                s += ' newBeliefFraction = %e\n' % (newBeliefFraction)
                                s += ' newPartition.prior = %e\n' % (newPartition.prior)
                                s += ' existingPartitionEntry.partition.prior = %e\n' % (existingPartitionEntry.partition.prior)
                                raise RuntimeError,s
                        newPartitionEntry.newBelief = existingPartitionEntry.newBelief * newBeliefFraction
                        self.appLogger.info('   newPartitionEntry.newBelief=%g'%newPartitionEntry.newBelief)
                        newBeliefFractionTotal += newBeliefFraction
                        for existingHistoryEntry in existingPartitionEntry.historyEntryList:
                            refinedExistingHistoryEntry = _HistoryEntry()
                            refinedExistingHistoryEntry.history = existingHistoryEntry.history.Copy()
                            refinedExistingHistoryEntry.belief = existingHistoryEntry.belief * newBeliefFraction
                            refinedExistingHistoryEntry.origBelief = existingHistoryEntry.origBelief * newBeliefFraction
                            refinedExistingHistoryEntry.userActionLikelihoodTotal = existingHistoryEntry.userActionLikelihoodTotal
                            refinedExistingHistoryEntry.history = existingHistoryEntry.history.Copy()
                            refinedExistingHistoryEntry.userActionLikelihoodTypes = existingHistoryEntry.userActionLikelihoodTypes.copy()
                            newPartitionEntry.historyEntryList.append(refinedExistingHistoryEntry)
                            self.appLogger.info('    refinedExistingHistoryEntry.belief=%g'%refinedExistingHistoryEntry.belief)
                        for newHistoryEntry in existingPartitionEntry.newHistoryEntryList:
                            refinedNewHistoryEntry = _HistoryEntry()
                            refinedNewHistoryEntry.history = newHistoryEntry.history.Copy()
                            refinedNewHistoryEntry.belief = newHistoryEntry.belief * newBeliefFraction
                            refinedNewHistoryEntry.origBelief = None
                            refinedNewHistoryEntry.userActionLikelihoodTotal = None
                            refinedNewHistoryEntry.userActionLikelihoodTypes = None
                            newPartitionEntry.newHistoryEntryList.append(refinedNewHistoryEntry)
                            self.appLogger.info('    refinedNewHistoryEntry.belief=%g'%refinedNewHistoryEntry.belief)
                        self.partitionEntryList.append(newPartitionEntry)
                    existingPartitionEntry.newBelief = existingPartitionEntry.newBelief * (1-newBeliefFractionTotal)
                    self.appLogger.info('  existingPartitionEntry.newBelief=%g'%existingPartitionEntry.newBelief)
                    for existingHistoryEntry in existingPartitionEntry.historyEntryList:
                        existingHistoryEntry.belief *= (1-newBeliefFractionTotal)
                        existingHistoryEntry.origBelief *= (1-newBeliefFractionTotal)
                        self.appLogger.info('   existingHistoryEntry.belief=%g'%existingHistoryEntry.belief)
                    for newHistoryEntry in existingPartitionEntry.newHistoryEntryList:
                        newHistoryEntry.belief = newHistoryEntry.belief * (1-newBeliefFractionTotal)
                        self.appLogger.info('   newHistoryEntry.belief=%g'%newHistoryEntry.belief)
                else:
                    self.appLogger.info('  Could not split this partition.')
                # 1B. Compute raw likelihoods and update offList mass
                self.appLogger.info(' Computing user action likelihoods for partition %s ...' % (self.partitionEntryList[i].partition))
                for existingHistoryEntry in existingPartitionEntry.historyEntryList:
                    if (self.useAggregateUserActionLikelihoods):
                        (userActionLikelihood,userActionLikelihoodType) = existingPartitionEntry.partition.UserActionLikelihood(userAction,existingHistoryEntry.history,sysAction)
                        self.appLogger.info('  History = %s; userActionLikelihood=%g; usereActionLikelihoodType=%s' % (existingHistoryEntry.history,userActionLikelihood,userActionLikelihoodType))
                    else:
                        userActionLikelihood = existingPartitionEntry.partition.UserActionLikelihood(userAction,existingHistoryEntry.history,sysAction)
                        self.appLogger.info('  History = %s; userActionLikelihood=%g' % (existingHistoryEntry.history,userActionLikelihood))
                    if (userActionLikelihood > 0.0):
                        # Update newHistoryEntry
                        nextNewHistoryEntry = _HistoryEntry()
                        nextNewHistoryEntry.history = existingHistoryEntry.history.Copy()
                        if self.offListBeliefUpdateMethod == 'heuristicPossibleActions':
                            minUserActionLikelihood = self._MinUserActionLikelihood(userAction)
                            userActionLikelihood = max(userActionLikelihood,minUserActionLikelihood)
                            nextNewHistoryEntry.belief = userActionLikelihood * asrLikelihood * existingHistoryEntry.origBelief
                        else:
                            nextNewHistoryEntry.belief = userActionLikelihood * asrLikelihood * existingHistoryEntry.origBelief
                        nextNewHistoryEntry.origBelief = None
                        nextNewHistoryEntry.userActionLikelihoodTotal = None
                        nextNewHistoryEntry.history.Update(existingPartitionEntry.partition,userAction,sysAction)
                        existingPartitionEntry.newHistoryEntryList.append(nextNewHistoryEntry)
                        self.appLogger.info('   New history = %s'%nextNewHistoryEntry.history)
                        self.appLogger.info('    userActionLikelihood=%g'%userActionLikelihood)
                        self.appLogger.info('    asrLikelihood=%g'%asrLikelihood)
                        self.appLogger.info('    existingHistoryEntry.origBelief=%g'%existingHistoryEntry.origBelief)
                        self.appLogger.info('    ->nextNewHistoryEntry.belief=%g'%nextNewHistoryEntry.belief)
                        # Update existingHistoryEntry
                        if (self.useAggregateUserActionLikelihoods):
                            if (userActionLikelihoodType not in existingHistoryEntry.userActionLikelihoodTypes):
                                # first time we've seen this type
                                existingHistoryEntry.userActionLikelihoodTypes[userActionLikelihoodType] = userActionLikelihood
                                newUserActionLikelihoodTotal = existingHistoryEntry.userActionLikelihoodTotal + userActionLikelihood
                            else:
                                # seen type before - check it's the same but dont add it to total
                                if (not existingHistoryEntry.userActionLikelihoodTypes[userActionLikelihoodType] == userActionLikelihood):
                                    s = 'Partition id = %d\n' % (existingPartitionEntry.id)
                                    s += 'Partition = %s\n' % (existingPartitionEntry.partition.__str__())
                                    s += 'History = %s\n' % (existingHistoryEntry.history.__str__())
                                    s += 'UserActionLikelihoodTotal for this history in this partition = %e\n' % (existingHistoryEntry.userActionLikelihoodTotal)
                                    s += 'UserAction = %s\n' % (userAction.__str__())
                                    s += 'UserActionLikelihood = %e\n' % (userActionLikelihood)
                                    s += 'UserActionLikelihoodType = %s\n' % (userActionLikelihoodType)
                                    s += 'Before this UserActionLikelihoodType had value %e but now its different\n' % (existingHistoryEntry.userActionLikelihoodTypes[userActionLikelihoodType])
                                    raise RuntimeError,s
                                else:
                                    newUserActionLikelihoodTotal = existingHistoryEntry.userActionLikelihoodTotal
                        else:
                            newUserActionLikelihoodTotal = existingHistoryEntry.userActionLikelihoodTotal + userActionLikelihood
                        if (newUserActionLikelihoodTotal  > 1.0):
                            s =  'Partition id = %d\n' % (existingPartitionEntry.id)
                            s += 'Partition = %s\n' % (existingPartitionEntry.partition.__str__())
                            s += 'History = %s\n' % (existingHistoryEntry.history.__str__())
                            s += 'UserActionLikelihoodTotal for this history in this partition = %e\n' % (existingHistoryEntry.userActionLikelihoodTotal)
                            s += 'UserAction = %s\n' % (userAction.__str__())
                            s += 'UserActionLikelihood = %e\n' % (userActionLikelihood)
                            s += 'If I add this UserActionLikelihood to UserActionLikelihoodTotal for this history\n in this partition, it will exceed 1.0, which it cant\n'
                            raise RuntimeError,s
                        existingHistoryEntry.userActionLikelihoodTotal = newUserActionLikelihoodTotal
                        existingPartitionEntry.newBelief = existingPartitionEntry.newBelief + nextNewHistoryEntry.belief
                        rawOnlistBeliefTotal += nextNewHistoryEntry.belief
                    else:
                        pass
                    offListUserActionLikelihood = 1.0 - existingHistoryEntry.userActionLikelihoodTotal
                    # Re-compute the amount of mass for all offlist actions
                    oldOffListHistoryEntryBelief = existingHistoryEntry.belief
                    if self.offListBeliefUpdateMethod == 'plain':
                        offListUserActionASRLikelihood = asrUnseenActionLikelihood
                        existingHistoryEntry.belief = existingHistoryEntry.origBelief * offListUserActionLikelihood * offListUserActionASRLikelihood
                    elif self.offListBeliefUpdateMethod == 'heuristicUsingPrior':
                        offListUserActionASRLikelihood = asrUnseenActionLikelihood
                        discountedOffListUserActionLikelihood = offListUserActionLikelihood * existingPartitionEntry.partition.UserActionUnlikelihood(userAction,existingHistoryEntry.history,sysAction)
                        existingHistoryEntry.belief = existingHistoryEntry.origBelief * offListUserActionASRLikelihood * discountedOffListUserActionLikelihood
                    elif self.offListBeliefUpdateMethod == 'heuristicPossibleActions':
                        offListUserActionASRLikelihood = self._OffListUserActionASRLikelihood(asrUnseenActionLikelihood,userAction)
                        existingHistoryEntry.belief = existingHistoryEntry.origBelief * offListUserActionLikelihood * offListUserActionASRLikelihood #* self.conservativeUpdateFactor #* existingPartitionEntry.partition.prior
                    else:
                        raise RuntimeError,'Unknown offListBeliefUpdateMethod = %s'%self.offListBeliefUpdateMethod
                    self.appLogger.info('   offListUserActionLikelihood=%g'%offListUserActionLikelihood)
                    self.appLogger.info('   offListUserActionASRLikelihood=%g'%offListUserActionASRLikelihood)
                    self.appLogger.info('   existingHistoryEntry.origBelief=%g'%existingHistoryEntry.origBelief)
                    self.appLogger.info('   ->existingHistoryEntry.belief=%g'%existingHistoryEntry.belief)
                    existingPartitionEntry.newBelief = existingPartitionEntry.newBelief - oldOffListHistoryEntryBelief + existingHistoryEntry.belief
                    rawOfflistBeliefTotal += existingHistoryEntry.belief
#                    self.appLogger.info('  oldHistoryEntryBelief = %g -> newHistoryEntryBelief = %g'%(oldOffListHistoryEntryBelief,existingHistoryEntry.belief))
                self.appLogger.info(' Raw (unnormalized) log-belief in this partition is now %s' % (_LogToStringSafely(existingPartitionEntry.newBelief)))
                i += 1

            # 2. Compact tree by pruning
            if not self.compactByPruningFieldValuePair:
                if (partitionCount > self.stats.lastUpdateMaxPartitions):
                    self.stats.lastUpdateMaxPartitions = partitionCount
                if (self.maxPartitions > 0 and partitionCount > self.maxPartitions):
                    leafPartitionEntryList = []
                    i = 0
                    for partitionEntry in self.partitionEntryList:
                        partitionEntry.selfPointer = i
                        if (len(partitionEntry.children) == 0 and partitionEntry.parent != None):
                            leafPartitionEntryList.append(partitionEntry)
                        i += 1
                    leafPartitionCount = len(leafPartitionEntryList)
                    leafPartitionEntryList.sort(PartitionDistribution._ComparePartitionEntriesNewBelief)
                    while (partitionCount > self.maxPartitions):
                        for i in range(leafPartitionCount):
                            partitionEntry = leafPartitionEntryList[i]
                            # print '  Looking at partition %d...' % (partitionEntry.id)
                            if (partitionEntry.parent.partition.Recombine(partitionEntry.partition)):
                                self.appLogger.info('Combining child (id %d) into its parent (id %d)' % (partitionEntry.id,partitionEntry.parent.id))
                                self.appLogger.info('Parent (%d) is now: %s' % (partitionEntry.parent.id,partitionEntry.parent.partition))
                                parent = partitionEntry.parent
                                # merge histories
                                parent.historyEntryList.extend(partitionEntry.historyEntryList)
                                PartitionDistribution._CombineHistoryDuplicatesOffList(parent.historyEntryList)
                                parent.newHistoryEntryList.extend(partitionEntry.newHistoryEntryList)
                                PartitionDistribution._CombineHistoryDuplicatesOnList(parent.newHistoryEntryList)
                                # merge belief
                                parent.newBelief = parent.newBelief + partitionEntry.newBelief
                                # delete pointer to child
                                del parent.children[ parent.children.index(partitionEntry) ]
                                self.partitionEntryList[ partitionEntry.selfPointer ] = None
                                del leafPartitionEntryList[i]
                                partitionCount -= 1
                                leafPartitionCount -= 1
                                # test if parent is now a leaf
                                if (len(parent.children) == 0 and parent.parent != None):
                                    # find the right place to insert the parent
                                    insertedFlag = 0
                                    for j in range(leafPartitionCount):
                                        if (parent.newBelief < leafPartitionEntryList[j].newBelief):
                                            leafPartitionEntryList.insert(j,parent)
                                            insertedFlag = 1
                                            break
                                    if (insertedFlag == 0):
                                        leafPartitionEntryList.append(parent)
                                    leafPartitionCount += 1
                                break
                    # Clean up empty entries
                    cleanPartitionEntryList = []
                    for partitionEntry in self.partitionEntryList:
                        if (partitionEntry != None):
                            cleanPartitionEntryList.append(partitionEntry)
                    self.partitionEntryList = cleanPartitionEntryList
                
        rawBeliefTotal = rawOfflistBeliefTotal + rawOnlistBeliefTotal

        # 3. Normalize, clean up and sort
        if (rawBeliefTotal == 0.0):
            self.stats.EndClock('mainUpdate')
            return
        rawOfflistBeliefTotalCheck = 0.0
        rawOnlistBeliefTotalCheck = 0.0
        i = 0
        for partitionEntry in self.partitionEntryList:
            for newHistoryEntry in partitionEntry.newHistoryEntryList:
                rawOnlistBeliefTotalCheck += newHistoryEntry.belief
            for historyEntry in partitionEntry.historyEntryList:
                historyEntry.history.Update(partitionEntry.partition,None,sysAction)
                partitionEntry.newHistoryEntryList.append(historyEntry)
                rawOfflistBeliefTotalCheck += historyEntry.belief
            partitionEntry.historyEntryList = partitionEntry.newHistoryEntryList
            partitionEntry.newHistoryEntryList = []
            PartitionDistribution._CombineHistoryDuplicatesOnList(partitionEntry.historyEntryList)
            partitionEntry.belief = 0.0
            partitionEntry.newBelief = 0.0
            for historyEntry in partitionEntry.historyEntryList:
                historyEntry.belief = historyEntry.belief / rawBeliefTotal
                historyEntry.origBelief = historyEntry.belief
                historyEntry.userActionLikelihoodTotal = 0.0
                historyEntry.userActionLikelihoodTypes = {}
                if (historyEntry.belief < 0.0):
                    s =  'historyEntry.belief < 0: %e\n' % (historyEntry.belief)
                    s += ' rawBeliefTotal = %e' % (rawBeliefTotal)
                    raise RuntimeError,s
                partitionEntry.belief += historyEntry.belief
            partitionEntry.historyEntryList.sort(PartitionDistribution._CompareHistoryEntries)
            if (self.maxHistories > 0 and len(partitionEntry.historyEntryList) > self.maxHistories):
                deletedMass = 0.0
                while (len(partitionEntry.historyEntryList) > self.maxHistories):
                    deletedMass += partitionEntry.historyEntryList[0].belief
                    del partitionEntry.historyEntryList[0]
                increaseFactor = 1.0 / (1.0 - deletedMass)
                for historyEntry in partitionEntry.historyEntryList:
                    historyEntry.belief *= increaseFactor
                    historyEntry.origBelief = historyEntry.belief
            i += 1
        self.partitionEntryList.sort(PartitionDistribution._ComparePartitionEntries)
        
#        self._CompactByProbability(self.minPartitionProbability)
#        if self.compactByPruningFieldValuePair:
#            self._CompactByMaxPartitions(self.maxPartitions)
        
#        self.stats.EndClock('mainUpdate')

    
    def _CompactByFieldValue(self,field,value):
        self.appLogger.info('** PartitionDistribution: **\n%s'%self)
        self.appLogger.info('Try to compact %s=%s'%(field,value))
        for partitionEntry in self.partitionEntryList:
            if partitionEntry.parent == None:
                rootEntry = partitionEntry
                break
        rootEntry.Prune(field,value)
        cleanPartitionEntryList = []
        for partitionEntry in self.partitionEntryList:
            if not (partitionEntry != rootEntry and partitionEntry.parent == None):
                cleanPartitionEntryList.append(partitionEntry)
        self.partitionEntryList = cleanPartitionEntryList
        for partitionEntry in self.partitionEntryList:
            count = 1
            fields = partitionEntry.partition.fields
            for field in fields:
                if fields[field].type == 'excludes':
                    if field == 'route':
                        num_field = self.num_route
                    elif field in ['departure_place','arrival_place']:
                        num_field = self.num_place
                    elif field == 'travel_time':
                        num_field = self.num_time
                    else:
                        raise RuntimeError,'Invalid field %s'%field
                    count *= (num_field - len(fields[field].excludes))
            partitionEntry.partition.count = count
            partitionEntry.partition.prior = 1.0 * count/partitionEntry.partition.totalCount
        self.partitionEntryList.sort(PartitionDistribution._ComparePartitionEntries)
        self.appLogger.info('** PartitionDistribution: **\n%s'%self)
        

    def _CompactByMaxPartitions(self,maxPartitions):
        '''
        Compacts a partitionDistribution object down
        to at most maxPartitions.

        This function does not need to be called as
        a part of the normal operation of the class.
        '''
        self.appLogger.info('Compacts a partitionDistribution down based on maximum count of partitions')
        if not self.compactByPruningFieldValuePair:
            self.stats.InitUpdate()
            self.stats.StartClock('compact')
            assert maxPartitions > 0,'maxPartitions must be > 0'
            partitionCount = len(self.partitionEntryList)
            self.stats.lastUpdateMaxPartitions = partitionCount
            if (maxPartitions > 0 and partitionCount > maxPartitions):
                leafPartitionEntryList = []
                i = 0
                for partitionEntry in self.partitionEntryList:
                    partitionEntry.selfPointer = i
                    if (len(partitionEntry.children) == 0 and partitionEntry.parent != None):
                        leafPartitionEntryList.append(partitionEntry)
                    i += 1
                leafPartitionCount = len(leafPartitionEntryList)
                leafPartitionEntryList.sort(PartitionDistribution._ComparePartitionEntries)
                while (partitionCount > maxPartitions):
                    for i in range(leafPartitionCount):
                        partitionEntry = leafPartitionEntryList[i]
                        if (partitionEntry.parent.partition.Recombine(partitionEntry.partition)):
                            self.appLogger.info('Combining child (id %d) into its parent (id %d)' % (partitionEntry.id,partitionEntry.parent.id))
                            self.appLogger.info('Parent (%d) is now: %s' % (partitionEntry.parent.id,partitionEntry.parent.partition))
                            parent = partitionEntry.parent
                            # merge histories
                            parent.historyEntryList.extend(partitionEntry.historyEntryList)
                            PartitionDistribution._CombineHistoryDuplicatesOnList(parent.historyEntryList)
                            # merge belief
                            parent.belief = parent.belief + partitionEntry.belief
                            # delete pointer to child
                            del parent.children[ parent.children.index(partitionEntry) ]
                            self.partitionEntryList[ partitionEntry.selfPointer ] = None
                            del leafPartitionEntryList[i]
                            partitionCount -= 1
                            leafPartitionCount -= 1
                            # test if parent is now a leaf
                            if (len(parent.children) == 0 and parent.parent != None):
                                # find the right place to insert the parent
                                insertedFlag = 0
                                for j in range(leafPartitionCount):
                                    if (parent.belief < leafPartitionEntryList[j].belief):
                                        leafPartitionEntryList.insert(j,parent)
                                        insertedFlag = 1
                                        break
                                if (insertedFlag == 0):
                                    leafPartitionEntryList.append(parent)
                                leafPartitionCount += 1
                            break
                # Clean up empty entries
                cleanPartitionEntryList = []
                for partitionEntry in self.partitionEntryList:
                    if (partitionEntry != None):
                        cleanPartitionEntryList.append(partitionEntry)
                self.partitionEntryList = cleanPartitionEntryList
                for partitionEntry in self.partitionEntryList:
                    partitionEntry.historyEntryList.sort(PartitionDistribution._CompareHistoryEntries)
                self.partitionEntryList.sort(PartitionDistribution._ComparePartitionEntries)
            self.stats.EndClock('compact')
        else:
            rootEntry = None
            for partitionEntry in self.partitionEntryList:
                if partitionEntry.parent == None:
                    rootEntry = partitionEntry
                    break
            while len(self.partitionEntryList) > self.maxPartitions:
                marginals = {}
                for field in rootEntry.partition.fields:
                    marginals[field] = []
                for field in rootEntry.partition.fields:
                    marginalTotals = {}
                    for partitionEntry in self.partitionEntryList:
                        if (partitionEntry.partition.fields[field].type == 'equals'):
                            val = partitionEntry.partition.fields[field].equals
                            if (val not in marginalTotals):
                                marginalTotals[val] = partitionEntry.belief
                            else:
                                marginalTotals[val] += partitionEntry.belief
                    for val in marginalTotals:
                        marginals[field].append({'equals': val, 'belief': marginalTotals[val]})
                    marginals[field].sort(lambda x, y: cmp(x['belief'], y['belief']))
                minBelief = 1.0
                minField = ''
                minValue = ''
                for field in rootEntry.partition.fields:
                    for marginal in marginals[field]:
                        if marginal['belief'] < minBelief:
                            minBelief = marginal['belief']
                            minField = field
                            minValue = marginal['equals']
                if minField != '':
                    self._CompactByFieldValue(minField,minValue)


    def _CompactByProbability(self,minProbability):
        '''
        Compacts a partitionDistribution object down
        to at most maxPartitions.

        This function does not need to be called as
        a part of the normal operation of the class.
        '''
        self.appLogger.info('Compacts a partitionDistribution down based on minimum partition probability')
#        self.stats.InitUpdate()
#        self.stats.StartClock('compact')
        if not self.compactByPruningFieldValuePair:
            partitionCount = len(self.partitionEntryList)
            self.stats.lastUpdateMaxPartitions = partitionCount
            leafPartitionEntryList = []
            i = 0
            for partitionEntry in self.partitionEntryList:
                partitionEntry.selfPointer = i
                if (len(partitionEntry.children) == 0 and partitionEntry.parent != None):
                    leafPartitionEntryList.append(partitionEntry)
                i += 1
            leafPartitionCount = len(leafPartitionEntryList)
            leafPartitionEntryList.sort(PartitionDistribution._ComparePartitionEntries)
            needToCleanup = False
            while (leafPartitionCount > 0 and leafPartitionEntryList[0].belief < minProbability):
                changed = False
                for i in range(leafPartitionCount):
                    partitionEntry = leafPartitionEntryList[i]
                    if partitionEntry.belief < minProbability:
                        if partitionEntry.parent.partition.Recombine(partitionEntry.partition):
                            self.appLogger.info('Combining child (id %d, belief %g) into its parent (id %d)' % (partitionEntry.id,partitionEntry.belief,partitionEntry.parent.id))
                            self.appLogger.info('Parent (%d) is now: %s' % (partitionEntry.parent.id,partitionEntry.parent.partition))
                            parent = partitionEntry.parent
                            # merge histories
                            parent.historyEntryList.extend(partitionEntry.historyEntryList)
                            PartitionDistribution._CombineHistoryDuplicatesOnList(parent.historyEntryList)
                            # merge belief
                            parent.belief = parent.belief + partitionEntry.belief
                            # delete pointer to child
                            del parent.children[ parent.children.index(partitionEntry) ]
                            self.partitionEntryList[ partitionEntry.selfPointer ] = None
                            del leafPartitionEntryList[i]
                            partitionCount -= 1
                            leafPartitionCount -= 1
                            # test if parent is now a leaf
                            if (len(parent.children) == 0 and parent.parent != None):
                                # find the right place to insert the parent
                                insertedFlag = 0
                                for j in range(leafPartitionCount):
                                    if (parent.belief < leafPartitionEntryList[j].belief):
                                        leafPartitionEntryList.insert(j,parent)
                                        insertedFlag = 1
                                        break
                                if (insertedFlag == 0):
                                    leafPartitionEntryList.append(parent)
                                leafPartitionCount += 1
                            leafPartitionEntryList.sort(PartitionDistribution._ComparePartitionEntries)
                            needToCleanup = True
                            changed = True
                            break
                        else:
                            self.appLogger.info('Cannot combine child (id %d, belief %g) into its parent (id %d)' % (partitionEntry.id,partitionEntry.belief,partitionEntry.parent.id))
                if not changed:
                    break
            
            if needToCleanup:
                # Clean up empty entries
                cleanPartitionEntryList = []
                for partitionEntry in self.partitionEntryList:
                    if (partitionEntry != None):
                        cleanPartitionEntryList.append(partitionEntry)
                self.partitionEntryList = cleanPartitionEntryList
        
                rawBeliefTotal = 0.0
                for partitionEntry in self.partitionEntryList:
                    for historyEntry in partitionEntry.historyEntryList:
                        rawBeliefTotal += historyEntry.belief
                        
                for partitionEntry in self.partitionEntryList:
                    partitionEntry.belief = 0.0
                    partitionEntry.newBelief = 0.0
                    for historyEntry in partitionEntry.historyEntryList:
                        historyEntry.belief = historyEntry.belief / rawBeliefTotal
                        historyEntry.origBelief = historyEntry.belief
                        if (historyEntry.belief < 0.0):
                            s =  'historyEntry.belief < 0: %e\n' % (historyEntry.belief)
                            s += ' rawBeliefTotal = %e' % (rawBeliefTotal)
                            raise RuntimeError,s
                        partitionEntry.belief += historyEntry.belief
                    partitionEntry.historyEntryList.sort(PartitionDistribution._CompareHistoryEntries)
                self.partitionEntryList.sort(PartitionDistribution._ComparePartitionEntries)
        else:
            rootEntry = None
            for partitionEntry in self.partitionEntryList:
                if partitionEntry.parent == None:
                    rootEntry = partitionEntry
                    break
            marginals = {}
            for field in rootEntry.partition.fields:
                marginals[field] = []
            for field in rootEntry.partition.fields:
                marginalTotals = {}
                for partitionEntry in self.partitionEntryList:
                    if (partitionEntry.partition.fields[field].type == 'equals'):
                        val = partitionEntry.partition.fields[field].equals
                        if (val not in marginalTotals):
                            marginalTotals[val] = partitionEntry.belief
                        else:
                            marginalTotals[val] += partitionEntry.belief
                for val in marginalTotals:
                    marginals[field].append({'equals': val, 'belief': marginalTotals[val]})
                marginals[field].sort(lambda x, y: cmp(x['belief'], y['belief']))
            for field in rootEntry.partition.fields:
                for marginal in marginals[field]:
                    if marginal['belief'] < minProbability:
                        self._CompactByFieldValue(field,marginal['equals'])
                    else:
                        break


    def _TraversePartitionTreeToCombine(self,parentEntry):
        if len(parentEntry.children) == 0:
            return False
        else:
            for childEntry in parentEntry.children: 
                if self._TraversePartitionTreeToCombine(childEntry):
                    return True
            parent = parentEntry.partition
            for childEntry in parentEntry.children:
                child = childEntry.partition
                fieldsToRecombine = []
                nextChild = False
                self.appLogger.info('Try to combine parent (id %d, belief %g) into its child (id %d)' % (parentEntry.id,parentEntry.belief,childEntry.id))
                self.appLogger.info('Parent %s'%parent)
                self.appLogger.info('Child %s'%child)
                for field in parent.fields:
                    self.appLogger.info('Inspect field %s'%field)
                    if parent.fields[field].type == 'excludes':
                        if child.fields[field].type == 'equals':
                            nextChild = True
                            self.appLogger.info('Parent excludes but child equals')
                        else:
                            if set(parent.fields[field].excludes) == set(child.fields[field].excludes):
                                self.appLogger.info('Parent and child have the same excludes %s'%str(parent.fields[field].excludes))
                                pass
                            elif set(parent.fields[field].excludes).issubset(set(child.fields[field].excludes)) or\
                            set(child.fields[field].excludes).issubset(set(parent.fields[field].excludes)):
                                fieldsToRecombine.append(field)
                                self.appLogger.info("Child's excludes subsets/supersets parent's")
    #                            elif len(parent.fields[field].excludes) == len(child.fields[field].excludes) and \
    #                            len(set(parent.fields[field].excludes).symmetric_difference(set(child.fields[field].excludes))) != 0:
                            else:
                                nextChild = True
                                self.appLogger.info('Disjoint excludes')
                    else:
                        if child.fields[field].type == 'equals' and parent.fields[field].equals == child.fields[field].equals:
                            self.appLogger.info('Parent and child have the same equals %s'%parent.fields[field].equals)
                            pass
                        else:
                            raise RuntimeError,'Error: field %s: parent %s but child %s'%(field,parent,child)
                    if nextChild:
                        break
                if nextChild:
                    continue
                
                for field in fieldsToRecombine:
                    if child.fields[field].type == 'excludes' and \
                    set(child.fields[field].excludes).issubset(set(parent.fields[field].excludes)):
                        child.fields[field].excludes = parent.fields[field].excludes 

                self.appLogger.info('Combining parent (id %d, belief %g) into its child (id %d)' % (parentEntry.id,parentEntry.belief,childEntry.id))
                self.appLogger.info('Child (%d) is now: %s' % (childEntry.id,childEntry.partition))
                childEntry.historyEntryList.extend(parentEntry.historyEntryList)
                PartitionDistribution._CombineHistoryDuplicatesOnList(childEntry.historyEntryList)
                # merge belief
                childEntry.belief = childEntry.belief + parentEntry.belief
                for otherChildEntry in parentEntry.children:
                    if otherChildEntry != childEntry:
                        otherChildEntry.parent = childEntry
                        childEntry.children.append(otherChildEntry)
                childEntry.parent = parentEntry.parent
                if childEntry.parent:
                    childEntry.parent.children.append(childEntry)
                    childEntry.parent.children.remove(parentEntry)
                self.partitionEntryList.remove(parentEntry)
                return True
            else:
                return False


    def KillFieldBelief(self,field,value):
        if value == None:
            self.appLogger.info('Kill belief of every value for field %s'%field)
        else:
            self.appLogger.info('Kill belief of %s for field %s'%(value,field))

#        for partitionEntry in self.partitionEntryList:
#            if partitionEntry.partition.fields[field].type == 'equals':
#                partitionEntry.belief = 0.0
#                partitionEntry.newBelief = 0.0
#                for historyEntry in partitionEntry.historyEntryList:
#                    historyEntry.belief = 0.0
#                    historyEntry.origBelief = 0.0
#        self.CompactByProbability(self.minPartitionProbability)
        if not self.compactByPruningFieldValuePair:
            for partitionEntry in self.partitionEntryList:
                partitionEntry.partition.fields[field].type = 'excludes'
                partitionEntry.partition.fields[field].excludes = {}
                if partitionEntry.parent == None:
                    rootEntry = partitionEntry
    
            needToCombine = True
            while needToCombine:
                self.appLogger.info('** PartitionDistribution: **\n%s'%self)
                needToCombine = self._TraversePartitionTreeToCombine(rootEntry)
                for partitionEntry in self.partitionEntryList:
                    if partitionEntry.parent == None:
                        rootEntry = partitionEntry
                        break
                else:
                    raise RuntimeError,'No Root!!!'
    
            for partitionEntry in self.partitionEntryList:
                count = 1
                fields = partitionEntry.partition.fields
                for field in fields:
                    if fields[field].type == 'excludes':
                        if field == 'route':
                            num_field = self.num_route
                        elif field in ['departure_place','arrival_place']:
                            num_field = self.num_place
                        elif field == 'travel_time':
                            num_field = self.num_time
                        else:
                            raise RuntimeError,'Invalid field %s'%field
                        count *= (num_field - len(fields[field].excludes))
                partitionEntry.partition.count = count
                partitionEntry.partition.prior = 1.0 * count/partitionEntry.partition.totalCount
    
            rawBeliefTotal = 0.0
            for partitionEntry in self.partitionEntryList:
                for historyEntry in partitionEntry.historyEntryList:
                    rawBeliefTotal += historyEntry.belief
                    
            for partitionEntry in self.partitionEntryList:
                partitionEntry.belief = 0.0
                partitionEntry.newBelief = 0.0
                for historyEntry in partitionEntry.historyEntryList:
                    historyEntry.belief = historyEntry.belief / rawBeliefTotal
                    historyEntry.origBelief = historyEntry.belief
                    if (historyEntry.belief < 0.0):
                        s =  'historyEntry.belief < 0: %e\n' % (historyEntry.belief)
                        s += ' rawBeliefTotal = %e' % (rawBeliefTotal)
                        raise RuntimeError,s
                    partitionEntry.belief += historyEntry.belief
                partitionEntry.historyEntryList.sort(PartitionDistribution._CompareHistoryEntries)
            self.partitionEntryList.sort(PartitionDistribution._ComparePartitionEntries)
        else:
            if value == None:
                values = set([])
                for partitionEntry in self.partitionEntryList:
                    if (partitionEntry.partition.fields[field].type == 'equals'):
                        values.add(partitionEntry.partition.fields[field].equals)
                for value in values:
                    self._CompactByFieldValue(field,value)
            else:
                self._CompactByFieldValue(field,value)
            

    @staticmethod
    def _ComparePartitionEntries(a,b):
        return cmp(a.belief,b.belief)

    @staticmethod
    def _CompareHistoryEntries(a,b):
        return cmp(a.belief,b.belief)

    @staticmethod
    def _ComparePartitionEntriesNewBelief(a,b):
        return cmp(a.newBelief,b.newBelief)

    @staticmethod
    def _CombineHistoryDuplicatesOnList(historyEntryList):
        i = 0
        length = len(historyEntryList)
        while (i < length):
            j=i+1
            while (j < length):
                if (historyEntryList[i].history == historyEntryList[j].history):
                    historyEntryList[i].belief += historyEntryList[j].belief
                    del historyEntryList[j]
                    length -= 1
                else:
                    j = j+1
            i=i+1

    @staticmethod
    def _CombineHistoryDuplicatesOffList(historyEntryList):
        i = 0
        length = len(historyEntryList)
        while (i < length):
            j=i+1
            while (j < length):
                if (historyEntryList[i].history == historyEntryList[j].history):
                    historyEntryList[i].belief += historyEntryList[j].belief
                    historyEntryList[i].origBelief += historyEntryList[j].origBelief
                    del historyEntryList[j]
                    length -= 1
                else:
                    j = j+1
            i=i+1

    def __str__(self):
        resultList = ['( id,pid) belief  logBel  [logPri ] description']
        for partitionEntry in self.partitionEntryList:
            logProb = '      -' if (partitionEntry.belief == 0) else '%7.3f' % (log(partitionEntry.belief))
            priorLogProb = '      -' if (partitionEntry.partition.prior == 0) else '%7.3f' % (log(partitionEntry.partition.prior))
            parentID = '-' if (partitionEntry.parent == None) else partitionEntry.parent.id
            s = '(%3.d,%3s) %.5f %5s [%5s] %s' % (partitionEntry.id, parentID, partitionEntry.belief, logProb, priorLogProb,partitionEntry.partition.__str__())
            resultList.append(s)
            for historyEntry in partitionEntry.historyEntryList:
                logProb = '      -' if (historyEntry.belief == 0) else '%7.3f' % (log(historyEntry.belief))
                s = '          %.5f %5s           %s' % (historyEntry.belief, logProb, historyEntry.history.__str__())
                resultList.append(s)
        return '\n'.join(resultList)

def _LogToStringSafely(n):
    if (n == 0.0):
        return '-'
    elif (n < 0.0):
        print 'Cannot take log of value less than 0: %f' % (n)
        return '-'
        #raise RuntimeError,'Cannot take log of value less than 0: %f' % (n)
    else:
        return '%s' % (log(n))

class _PartitionEntry(object):
    __slots__ = ['appLogger', 'children', 'historyEntryList','newHistoryEntryList','id','partition','parent','belief','selfPointer','newBelief']
    def __init__(self,partition,belief,parent,nextPartitionEntryID):
        self.appLogger = logging.getLogger('Learning')
        self.children = []
        self.historyEntryList = []
        self.newHistoryEntryList = []
        self.id = nextPartitionEntryID[0]
        nextPartitionEntryID[0] += 1
        self.partition = partition
        self.belief = belief
        self.parent = parent
        self.selfPointer = -1
        self.newBelief = None

    
    def Prune(self,field,value):
        self.appLogger.info('Pruning in partition (id %d) = %s'%(self.id,self.partition))
        if len(self.children) > 0:
            for child in self.children:
                child.Prune(field,value)
        else:
            self.appLogger.info('Leaf partition (id %d) completed'%self.id)
            return
        if self.partition.fields[field].type == 'excludes' and value in self.partition.fields[field].excludes:
            for child in self.children:
                if child.partition.fields[field].type == 'equals' and child.partition.fields[field].equals == value:
#                    partitionToCombine = child
                    self.appLogger.info('Child (id %d) to prune = %s'%(child.id,child.partition))
                    beliefs = []
                    child._DeletePartition(beliefs)
                    beliefs.append(child.belief)
                    child.parent = None
                    self.children.remove(child)
                    self.appLogger.info('Child (id %d) removed'%child.id)
                    self._UpdateBeliefAndRemoveComplements(beliefs,field,value)
                    break
#            else:
#                raise RuntimeError,'No complement for %s=%s'%(field,value)
#            beliefs = []
#            partitionToCombine._DeletePartition(beliefs)
#            beliefs.append(partitionToCombine.belief)
#            partitionToCombine.parent = None
#            self.children.remove(partitionToCombine)
#            self.appLogger.info('Child (id %d) removed'%partitionToCombine.id)
#            self._UpdateBeliefAndRemoveComplements(beliefs,field,value)
        self.appLogger.info('Partition (id %d) completed'%self.id)


    def _DeletePartition(self,beliefs):
        self.appLogger.info('Delete partition (id %d) %s'%(self.id,self.partition))
        toRemoveChildList = []
        for child in self.children:
            child._DeletePartition(beliefs)
            beliefs.append(child.belief)
            child.parent = None
            toRemoveChildList.append(child)
        for child in toRemoveChildList:
            self.children.remove(child)
            self.appLogger.info('Child (id %d) of partition (id %d) removed'%(child.id,self.id))
        self.appLogger.info('Partition (id %d) completed'%self.id)
    
    
    def _UpdateBeliefAndRemoveComplements(self,beliefs,field,value):
        self.appLogger.info('Update partition (id %d) %s'%(self.id,str(self.partition.fields[field].excludes)))
        self.belief += beliefs.pop(0)
        del self.partition.fields[field].excludes[value]
        self.appLogger.info('Belief of partition (id %d) updated'%self.id)
        for child in self.children:
            if child.partition.fields[field].type == 'excludes' and value in child.partition.fields[field].excludes:
                child._UpdateBeliefAndRemoveComplements(beliefs,field,value)
                if len(beliefs) == 0:
                    break
        self.appLogger.info('Partition (id %d) completed'%self.id)
    
    
class _HistoryEntry(object):
    __slots__ = ['belief','history','userActionLikelihoodTotal','origBelief','userActionLikelihoodTypes']
    def __init__(self):
        self.userActionLikelihoodTypes = {}

class _Stats(object):
    def __init__(self):
        self.InitUpdate()

    def InitUpdate(self):
        self.lastUpdateMaxPartitions = 0
        self.lastUpdateSplits = 0
        self.clocks = {}
        self.clocksTemp = {}

    def StartClock(self,name):
        self.clocksTemp[name] = self._CPU()

    def EndClock(self,name):
        if (name in self.clocks):
            self.clocks[name] += self._CPU() - self.clocksTemp[name]
        else:
            self.clocks[name] = self._CPU() - self.clocksTemp[name]

    @staticmethod
    def _CPU():
        return 0#(resource.getrusage(resource.RUSAGE_SELF).ru_utime+
                #resource.getrusage(resource.RUSAGE_SELF).ru_stime)

class _DefaultHistory(object):
    @staticmethod
    def Seed(partition):
        return [_DefaultHistory()]

    def __init__(self):
        self.prior = 1.0

    def __eq__(self,otherHistory):
        return True

    def Update(self,partition,userAction,sysAction):
        return

    def Copy(self):
        return _DefaultHistory()

    def __str__(self):
        return '-'
