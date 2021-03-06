'''
Illustration of how to simulate a dialog.

This example shows how to simulate a single dialog.  A simulated
user is asked for each of the four fields.  The simulated user's
response is then passed to an ASR simulation, which adds synthetic
errors.  The belief state is updated.

Since the user's responses and ASR errors are random, each run
is different.

The system's policy used here is very simple, and doesn't change
based on user responses.

Part of the AT&T Statistical Dialog Toolkit (ASDT).

Jason D. Williams
jdw@research.att.com
www.research.att.com/people/Williams_Jason_D
'''

# Extend sys.path to include src directory
import os,sys,shutil,traceback
import datetime as dt
#sys.path.append(os.path.join(os.path.dirname(__file__),'../../src'))

import logging.config
import logging
import numpy as np
from GlobalConfig import *
from BeliefState import BeliefState
from UserSimulation import UserSimulation
from DialogModules import UserAction,ASRResult
from DB import InitDB
#from DialogManager import OpenDialogManager as DialogManager
from DialogManager import SBSarsaDialogManager as DialogManager

def GetReward(rewards,userGoal,beliefState,sysAction):
#    if sysAction.type == 'inform':
#        field = beliefState.GetTopUserGoal()
#        if userGoal['Bus number'] == '' and field['route'].type == 'equals':
#            return rewards['taskFailureReward']
#        if userGoal['Bus number'] != '' and field['route'].type != 'equals':
#            return rewards['taskFailureReward']
#        if userGoal['Bus number'] != '' and userGoal['Bus number'] != field['route'].equals:
#            return rewards['taskFailureReward']
#        if userGoal['Departure place'] == '' and field['departure_place'].type == 'equals':
#            return rewards['taskFailureReward']
#        if userGoal['Departure place'] != '' and field['departure_place'].type != 'equals':
#            return rewards['taskFailureReward']
#        if userGoal['Departure place'] != '' and userGoal['Departure place'] != field['departure_place'].equals:
#            return rewards['taskFailureReward']
#        if userGoal['Arrival place'] == '' and field['arrival_place'].type == 'equals':
#            return rewards['taskFailureReward']
#        if userGoal['Arrival place'] != '' and field['arrival_place'].type != 'equals':
#            return rewards['taskFailureReward']
#        if userGoal['Arrival place'] != '' and userGoal['Arrival place'] != field['arrival_place'].equals:
#            return rewards['taskFailureReward']
#        if userGoal['Travel time'] == '' and field['travel_time'].type == 'equals':
#            return rewards['taskFailureReward']
#        if userGoal['Travel time'] != '' and field['travel_time'].type != 'equals':
#            return rewards['taskFailureReward']
#        if userGoal['Travel time'] != '' and userGoal['Travel time'] != field['travel_time'].equals:
#            return rewards['taskFailureReward']
#        return rewards['taskSuccessReward']
#    else:
#        return rewards['taskProceedReward']
    reward = rewards['taskProceedReward']
    fieldMatch = {'departure_place':True,'arrival_place':True,'travel_time':True,'route':True}
    field = beliefState.GetTopUserGoal()
    if userGoal['Bus number'] == '' and field['route'].type == 'equals':
#        reward = rewards['taskFailureReward']
        fieldMatch['route'] = False
    elif userGoal['Bus number'] != '' and field['route'].type != 'equals':
#        reward = rewards['taskFailureReward']
        fieldMatch['route'] = False
    elif userGoal['Bus number'] != '' and userGoal['Bus number'] != field['route'].equals:
#        reward = rewards['taskFailureReward']
        fieldMatch['route'] = False
    elif userGoal['Departure place'] == '' and field['departure_place'].type == 'equals':
#        reward = rewards['taskFailureReward']
        fieldMatch['departure_place'] = False
    elif userGoal['Departure place'] != '' and field['departure_place'].type != 'equals':
#        reward = rewards['taskFailureReward']
        fieldMatch['departure_place'] = False
    elif userGoal['Departure place'] != '' and userGoal['Departure place'] != field['departure_place'].equals:
#        reward = rewards['taskFailureReward']
        fieldMatch['departure_place'] = False
    elif userGoal['Arrival place'] == '' and field['arrival_place'].type == 'equals':
#        reward = rewards['taskFailureReward']
        fieldMatch['arrival_place'] = False
    elif userGoal['Arrival place'] != '' and field['arrival_place'].type != 'equals':
#        reward = rewards['taskFailureReward']
        fieldMatch['arrival_place'] = False
    elif userGoal['Arrival place'] != '' and userGoal['Arrival place'] != field['arrival_place'].equals:
#        reward = rewards['taskFailureReward']
        fieldMatch['arrival_place'] = False
    elif userGoal['Travel time'] == '' and field['travel_time'].type == 'equals':
#        reward = rewards['taskFailureReward']
        fieldMatch['travel_time'] = False
    elif userGoal['Travel time'] != '' and field['travel_time'].type != 'equals':
#        reward = rewards['taskFailureReward']
        fieldMatch['travel_time'] = False
    elif userGoal['Travel time'] != '' and userGoal['Travel time'] != field['travel_time'].equals:
#        reward = rewards['taskFailureReward']
        fieldMatch['travel_time'] = False
    elif sysAction.type == 'inform':
        reward = rewards['taskSuccessReward']
#    else:
#        reward = rewards['taskProceedReward']
    return reward,fieldMatch

def GetSubSuccess(userGoal,beliefState,sysAction):
    if sysAction.type == 'inform':
        field = beliefState.GetTopUserGoal()
        if userGoal['Departure place'] == '' and field['departure_place'].type == 'equals':
            return False
        if userGoal['Departure place'] != '' and field['departure_place'].type != 'equals':
            return False
        if userGoal['Departure place'] != '' and userGoal['Departure place'] != field['departure_place'].equals:
            return False
        if userGoal['Arrival place'] == '' and field['arrival_place'].type == 'equals':
            return False
        if userGoal['Arrival place'] != '' and field['arrival_place'].type != 'equals':
            return False
        if userGoal['Arrival place'] != '' and userGoal['Arrival place'] != field['arrival_place'].equals:
            return False
        if userGoal['Travel time'] == '' and field['travel_time'].type == 'equals':
            return False
        if userGoal['Travel time'] != '' and field['travel_time'].type != 'equals':
            return False
        if userGoal['Travel time'] != '' and userGoal['Travel time'] != field['travel_time'].equals:
            return False
        return True
    else:
        return False
    
def SimulateOneDialog(userSimulation,dialogManager,rewards,errorRate=-1,preventCorrectionInConfirm=False,preferDirectAnswerToRoute=False):
    '''
    Simulates one dialog.

      userSimulation is a Simulation.UserSimulation object

      asrSimulation is a Simulation.ASRSimulation object

      dialogManager is a DialogManager.* object

    Displays result on the "Transcript" logger
    '''
    userSimulation.Init(errorRate)
    systemAction = dialogManager.Init()

    appLogger = logging.getLogger('Transcript')
    appLogger.info('------ Prior to start of dialog ------')
    appLogger.info('PartitionDistribution:\n%s' % (dialogManager.beliefState))

    dialogSuccess = False
    dialogSubSuccess = False
    dialogReward = 0
    i = 0
    turns = []
    while(systemAction.type == 'ask'):
        appLogger.info('\n------ Turn %d ------' % (i+1))
        appLogger.info('User Goal: %s'%userSimulation.goal)
        appLogger.info('System Action: %s' % (systemAction))
        
        userAction = userSimulation.TakeTurn(systemAction)

        appLogger.info('User Action: %s' % (userAction))

        if userAction.userActions[0].type == 'hangup':
            break
        
        if preventCorrectionInConfirm:
            if systemAction.type == 'ask' and systemAction.force == 'confirm' and\
            userAction.userActions[0].type != 'non-understanding' and 'confirm' in userAction.userActions[0].content:
                appLogger.info('For now, just deal with YES/NO only in a turn')
                userAction.userActions[0].content = {'confirm':userAction.userActions[0].content['confirm']}
#            elif systemAction.type == 'ask' and systemAction.force == 'request' and\
#            userAction.userActions[0].type != 'non-understanding' and 'confirm' in userAction.userActions[0].content:
#                appLogger.info('For now, just remove useless YES/NO in response to request')
#                del userAction.userActions[0].content['confirm']

        if preferDirectAnswerToRoute and userAction.userActions[0].type != 'non-understanding' and\
        'route' in userAction.userActions[0].content and len(userAction.userActions[0].content) > 1:
            if not (systemAction.type == 'ask' and systemAction.force == 'confirm' and 'route' in systemAction.content):
                if (systemAction.type == 'ask' and systemAction.force == 'confirm' and\
                (not set(userAction.userActions[0].content).isdisjoint(set(systemAction.content)))) or\
                (systemAction.type == 'ask' and systemAction.force == 'request' and\
                systemAction.content in userAction.userActions[0].content):
                    appLogger.info('For now, just remove route to focus on other fields')
                    del userAction.userActions[0].content['route']

        if userAction.userActions[0].type != 'hangup' and userAction.userActions[0].content == {}:
            userAction = ASRResult.Simulated(None,[UserAction('non-understanding')],[1.0])
        
        appLogger.info('User Action: %s' % (userAction))
#        asrResult = asrSimulation.SimASR(systemAction.grammar,userAction)
#        appLogger.info('** ASR Result: **\n%s' % (asrResult))
        
        reward,fieldMatch = GetReward(rewards,userSimulation.goal,dialogManager.beliefState,systemAction)
        dialogReward += reward
        
        nextSystemAction = dialogManager.TakeTurn(userAction,reward)
        
#        appLogger.info('** PartitionDistribution: **\n%s' % (dialogManager.beliefState))
        
        updateTime = 0 #dialogManager.beliefState.partitionDistribution.stats.clocks['mainUpdate']
        
#        appLogger.info('Update time: %f' % (updateTime))
        
        turns.append({
            'systemAction': systemAction,
            'userAction':userAction,
            'updateTime':updateTime,
        })
        
        systemAction = nextSystemAction

        if i >= 39:#rewards['taskSuccessReward']:
            break
        i += 1
    if userAction.userActions[0].type != 'hangup':
        reward,fieldMatch = GetReward(rewards,userSimulation.goal,dialogManager.beliefState,systemAction)
        dialogReward += reward
        dialogManager.TakeTurn(None,reward)
#        if systemAction.type == 'inform' and reward == rewards['taskSuccessReward']:
        if systemAction.type == 'inform':
            dialogSuccess = True
        dialogSubSuccess = GetSubSuccess(userSimulation.goal,dialogManager.beliefState,systemAction)
    else:
        appLogger.info('User hung up')
    appLogger.info('\n------ Turn %d ------' % (i+1))
    appLogger.info('System Action: %s' % (systemAction))
    appLogger.info('User Goal: %s'%userSimulation.goal)
#    appLogger.info('Dialog %s'%('Success' if dialogManager.DialogResult()[0] else 'Fail'))
    appLogger.info('Dialog %s'%('Success' if dialogSuccess else 'Fail'))
    appLogger.info('Dialog %s in ignorance of route'%('Success' if dialogSubSuccess else 'Fail'))
#    turns.append({
#        'systemAction': systemAction,
#        'userAction':None,
#        'updateTime':None,
#    })
    log = {
           'userGoal': userSimulation.goal,
           'turns' : turns,
#           'result': dialogManager.DialogResult()
           'result': (dialogSuccess,dialogReward,fieldMatch),
           'subSuccess': dialogSubSuccess
           }
    return log

def main():
    InitConfig()
    config = GetConfig()
    config.read(['LGrl.conf'])
    config.set('Global','modelPath','.')
    config.set('DialogManager','dialogStrategyLearning','false')
    
    rewards = {}
    rewards['taskSuccessReward'] = config.getint('DialogManager','taskSuccessReward')
    rewards['taskFailureReward'] = config.getint('DialogManager','taskFailureReward')
    rewards['taskProceedReward'] = config.getint('DialogManager','taskProceedReward')

#    InitDB()
    for testIndex in range(0,1):
        logging.config.fileConfig('logging.conf')
        if testIndex == 0:
            iter = [496]
            errorRates = [-1]
            config.set('PartitionDistribution','offListBeliefUpdateMethod','heuristicPossibleActions')
            config.set('PartitionDistribution','minPartitionProbability','1e-6')
            config.set('PartitionDistribution','compactByPruningFieldValuePair','true')
            config.set('PartitionDistribution','maxPartitions','256')
            config.set('PartitionDistribution','defaultResetFraction','0.01')
            config.set('PartitionDistribution','resetFractionApplyThreshold','0.99')
            config.set('PartitionDistribution','applyResetFractionPerField','true')
            config.set('BeliefState','numberOfPossibleActionsForConfirmation','1000000000')
            config.set('BeliefState','fixedASRConfusionProbability','0.3')
            config.set('BeliefState','useLearnedUserModel','true')
            config.set('BeliefState','useHistory','false')
            config.set('BeliefState','minRelevantUserActProb','1e-3')
            config.set('BeliefState','irrelevantUserActProb','1e-20')
            config.set('DialogManager','confidenceScoreCalibration','true')
            config.set('DialogManager','routeRejectThresholdMultiplier','0.1')
            config.set('DialogManager','imposeConfirmStrategy','true')
            config.set('DialogManager','maxRepeatedConfirmFail','1')
            config.set('DialogManager','fieldAcceptThreshold','0.9')
            config.set('DialogManager','basisWidth','0.25')
            config.set('DialogThread','integrateExceptionalHandlingIntoBeliefTracking','false')
            preventCorrectionInConfirm = True
            preferDirectAnswerToRoute = False
        elif testIndex == 1:
            iter = [1000]
            errorRates = [-1]
            config.set('PartitionDistribution','offListBeliefUpdateMethod','heuristicPossibleActions')
            config.set('PartitionDistribution','minPartitionProbability','1e-5')
            config.set('PartitionDistribution','compactByPruningFieldValuePair','true')
            config.set('PartitionDistribution','maxPartitions','256')
            config.set('PartitionDistribution','defaultResetFraction','0.05')
            config.set('PartitionDistribution','resetFractionApplyThreshold','0.97')
            config.set('PartitionDistribution','applyResetFractionPerField','true')
            config.set('BeliefState','numberOfPossibleActionsForConfirmation','1000000')
            config.set('BeliefState','fixedASRConfusionProbability','0.3')
            config.set('BeliefState','useLearnedUserModel','true')
            config.set('BeliefState','useHistory','false')
            config.set('BeliefState','minRelevantUserActProb','5e-2')
            config.set('BeliefState','irrelevantUserActProb','1e-20')
            config.set('DialogManager','confidenceScoreCalibration','true')
            config.set('DialogManager','routeRejectThresholdMultiplier','0.1')
            config.set('DialogManager','imposeConfirmStrategy','false')
            config.set('DialogManager','fieldAcceptThreshold','0.9')
            config.set('DialogManager','basisWidth','0.25')
            config.set('DialogThread','integrateExceptionalHandlingIntoBeliefTracking','false')
            preventCorrectionInConfirm = True
            preferDirectAnswerToRoute = False
        elif testIndex == 2:
            iter = [1000]
            errorRates = [-1]
            config.set('PartitionDistribution','offListBeliefUpdateMethod','heuristicPossibleActions')
            config.set('PartitionDistribution','minPartitionProbability','1e-5')
            config.set('PartitionDistribution','compactByPruningFieldValuePair','true')
            config.set('PartitionDistribution','maxPartitions','256')
            config.set('PartitionDistribution','defaultResetFraction','0.01')
            config.set('PartitionDistribution','resetFractionApplyThreshold','0.99')
            config.set('PartitionDistribution','applyResetFractionPerField','true')
            config.set('BeliefState','numberOfPossibleActionsForConfirmation','1000000')
            config.set('BeliefState','fixedASRConfusionProbability','0.3')
            config.set('BeliefState','useLearnedUserModel','true')
            config.set('BeliefState','useHistory','false')
            config.set('BeliefState','minRelevantUserActProb','1e-3')
            config.set('BeliefState','irrelevantUserActProb','1e-20')
            config.set('DialogManager','confidenceScoreCalibration','true')
            config.set('DialogManager','routeRejectThresholdMultiplier','0.1')
            config.set('DialogManager','imposeConfirmStrategy','false')
            config.set('DialogManager','fieldAcceptThreshold','0.9')
            config.set('DialogManager','basisWidth','0.25')
            config.set('DialogThread','integrateExceptionalHandlingIntoBeliefTracking','false')
            preventCorrectionInConfirm = True
            preferDirectAnswerToRoute = False
        elif testIndex == 3:
            iter = [1000]
            errorRates = [-1]
            config.set('PartitionDistribution','offListBeliefUpdateMethod','heuristicPossibleActions')
            config.set('PartitionDistribution','minPartitionProbability','1e-4')
            config.set('BeliefState','numberOfPossibleActionsForConfirmation','1000')
            config.set('BeliefState','fixedASRConfusionProbability','0.3')
            config.set('DialogThread','preventCorrectionInConfirm','true')
            config.set('DialogManager','confidenceScoreCalibration','false')
            config.set('BeliefState','useLearnedUserModel','false')
        elif testIndex == 4:
            iter = [300]
            errorRates = [-1]
            config.set('PartitionDistribution','offListBeliefUpdateMethod','heuristicUsingPrior')
            config.set('DialogThread','preventCorrectionInConfirm','true')
            config.set('BeliefState','fixedASRConfusionProbability','1.0')
#        elif testIndex == 4:
#            iter = [500]
#            errorRates = [-1]
#            config.set('DialogManager','preferNaturalSequence','false')
            
#        iter = [100,50,25]
#        iter = [200]
#        errorRates = [0,1,2]
#        errorRates = [-1]
        interval = 1
#        basisFunctionMax = [500]
        basisFunctionMax = ['500','500','500','500']
        totalDialogSuccessCount = 0
        intervalDialogSuccessCount = 0
        totalDialogSuccessRate = []
        intervalDialogSuccessRate = []
        totalDialogSubSuccessCount = 0
        intervalDialogSubSuccessCount = 0
        totalDialogSubSuccessRate = []
        intervalDialogSubSuccessRate = []
        totalDialogReward = []
        intervalDialogReward = []
        totalAvgDialogReward = []
        intervalAvgDialogReward = []
        totalDialogLength = []
        intervalDialogLength = []
        totalAvgDialogLength = []
        intervalAvgDialogLength = []
        intervalElapsedTime = []
        totalIncorrectRouteCount = 0
        intervalIncorrectRouteCount = 0
        intervalIncorrectRouteCounts = []
        totalIncorrectDeparturePlaceCount = 0
        intervalIncorrectDeparturePlaceCount = 0
        intervalIncorrectDeparturePlaceCounts = []
        totalIncorrectArrivalPlaceCount = 0
        intervalIncorrectArrivalPlaceCount = 0
        intervalIncorrectArrivalPlaceCounts = []
        totalIncorrectTravelTimeCount = 0
        intervalIncorrectTravelTimeCount = 0
        intervalIncorrectTravelTimeCounts = []
        dialogLengthDict = {}
        successDialogLengthDict = {}
        failDialogLengthDict = {}
        
        startTime = dt.datetime.now()
        intervalStartTime = dt.datetime.now()

        appLogger = logging.getLogger('Transcript')

        dialogStrategyLearning = config.getboolean('DialogManager','dialogStrategyLearning')
#        config.set('DialogManager','dialogStrategyLearning',dialogStrategyLearning)
        
        if not dialogStrategyLearning:
            config.set('SparseBayes','CONTROL_BasisFunctionMax',basisFunctionMax[0])
            try:
                os.remove('DataPoints.model')
                os.remove('Mu.model')
                os.remove('Relevant.model')
            except:
                pass
            shutil.copy('DataPoints-%d.model'%testIndex,'DataPoints.model')
            shutil.copy('Mu-%d.model'%testIndex,'Mu.model')
            shutil.copy('Relevant-%d.model'%testIndex,'Relevant.model')
        
        dialogManager = DialogManager()
        userSimulation = UserSimulation()

        dialogNum = 0    
        maxDialogNum = sum(iter)    
        for ei,errorRate in enumerate(errorRates):
#        for ei,errorRate in enumerate([0]):
#            if ei > 0:
#                X,Targets,raw_BASIS,BASIS,Used,\
#                Alpha,beta,\
#                Aligned_out,Aligned_in,\
#                Relevant,Mu = dialogManager.GetPresentLearningStatus()
#            config.set('SparseBayes','CONTROL_BasisFunctionMax',basisFunctionMax[ei])
#                dialogManager = DialogManager()
#                dialogManager.SetLearningStatus(X,Targets,raw_BASIS,BASIS,Used,
#                                                  Alpha,beta,Aligned_out,Aligned_in,Relevant,Mu)
            if dialogStrategyLearning:
                config.set('SparseBayes','CONTROL_BasisFunctionMax',basisFunctionMax[ei])
                
            dialogManager.ReloadConfig()
            for i in range(iter[ei]):
#                appLogger = logging.getLogger('Transcript')
#                appLogger.info('Dialog %d'%i)
                
#                errorRate = i/(iter/1)
#                appLogger.info('Error rate %d'%errorRate)
                appLogger.info('Dialog %d'%dialogNum)
                appLogger.info('Error rate %d'%errorRate)

#                rewards['taskSuccessReward'] = config.getint('DialogManager','taskSuccessReward')
#                rewards['taskSuccessReward'] += errorRate*5 
                while True:
                    try:
                        log = SimulateOneDialog(userSimulation,dialogManager,rewards,errorRate,\
                                                preventCorrectionInConfirm,preferDirectAnswerToRoute)
                    except:
                        appLogger.error(traceback.format_exc())
#                        exit()
                        continue
                    break
                
                totalDialogReward.append(log['result'][1])
                intervalDialogReward.append(log['result'][1])
                totalDialogLength.append(len(log['turns']))
                intervalDialogLength.append(len(log['turns']))
                
                if len(log['turns']) in dialogLengthDict:
                    dialogLengthDict[len(log['turns'])] += 1
                else:
                    dialogLengthDict[len(log['turns'])] = 1
                    
                if log['result'][0]: 
                    totalDialogSuccessCount += 1
                    intervalDialogSuccessCount += 1
                    if len(log['turns']) in successDialogLengthDict:
                        successDialogLengthDict[len(log['turns'])] += 1
                    else:
                        successDialogLengthDict[len(log['turns'])] = 1
                else:
                    if len(log['turns']) in failDialogLengthDict:
                        failDialogLengthDict[len(log['turns'])] += 1
                    else:
                        failDialogLengthDict[len(log['turns'])] = 1
                if log['subSuccess']: 
                    totalDialogSubSuccessCount += 1
                    intervalDialogSubSuccessCount += 1
                if not log['result'][2]['route']:
                    totalIncorrectRouteCount += 1
                    intervalIncorrectRouteCount += 1
                if not log['result'][2]['departure_place']:
                    totalIncorrectDeparturePlaceCount += 1
                    intervalIncorrectDeparturePlaceCount += 1
                if not log['result'][2]['arrival_place']:
                    totalIncorrectArrivalPlaceCount += 1
                    intervalIncorrectArrivalPlaceCount += 1
                if not log['result'][2]['travel_time']:
                    totalIncorrectTravelTimeCount += 1
                    intervalIncorrectTravelTimeCount += 1
#                if (i+1) % (iter[errorRate]/interval) == 0:
                if (dialogNum+1) % (maxDialogNum/interval) == 0:
                    intervalElapsedTime.append(str(dt.datetime.now() - intervalStartTime))
                    appLogger.info('Interval elapsed time: %s'%intervalElapsedTime[-1])
        
#                    intervalAvgDialogLength.append(float(sum(intervalDialogLength))/(float(iter)/interval))
                    intervalAvgDialogLength.append(float(sum(intervalDialogLength))/(float(maxDialogNum)/interval))
                    intervalDialogLength = []
                    appLogger.info('Interval average dialog length: %f'%intervalAvgDialogLength[-1])
                    
#                    totalAvgDialogLength.append(float(sum(totalDialogLength))/(i+1))
                    totalAvgDialogLength.append(float(sum(totalDialogLength))/(dialogNum+1))
                    appLogger.info('Cumulative average dialog length: %f'%totalAvgDialogLength[-1])
                    
#                    intervalAvgDialogReward.append(float(sum(intervalDialogReward))/(float(iter)/interval))
                    intervalAvgDialogReward.append(float(sum(intervalDialogReward))/(float(maxDialogNum)/interval))
                    intervalDialogReward = []
                    appLogger.info('Interval average dialog reward: %f'%intervalAvgDialogReward[-1])
                    
#                    totalAvgDialogReward.append(float(sum(totalDialogReward))/(i+1))
                    totalAvgDialogReward.append(float(sum(totalDialogReward))/(dialogNum+1))
                    appLogger.info('Cumulative average dialog reward: %f'%totalAvgDialogReward[-1])
                    
#                    intervalDialogSuccessRate.append(float(intervalDialogSuccessCount)/(float(iter)/interval))
                    intervalDialogSuccessRate.append(float(intervalDialogSuccessCount)/(float(maxDialogNum)/interval))
                    intervalDialogSuccessCount = 0
                    appLogger.info('Interval dialog success rate: %f'%intervalDialogSuccessRate[-1])
                    
#                    totalDialogSuccessRate.append(float(totalDialogSuccessCount)/(i+1))
                    totalDialogSuccessRate.append(float(totalDialogSuccessCount)/(dialogNum+1))
                    appLogger.info('Cumulative dialog success rate: %f'%totalDialogSuccessRate[-1])
                    
#                    intervalDialogSubSuccessRate.append(float(intervalDialogSubSuccessCount)/(float(iter)/interval))
                    intervalDialogSubSuccessRate.append(float(intervalDialogSubSuccessCount)/(float(maxDialogNum)/interval))
                    intervalDialogSubSuccessCount = 0
                    appLogger.info('Interval dialog success rate in ignorance of route: %f'%intervalDialogSubSuccessRate[-1])
                    
#                    totalDialogSubSuccessRate.append(float(totalDialogSubSuccessCount)/(i+1))
                    totalDialogSubSuccessRate.append(float(totalDialogSubSuccessCount)/(dialogNum+1))
                    appLogger.info('Cumulative dialog success rate in ignorance of route: %f'%totalDialogSubSuccessRate[-1])

                    intervalIncorrectRouteCounts.append(intervalIncorrectRouteCount)
                    intervalIncorrectRouteCount = 0
                    appLogger.info('Interval number of incorrect route: %d'%intervalIncorrectRouteCounts[-1])
                    
                    intervalIncorrectDeparturePlaceCounts.append(intervalIncorrectDeparturePlaceCount)
                    intervalIncorrectDeparturePlaceCount = 0
                    appLogger.info('Interval number of incorrect departure place: %d'%intervalIncorrectDeparturePlaceCounts[-1])
                    
                    intervalIncorrectArrivalPlaceCounts.append(intervalIncorrectArrivalPlaceCount)
                    intervalIncorrectArrivalPlaceCount = 0
                    appLogger.info('Interval number of incorrect arrival place: %d'%intervalIncorrectArrivalPlaceCounts[-1])
                    
                    intervalIncorrectTravelTimeCounts.append(intervalIncorrectTravelTimeCount)
                    intervalIncorrectTravelTimeCount = 0
                    appLogger.info('Interval number of incorrect travel time: %d'%intervalIncorrectTravelTimeCounts[-1])
                    
                    intervalStartTime = dt.datetime.now()
                    
    #            if (i+1) % (iter/1) == 0:
    #                dialogManager.StoreModel('%d'%errorRate)
                dialogNum += 1
            
        endTime = dt.datetime.now()
        if dialogStrategyLearning:
            dialogManager.StoreModel('%d'%testIndex)
        
        appLogger.info('Interval average dialog length: %s'%str(intervalAvgDialogLength))
        appLogger.info('Cumulative average dialog length: %s'%str(totalAvgDialogLength))
        
        appLogger.info('Interval average dialog reward: %s'%str(intervalAvgDialogReward))
        appLogger.info('Cumulative average dialog reward: %s'%str(totalAvgDialogReward))
        
        appLogger.info('Interval dialog success rates: %s'%str(intervalDialogSuccessRate))
        appLogger.info('Cumulative dialog success rates: %s'%str(totalDialogSuccessRate))
        appLogger.info('Total dialog success count: %d'%totalDialogSuccessCount)
        
        appLogger.info('Interval dialog success rates in ignorance of route: %s'%str(intervalDialogSubSuccessRate))
        appLogger.info('Cumulative dialog success rates in ignorance of route: %s'%str(totalDialogSubSuccessRate))
        appLogger.info('Total dialog success count in ignorance of route: %d'%totalDialogSubSuccessCount)
    
        appLogger.info('Interval number of incorrect route: %s'%str(intervalIncorrectRouteCounts))
        appLogger.info('Total number of incorrect route: %d'%totalIncorrectRouteCount)

        appLogger.info('Interval number of incorrect departure place: %s'%str(intervalIncorrectDeparturePlaceCounts))
        appLogger.info('Total number of incorrect departure place: %d'%totalIncorrectDeparturePlaceCount)

        appLogger.info('Interval number of incorrect arrival place: %s'%str(intervalIncorrectArrivalPlaceCounts))
        appLogger.info('Total number of incorrect arrival place: %d'%totalIncorrectArrivalPlaceCount)

        appLogger.info('Interval number of incorrect travel time: %s'%str(intervalIncorrectTravelTimeCounts))
        appLogger.info('Total number of incorrect travel time: %d'%totalIncorrectTravelTimeCount)

        appLogger.info('Interval elapsed times: %s'%str(intervalElapsedTime))
        appLogger.info('Start time: %s'%startTime.isoformat(' '))
        appLogger.info('End time: %s'%endTime.isoformat(' '))
        appLogger.info('Total elapsed time: %s'%(endTime - startTime))
        
        appLogger.info('Dialog length distribution: \n%s'%str(dialogLengthDict))
        appLogger.info('Success dialog length distribution: \n%s'%str(successDialogLengthDict))
        appLogger.info('Fail dialog length distribution: \n%s'%str(failDialogLengthDict))
        
        lengthList = []
        for key in dialogLengthDict:
            lengthList.extend([key]*dialogLengthDict[key])
        appLogger.info('Dialog length average: %f (+/- %f)'%(np.average(lengthList),np.std(lengthList)))
        lengthList = []
        for key in successDialogLengthDict:
            lengthList.extend([key]*successDialogLengthDict[key])
        appLogger.info('Success dialog length average: %f (+/- %f)'%(np.average(lengthList),np.std(lengthList)))
        lengthList = []
        for key in failDialogLengthDict:
            lengthList.extend([key]*failDialogLengthDict[key])
        appLogger.info('Fail dialog average: %f (+/- %f)'%(np.average(lengthList),np.std(lengthList)))
        
        logging.shutdown()
        try:
            os.remove('run-%d.log'%testIndex)
        except:
            pass
        os.rename('run.log','run-%d.log'%testIndex)
        
if (__name__ == '__main__'):
    main()
