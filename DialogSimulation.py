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
import os,sys
import datetime as dt
#sys.path.append(os.path.join(os.path.dirname(__file__),'../../src'))

import logging.config
import logging
from GlobalConfig import *
from BeliefState import BeliefState
from UserSimulation import UserSimulation
from DB import InitDB
#from DialogManager import OpenDialogManager as DialogManager
from DialogManager import SBSarsaDialogManager as DialogManager

def GetReward(rewards,userGoal,beliefState,sysAction):
    if sysAction.type == 'inform':
        field = beliefState.GetTopUserGoal()
        if userGoal['Bus number'] == '' and field['route'].type == 'equals':
            return rewards['taskFailureReward']
        if userGoal['Bus number'] != '' and field['route'].type != 'equals':
            return rewards['taskFailureReward']
        if userGoal['Bus number'] != '' and userGoal['Bus number'] != field['route'].equals:
            return rewards['taskFailureReward']
        if userGoal['Departure place'] == '' and field['departure_place'].type == 'equals':
            return rewards['taskFailureReward']
        if userGoal['Departure place'] != '' and field['departure_place'].type != 'equals':
            return rewards['taskFailureReward']
        if userGoal['Departure place'] != '' and userGoal['Departure place'] != field['departure_place'].equals:
            return rewards['taskFailureReward']
        if userGoal['Arrival place'] == '' and field['arrival_place'].type == 'equals':
            return rewards['taskFailureReward']
        if userGoal['Arrival place'] != '' and field['arrival_place'].type != 'equals':
            return rewards['taskFailureReward']
        if userGoal['Arrival place'] != '' and userGoal['Arrival place'] != field['arrival_place'].equals:
            return rewards['taskFailureReward']
        if userGoal['Travel time'] == '' and field['travel_time'].type == 'equals':
            return rewards['taskFailureReward']
        if userGoal['Travel time'] != '' and field['travel_time'].type != 'equals':
            return rewards['taskFailureReward']
        if userGoal['Travel time'] != '' and userGoal['Travel time'] != field['travel_time'].equals:
            return rewards['taskFailureReward']
        return rewards['taskSuccessReward']
    else:
        return rewards['taskProceedReward']

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
    
def SimulateOneDialog(userSimulation,dialogManager,rewards,errorRate=0):
    '''
    Simulates one dialog.

      userSimulation is a Simulation.UserSimulation object

      asrSimulation is a Simulation.ASRSimulation object

      dialogManager is a DialogManager.* object

    Displays result on the "Transcript" logger
    '''
    
    userSimulation.Init(errorRate)
    systemAction = dialogManager.Init(userSimulation.goal)

    appLogger = logging.getLogger('Transcript')
    appLogger.info('------ Prior to start of dialog ------')
    appLogger.info('PartitionDistribution:\n%s' % (dialogManager.beliefState))

    dialogSuccess = False
    dialogReward = 0
    i = 0
    turns = []
    while(systemAction.type == 'ask'):
        appLogger.info('\n------ Turn %d ------' % (i+1))
        appLogger.info('User Goal: %s'%userSimulation.goal)
        appLogger.info('System Action: %s' % (systemAction))
        
        userAction = userSimulation.TakeTurn(systemAction)
        
        appLogger.info('User Action: %s' % (userAction))
#        asrResult = asrSimulation.SimASR(systemAction.grammar,userAction)
#        appLogger.info('** ASR Result: **\n%s' % (asrResult))
        
        reward = GetReward(rewards,userSimulation.goal,dialogManager.beliefState,systemAction)
        dialogReward += reward
        nextSystemAction = dialogManager.TakeTurn(userAction,reward)
        
        appLogger.info('** PartitionDistribution: **\n%s' % (dialogManager.beliefState))
        
        updateTime = dialogManager.beliefState.partitionDistribution.stats.clocks['mainUpdate']
        
#        appLogger.info('Update time: %f' % (updateTime))
        
        turns.append({
            'systemAction': systemAction,
            'userAction':userAction,
            'updateTime':updateTime,
        })
        
        systemAction = nextSystemAction
        
        if i >= rewards['taskSuccessReward']:
            break
        i += 1
    reward = GetReward(rewards,userSimulation.goal,dialogManager.beliefState,systemAction)
    dialogReward += reward
    dialogManager.TakeTurn(None,reward)
    if (systemAction.type == 'inform') and reward == rewards['taskSuccessReward']:
        dialogSuccess = True
    dialogSubSuccess = GetSubSuccess(userSimulation.goal,dialogManager.beliefState,systemAction)
    appLogger.info('\n------ Turn %d ------' % (i+1))
    appLogger.info('System Action: %s' % (systemAction))
    appLogger.info('User Goal: %s'%userSimulation.goal)
#    appLogger.info('Dialog %s'%('Success' if dialogManager.DialogResult()[0] else 'Fail'))
    appLogger.info('Dialog %s'%('Success' if dialogSuccess else 'Fail'))
    appLogger.info('Dialog %s in ignorance of route'%('Success' if dialogSubSuccess else 'Fail'))
    turns.append({
        'systemAction': systemAction,
        'userAction':None,
        'updateTime':None,
    })
    log = {
           'userGoal': userSimulation.goal,
           'turns' : turns,
#           'result': dialogManager.DialogResult()
           'result': (dialogSuccess,dialogReward),
           'subSuccess': dialogSubSuccess
           }
    return log

def main():
    InitConfig()
    config = GetConfig()
    config.read(['LGrl.conf'])
    
    rewards = {}
    rewards['taskSuccessReward'] = config.getint('DialogManager','taskSuccessReward')
    rewards['taskFailureReward'] = config.getint('DialogManager','taskFailureReward')
    rewards['taskProceedReward'] = config.getint('DialogManager','taskProceedReward')

#    InitDB()
    for testIndex in range(3):
        logging.config.fileConfig('logging.conf')
        if testIndex == 0:
            config.set('DialogManager','confidenceScoreCalibration','true')
            config.set('BeliefState','useLearnedUserModel','true')
            config.set('BeliefState','confirmUnlikelyDiscountFactor','0.1')
            config.set('PartitionDistribution','offListBeliefUpdateMethod','unlikelihood')
        elif testIndex == 1:
            config.set('DialogManager','confidenceScoreCalibration','true')
            config.set('BeliefState','useLearnedUserModel','true')
            config.set('BeliefState','confirmUnlikelyDiscountFactor','1.0')
            config.set('PartitionDistribution','offListBeliefUpdateMethod','unlikelihood')
        elif testIndex == 2:
            config.set('DialogManager','confidenceScoreCalibration','false')
            config.set('BeliefState','useLearnedUserModel','false')
            config.set('BeliefState','confirmUnlikelyDiscountFactor','0.1')
            config.set('PartitionDistribution','offListBeliefUpdateMethod','plain')
#        elif testIndex == 2:
#            config.set('DialogManager','confidenceScoreCalibration','false')
#            config.set('BeliefState','useLearnedUserModel','true')
#            config.set('BeliefState','confirmUnlikelyDiscountFactor','1.0')
#        elif testIndex == 3:
#            config.set('DialogManager','confidenceScoreCalibration','false')
#            config.set('BeliefState','useLearnedUserModel','false')
#            config.set('BeliefState','confirmUnlikelyDiscountFactor','1.0')
            
        dialogManager = DialogManager()
    #    dialogManager = DialogManager(confidenceScoreCalibration=None,useLearnedUserModel=None,confirmUnlikelyDiscountFactor=None)
        userSimulation = UserSimulation()
    #    asrSimulation = ASRSimulation()
        iter = 500
        interval = 10
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
        
        startTime = dt.datetime.now()
        intervalStartTime = dt.datetime.now()
        for i in range(iter):
            appLogger = logging.getLogger('Transcript')
            appLogger.info('Dialog %d'%i)
            
            errorRate = i/(iter/1)
            appLogger.info('Error rate %d'%errorRate)
    
            log = SimulateOneDialog(userSimulation,dialogManager,rewards,errorRate)
            
            totalDialogReward.append(log['result'][1])
            intervalDialogReward.append(log['result'][1])
            totalDialogLength.append(len(log['turns']))
            intervalDialogLength.append(len(log['turns']))
            
            if log['result'][0]: 
                totalDialogSuccessCount += 1
                intervalDialogSuccessCount += 1
            if log['subSuccess']: 
                totalDialogSubSuccessCount += 1
                intervalDialogSubSuccessCount += 1
            if (i+1) % (iter/interval) == 0:
                intervalElapsedTime.append(str(dt.datetime.now() - intervalStartTime))
                appLogger.info('Interval elapsed time: %s'%intervalElapsedTime[-1])
    
                intervalAvgDialogLength.append(float(sum(intervalDialogLength))/(float(iter)/interval))
                intervalDialogLength = []
                appLogger.info('Interval average dialog length: %f'%intervalAvgDialogLength[-1])
                
                totalAvgDialogLength.append(float(sum(totalDialogLength))/(i+1))
                appLogger.info('Cumulative average dialog length: %f'%totalAvgDialogLength[-1])
                
                intervalAvgDialogReward.append(float(sum(intervalDialogReward))/(float(iter)/interval))
                intervalDialogReward = []
                appLogger.info('Interval average dialog reward: %f'%intervalAvgDialogReward[-1])
                
                totalAvgDialogReward.append(float(sum(totalDialogReward))/(i+1))
                appLogger.info('Cumulative average dialog reward: %f'%totalAvgDialogReward[-1])
                
                intervalDialogSuccessRate.append(float(intervalDialogSuccessCount)/(float(iter)/interval))
                intervalDialogSuccessCount = 0
                appLogger.info('Interval dialog success rate: %f'%intervalDialogSuccessRate[-1])
                
                totalDialogSuccessRate.append(float(totalDialogSuccessCount)/(i+1))
                appLogger.info('Cumulative dialog success rate: %f'%totalDialogSuccessRate[-1])
                
                intervalDialogSubSuccessRate.append(float(intervalDialogSubSuccessCount)/(float(iter)/interval))
                intervalDialogSubSuccessCount = 0
                appLogger.info('Interval dialog success rate in ignorance of route: %f'%intervalDialogSubSuccessRate[-1])
                
                totalDialogSubSuccessRate.append(float(totalDialogSubSuccessCount)/(i+1))
                appLogger.info('Cumulative dialog success rate in ignorance of route: %f'%totalDialogSubSuccessRate[-1])
                intervalStartTime = dt.datetime.now()
                
#            if (i+1) % (iter/1) == 0:
#                dialogManager.StoreModel('%d'%errorRate)
    
        endTime = dt.datetime.now()
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
    
        appLogger.info('Interval elapsed times: %s'%str(intervalElapsedTime))
        appLogger.info('Start time: %s'%startTime.isoformat(' '))
        appLogger.info('End time: %s'%endTime.isoformat(' '))
        appLogger.info('Total elapsed time: %s'%(endTime - startTime))
        
        logging.shutdown()
        try:
            os.remove('run-%d.log'%testIndex)
        except:
            pass
        os.rename('run.log','run-%d.log'%testIndex)
        
if (__name__ == '__main__'):
    main()
