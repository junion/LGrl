'''
Illustration of a mixed initiative name dialer with
100k names.

To run this dialog manager, see httpd.py

Part of the AT&T Statistical Dialog Toolkit (ASDT).

Jason D. Williams
jdw@research.att.com
www.research.att.com/people/Williams_Jason_D
'''

import logging.config
import logging
import threading
import Queue
from GlobalConfig import *
from DialogManager import SBSarsaDialogManager as DialogManager
from GalaxyFrames import *
from DialogModules import UserAction,ASRResult
    
class DialogThread(threading.Thread):
    def __init__(self,sessionID,inQueue,outQueue):
        threading.Thread.__init__(self)

        logging.config.fileConfig('E:/Development/LGrl-G/logging.conf')
        self.appLogger = logging.getLogger('DialogThread')
#        self.appLogger.info('DialogThread init')
        self.sessionID = sessionID
        self.msg_idx = 0
        self.utt_count = 0
        self.inQueue = inQueue
        self.outQueue = outQueue
        self.dialogManager = DialogManager()

        self.appLogger.info('Dialog thread %s created'%self.getName())

    def _MapInputToUserAction(self,frame):
        '''
        Example
            userAction = UserAction('non-understanding')
            userAction = UserAction('ig',{'route':'28X','confirm':'NO'})
        '''
        userActionHyps = [UserAction('ig',{'route':'28X','confirm':'NO'})]
        probs = [0.9]
        correctPosition = 0
        return ASRResult.Simulated(None,userActionHyps,probs,correctPosition=correctPosition)
            
    def run(self):
        while True:
            frame = self.inQueue.get()
            self.inQueue.task_done()
            
            if frame.name == 'begin_session':
                systemAction = self.dialogManager.Init()
                message = {'type':'GALAXYACTIONCALL',
                           'data':introMessage%(self.sessionID,self.msg_idx,"welcome",self.utt_count)}
                self.outQueue.put(message)
#                message = {'type':'GALAXYACTIONCALL',
#                           'data':intro%(self.sessionID,self.msg_idx,"how_to_get_help",self.utt_count)}
#                self.outQueue.put(message)
                message = {'type':'GALAXYCALL',
                           'data':systemUtterance%(self.sessionID,self.msg_idx,"welcome",self.utt_count)}
                self.outQueue.put(message)
            elif frame.name == 'handle_event':
                if frame == 'user_utterance_end':
                    self.appLogger.info('user_utterance_end')
                    # userAction = frame
#                    systemAction = self.dialogManager.TakeTurn(userAction)  
#                    message = {'type':'GALAXYCALL',
#                           'data':systemUtterance%(self.sessionID,self.msg_idx,"welcome",self.utt_count)}
#                    self.outQueue.put(message)  
                    # broadcast dialog state
                elif frame == 'system_utterance_start':
                    self.appLogger.info('system_utterance_start')
                    # broadcast dialog state
                elif frame == 'system_utterance_end':
                    self.appLogger.info('system_utterance_end')
                    self.utt_count += 1
                    # broadcast dialog state
                elif frame == 'timeout':
                    self.appLogger.info('timeout')
                    # broadcast dialog state
            elif frame.name == 'end_session':
                self.appLogger.info('end_session')
                
            
