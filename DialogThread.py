'''

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
        self.turnNumber = 0
        self.idSuffix = 0
        self.uttCount = 0
        self.dialogStateIndex = 0
        self.dialogState = 'initial'
        self.floorStatus = 'system'
        self.notifyPrompts = []
        self.systemAction = None
        self.newDialogState = None
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
            
    def _GetNewDialogState(self):
        if not self.systemAction:
            self.newDialogState = 'inform_welcome'
        elif self.systemAction.type == 'ask' and self.systemAction.force == 'request':
            if self.systemAction.content == 'all':
                self.newDialogState = 'request_all'
            elif self.systemAction.content == 'departure_place':
                self.newDialogState = 'request_departure_place'
            elif self.systemAction.content == 'arrival_place':
                self.newDialogState = 'request_arrival_place'
            elif self.systemAction.content == 'travel_time':
                self.newDialogState = 'request_travel_time'
        elif self.systemAction.type == 'ask' and self.systemAction.force == 'confirm':
            if 'route' in self.systemAction.content:
                self.newDialogState = 'confirm_route'
            elif 'departure_place' in self.systemAction.content:
                self.newDialogState = 'confirm_departure_place'
            elif 'arrival_place' in self.systemAction.content:
                self.newDialogState = 'confirm_arrival_place'
            elif 'travel_time' in self.systemAction.content:
                self.newDialogState = 'confirm_travel_time'
        elif self.systemAction.type == 'inform':
            if self.systemAction.force == 'confirm_okay':
                self.newDialogState = 'inform_confirm_okay'
            elif self.systemAction.force == 'processing':
                self.newDialogState = 'inform_processing'
            elif self.systemAction.force == 'success':
                self.newDialogState = 'inform_success'
            elif self.systemAction.force == 'subsequent_processing':
                self.newDialogState = 'inform_subsequent_processing'
            elif self.systemAction.force == 'starting_new_query':
                self.newDialogState = 'inform_starting_new_query'
        
    def run(self):
        while True:
            self.appLogger.info('Wait event')
            frame = self.inQueue.get()
            self.inQueue.task_done()
            self.appLogger.info('Frame:\n%s'%frame.PPrint())
            
            if frame.name == 'begin_session':
                self.appLogger.info('begin_session')
                message = MakeSystemUtterance('inform_welcome',self.dialogState,self.turnNumber,\
                                              ' '.join(self.notifyPrompts),self.dialogStateIndex,\
                                              self.sessionID,self.idSuffix,self.uttCount)
#                self.appLogger.info('message:\n%s'%message)

                self.notifyPrompts.append(str(self.uttCount))
                self.idSuffix += 1
                self.uttCount += 1
                self.outQueue.put(message)
                
#                message = MakeSystemUtterance('inform_how_to_get_help',self.dialogState,self.turnNumber,\
#                                              ' '.join(self.notifyPrompts),self.dialogStateIndex,\
#                                              self.sessionID,self.idSuffix,self.uttCount)
#                self.notifyPrompts.append(str(self.uttCount))
#                self.idSuffix += 1
#                self.uttCount += 1
#                self.outQueue.put(message)
                
#                message = {'type':'WAITINTERACTIONEVENT'}
#                self.outQueue.put(message)
                
            elif frame.name == 'DialogManager.handle_event':
                eventType = frame[':event_type']
                self.appLogger.info('event_type: %s'%eventType)
                
                if eventType == 'user_utterance_end':
                    self.appLogger.info('user_utterance_end')

                    if not self.systemAction:
                        self.systemAction = self.dialogManager.Init(True)

                    userAction = UserAction('ig',{})

                    if frame[':properties'][':top_slots'] == '1_SinglePlace':
                        hypothesis = frame[':properties'][':hypothesis']
                        if self.systemAction.type == 'ask' and self.systemAction.force == 'request':
                            if self.systemAction.content == 'departure_place':
                                userAction.update({'departure_place':hypothesis})
                            elif self.systemAction.content == 'arrival_place':
                                userAction.update({'arrival_place':hypothesis})
                        else:
                            userAction.update({'departure_place':hypothesis,'arrival_place':hypothesis})

                    userActions = [userAction]
                    probs = [float(frame[':properties'][':confidence'])]
                    asrResult = ASRResult.FromHelios(userActions,probs)

                    self.systemAction = self.dialogManager.TakeTurn(asrResult)
                    self._GetNewDialogState()
                    message = MakeSystemUtterance(self.newDialogState,self.dialogState,self.turnNumber,\
                                                  ' '.join(self.notifyPrompts),self.dialogStateIndex,\
                                                  self.sessionID,self.idSuffix,self.uttCount)
                    self.notifyPrompts.append(str(self.uttCount))
                    self.idSuffix += 1
                    self.uttCount += 1
                    self.outQueue.put(message)
                    self.turnNumber += 1
                    
                elif eventType == 'system_utterance_start':
                    self.appLogger.info('system_utterance_start(%s) %s'%(frame[':properties'][':utt_count'],\
                                                                         frame[':properties'][':tagged_prompt']))
                    message = {'type':'WAITINTERACTIONEVENT'}
                    self.outQueue.put(message)
                    
                elif eventType == 'system_utterance_end':
                    self.appLogger.info('system_utterance_end(%s)'%frame[':properties'][':utt_count'])
                    self.appLogger.info('notifyPrompts: [ %s ]'%', '.join(self.notifyPrompts))
                    self.notifyPrompts.remove(frame[':properties'][':utt_count'])
                    self.appLogger.info('notifyPrompts: [ %s ]'%', '.join(self.notifyPrompts))
                    if self.uttCount == 1 and self.notifyPrompts == []: 
                        self.systemAction = self.dialogManager.Init()
                        self._GetNewDialogState()
                        message = MakeSystemUtterance(self.newDialogState,self.dialogState,self.turnNumber,\
                                                      ' '.join(self.notifyPrompts),self.dialogStateIndex,\
                                                      self.sessionID,self.idSuffix,self.uttCount)
                        self.notifyPrompts.append(str(self.uttCount))
                        self.idSuffix += 1
                        self.uttCount += 1
                        self.outQueue.put(message)
                    else:
                        message = {'type':'WAITINTERACTIONEVENT'}
                        self.outQueue.put(message)

                elif eventType == 'dialog_state_change':
                    self.appLogger.info('dialog_state_change')
                    # update dialog state
                    self.dialogState = 'initial' if not self.newDialogState else self.newDialogState
                    self.dialogStateIndex += 1
                    # broadcast dialog state
                    message = MakeDialogStateMessage(self.dialogState,self.turnNumber,\
                                                  ' '.join(self.notifyPrompts))
                    self.outQueue.put(message)

                elif eventType == 'turn_timeout':
                    self.appLogger.info('turn_timeout')
                    self.idSuffix += 1
                    asrResult = ASRResult.FromHelios([userAction('non-understanding')],[1.0])
                    self.systemAction = self.dialogManager.TakeTurn(asrResult)
                    self._GetNewDialogState()
                    message = MakeSystemUtterance(self.newDialogState,self.dialogState,self.turnNumber,\
                                                  ' '.join(self.notifyPrompts),self.dialogStateIndex,\
                                                  self.sessionID,self.idSuffix,self.uttCount)
                    self.notifyPrompts.append(str(self.uttCount))
                    self.idSuffix += 1
                    self.uttCount += 1
                    self.outQueue.put(message)
                else:
                    self.appLogger.info(eventType)

            elif frame.name == 'end_session':
                self.appLogger.info('end_session')
                
            
