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
import os, sys
#sys.path.append(os.path.join(os.path.dirname(__file__),'../../src'))

import logging.config
import logging
from GlobalConfig import *
from BeliefState import BeliefState
from UserSimulation import UserSimulation
from DB import InitDB
#from DialogManager import OpenDialogManager as DialogManager
from DialogManager import SBSarsaDialogManager as DialogManager

def SimulateOneDialog(userSimulation,dialogManager):
    '''
    Simulates one dialog.

      userSimulation is a Simulation.UserSimulation object

      asrSimulation is a Simulation.ASRSimulation object

      dialogManager is a DialogManager.* object

    Displays result on the "Transcript" logger
    '''
    
    userSimulation.Init()
    systemAction = dialogManager.Init(userSimulation.goal)

    appLogger = logging.getLogger('Transcript')
    appLogger.info('------ Prior to start of dialog ------')
    appLogger.info('PartitionDistribution:\n%s' % (dialogManager.beliefState))
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
        
        nextSystemAction = dialogManager.TakeTurn(userAction)
        
        appLogger.info('** PartitionDistribution: **\n%s' % (dialogManager.beliefState))
        
        updateTime = dialogManager.beliefState.partitionDistribution.stats.clocks['mainUpdate']
        
#        appLogger.info('Update time: %f' % (updateTime))
        
        turns.append({
            'systemAction': systemAction,
            'userAction':userAction,
            'updateTime':updateTime,
        })
        
        systemAction = nextSystemAction
        
        if i > 30:
            break
        i += 1
    appLogger.info('\n------ Turn %d ------' % (i+1))
    appLogger.info('System Action: %s' % (systemAction))
    appLogger.info('User Goal: %s'%userSimulation.goal)
    appLogger.info('Dialog %s'%('Success' if dialogManager.DialogResult() else 'Fail'))
    turns.append({
        'systemAction': systemAction,
        'userAction':None,
        'updateTime':None,
    })
    log = {
           'userGoal': userSimulation.goal,
           'turns' : turns,
           'result': dialogManager.DialogResult()
           }
    return log

def main():
    InitConfig()
    config = GetConfig()
    config.read(['LGrl.conf'])
    logging.config.fileConfig('logging.conf')
#    InitDB()
    dialogManager = DialogManager()
    userSimulation = UserSimulation()
#    asrSimulation = ASRSimulation()
    totalDialogSuccessCount = 0
    for i in range(100):
        appLogger = logging.getLogger('Transcript')
        appLogger.info('Dialog %d'%i)
        log = SimulateOneDialog(userSimulation,dialogManager)
        if log['result']: totalDialogSuccessCount += 1
    
    appLogger.info('Dialog success count: %d'%totalDialogSuccessCount)

if (__name__ == '__main__'):
    main()
