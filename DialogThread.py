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
        self.turn_number = 0
        self.id_suffix = 0
        self.utt_count = 0
        self.dialog_state_index = 0
        self.dialog_state = initDialogState
        self.stack = initStack
        self.agenda = initAgenda
        self.lineConfig = initLineConfig
        self.floor = 'system'
        self.inQueue = inQueue
        self.outQueue = outQueue
        self.dialogManager = DialogManager()
        self.systemUtteranceList = []

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
                message = {'type':'GALAXYACTIONCALL',
                           'content':introMessage%(self.turn_number,\
                                                ' '.join(self.systemUtteranceList),\
                                                self.dialog_state,\
                                                self.stack,\
                                                self.agenda,\
                                                self.lineConfig,\
                                                self.dialog_state_index,\
                                                self.floor,\
                                                self.sessionID,\
                                                self.id_suffix,\
                                                "welcome",\
                                                self.utt_count)}
                self.systemUtteranceList.append(str(self.utt_count))
                self.id_suffix += 1
                self.utt_count += 1
                self.outQueue.put(message)
                
                message = {'type':'GALAXYACTIONCALL',
                           'content':introMessage%(self.turn_number,\
                                                ' '.join(self.systemUtteranceList),\
                                                self.dialog_state,\
                                                self.stack,\
                                                self.agenda,\
                                                self.lineConfig,\
                                                self.dialog_state_index,\
                                                self.floor,\
                                                self.sessionID,\
                                                self.id_suffix,\
                                                "how_to_get_help",\
                                                self.utt_count)}
                self.systemUtteranceList.append(str(self.utt_count))
                self.id_suffix += 1
                self.utt_count += 1
                self.outQueue.put(message)
                
            elif frame.name == 'handle_event':
                eventType = frame[':event_type']
                
                if eventType == 'user_utterance_end':
                    self.appLogger.info('user_utterance_end')

                    if not self.dialogManager.Initialized():
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

                    systemAction = self.dialogManager.TakeTurn(asrResult)

                    if systemAction.type == 'ask' and systemAction.force == 'request':
                        message = {'type':'GALAXYACTIONCALL',
                                   'content':systemRequest%(self.turn_number,\
                                                        ' '.join(self.systemUtteranceList),\
                                                        self.dialog_state,\
                                                        self.stack,\
                                                        self.agenda,\
                                                        self.lineConfig,\
                                                        self.dialog_state_index,\
                                                        self.floor,\
                                                        self.sessionID,\
                                                        self.id_suffix,\
                                                        "how_to_get_help",\
                                                        self.utt_count)}
                    elif systemAction.type == 'ask' and systemAction.force == 'confirm':
                        message = {'type':'GALAXYACTIONCALL',
                                   'content':systemConfirm%(self.turn_number,\
                                                        ' '.join(self.systemUtteranceList),\
                                                        self.dialog_state,\
                                                        self.stack,\
                                                        self.agenda,\
                                                        self.dialog_state_index,\
                                                        self.floor,\
                                                        self.sessionID,\
                                                        self.id_suffix,\
                                                        "how_to_get_help",\
                                                        self.utt_count)}
                    self.systemUtteranceList.append(str(self.utt_count))
                    self.id_suffix += 1
                    self.utt_count += 1
                    self.outQueue.put(message)
                    self.turn_number += 1
                    
                elif eventType == 'system_utterance_start':
                    self.appLogger.info('system_utterance_start(%s) %s'%(frame[':properties'][':utt_count'],\
                                                                         frame[':properties'][':tagged_prompt']))
                    
                elif eventType == 'system_utterance_end':
                    self.appLogger.info('system_utterance_end(%s)'%frame[':properties'][':utt_count'])
                    self.systemUtteranceList.pop(frame[':properties'][':utt_count'])
                    if self.utt_count < 2 and self.systemUtteranceList == []: 
                        self.systemAction = self.dialogManager.Init()
                        message = {'type':'GALAXYACTIONCALL',
                                   'content':systemRequest%(self.turn_number,\
                                                        ' '.join(self.systemUtteranceList),\
                                                        self.dialog_state,\
                                                        self.stack,\
                                                        self.agenda,\
                                                        self.lineConfig,\
                                                        self.dialog_state_index,\
                                                        self.floor,\
                                                        self.sessionID,\
                                                        self.id_suffix,\
                                                        "how_to_get_help",\
                                                        self.utt_count)}
                        self.systemUtteranceList.append(str(self.utt_count))
                        self.id_suffix += 1
                        self.utt_count += 1
                        self.outQueue.put(message)
                    
                elif eventType == 'dialog_state_change':
                    self.appLogger.info('dialog_state_change')
                    # update dialog state
                    self.dialog_state_index += 1
                    # broadcast dialog state
                    
                elif eventType == 'turn_timeout':
                    self.appLogger.info('turn_timeout')
                    self.id_suffix += 1
                    asrResult = ASRResult.FromHelios([userAction('non-understanding')],[1.0])
                    systemAction = self.dialogManager.TakeTurn(asrResult)
                    if systemAction.type == 'ask' and systemAction.force == 'confirm':
                        message = {'type':'GALAXYACTIONCALL',
                                   'content':systemRequest%(self.turn_number,\
                                                        ' '.join(self.systemUtteranceList),\
                                                        self.dialog_state,\
                                                        self.stack,\
                                                        self.agenda,\
                                                        self.lineConfig,\
                                                        self.dialog_state_index,\
                                                        self.floor,\
                                                        self.sessionID,\
                                                        self.id_suffix,\
                                                        "how_to_get_help",\
                                                        self.utt_count)}
                        self.systemUtteranceList.append(str(self.utt_count))
                        self.id_suffix += 1
                        self.utt_count += 1
                        self.outQueue.put(message)
                else:
                    self.appLogger.info(eventType)

            elif frame.name == 'end_session':
                self.appLogger.info('end_session')
                
            
