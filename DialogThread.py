'''

'''

import logging.config
import logging
import threading
import Queue
from GlobalConfig import *
#from DialogManager import SBSarsaDialogManager as DialogManager
from DialogManager import OpenDialogManager as DialogManager
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
        self.departurePlaceTypeDict = {}
        self.arrivalPlaceTypeDict = {}
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
                                              self.sessionID,self.idSuffix,self.uttCount,'','','')
                self.notifyPrompts.append(str(self.uttCount))
                self.idSuffix += 1
                self.uttCount += 1
                self.outQueue.put(message)
                self.inQueue.get()
                self.inQueue.task_done()
                
                message = MakeSystemUtterance('inform_how_to_get_help',self.dialogState,self.turnNumber,\
                                              ' '.join(self.notifyPrompts),self.dialogStateIndex,\
                                              self.sessionID,self.idSuffix,self.uttCount,'','','')
                self.notifyPrompts.append(str(self.uttCount))
                self.idSuffix += 1
                self.uttCount += 1
                self.outQueue.put(message)
                self.inQueue.get()
                self.inQueue.task_done()
                
                message = {'type':'WAITINTERACTIONEVENT'}
                self.outQueue.put(message)
                
            elif frame.name == 'DialogManager.handle_event':
                eventType = frame[':event_type']
                self.appLogger.info('event_type: %s'%eventType)
                
                if eventType == 'user_utterance_end':
                    self.appLogger.info('user_utterance_end')

                    if not self.systemAction:
                        self.systemAction = self.dialogManager.Init(True)

                    self.appLogger.info('Previous system action: %s'%str(self.systemAction))

                    userAction = UserAction('ig',{})

                    self.appLogger.info('top_slots: %s'%frame[':properties'][':top_slots'])
                    self.appLogger.info('hypothesis: %s'%frame[':properties'][':hypothesis'])
                    self.appLogger.info('confidence: %s'%frame[':properties'][':confidence'])
                    
                    updateDeparturePlaceType = updateArrivalPlaceType = False
                    if frame[':properties'][':top_slots'] == '1_SinglePlace':
                        hypothesis = frame[':properties'][':hypothesis']
                        if self.systemAction.type == 'ask' and self.systemAction.force == 'request':
                            if self.systemAction.content == 'departure_place':
                                userAction.content.update({'departure_place':hypothesis})
                                updateDeparturePlaceType = True
                            elif self.systemAction.content == 'arrival_place':
                                userAction.content.update({'arrival_place':hypothesis})
                                updateArrivalPlaceType = True
                            else:
                                userAction.content.update({'departure_place':hypothesis,'arrival_place':hypothesis})
                                updateDeparturePlaceType = True
                                updateArrivalPlaceType = True
                        else:
                            userAction.content.update({'departure_place':hypothesis,'arrival_place':hypothesis})
                            updateDeparturePlaceType = True
                            updateArrivalPlaceType = True
                    elif frame[':properties'][':top_slots'] == '4_DateTime':
                        hypothesis = frame[':properties'][':hypothesis']
                        userAction.content.update({'travel_time':hypothesis})
                        message = MakeParseDateTimeMessage(frame[':properties'][':gal_slotsframe'])
                        self.outQueue.put(message)
                        result = self.inQueue.get()
                        self.inQueue.task_done()
                        self.appLogger.info('%s'%result)
                    elif frame[':properties'][':top_slots'] == 'Generic':
                        hypothesis = frame[':properties'][':hypothesis']
                        userAction.content.update({'confirm':hypothesis})
                    elif frame[':properties'][':top_slots'] == '0_BusNumber':
                        hypothesis = frame[':properties'][':hypothesis']
                        userAction.content.update({'route':hypothesis})

                    if frame[':properties'][':parse_str'].find('covered_neighborhood') > -1 or \
                    frame[':properties'][':parse_str'].find('uncovered_neighborhood') > -1 or \
                    frame[':properties'][':parse_str'].find('ambiguous_covered_place') > -1 or \
                    frame[':properties'][':parse_str'].find('ambiguous_uncovered_place') > -1:
                        if updateDeparturePlaceType:
                            self.departurePlaceTypeDict[hypothesis] = 'neighborhood'
                        if updateArrivalPlaceType:                        
                            self.arrivalPlaceTypeDict[hypothesis] = 'neighborhood'
                    else:                        
                        if updateDeparturePlaceType:
                            self.departurePlaceTypeDict[hypothesis] = 'stop'
                        if updateArrivalPlaceType:                        
                            self.arrivalPlaceTypeDict[hypothesis] = 'stop'

                    self.appLogger.info('userAction: %s'%str(userAction))

                    userActions = [userAction]
                    probs = [float(frame[':properties'][':confidence'])]
                    asrResult = ASRResult.FromHelios(userActions,probs)

                    self.appLogger.info('ASRResult: %s'%str(asrResult))

                    self.systemAction = self.dialogManager.TakeTurn(asrResult)
                    self.appLogger.info('System action: %s'%str(self.systemAction))

                    query = result = version = ''
                    if self.systemAction.type == 'inform':
                        # inform processing
                        self.systemAction.force = 'processing'
                        self._GetNewDialogState()
                        self.appLogger.info('New dialog state: %s'%self.newDialogState)
                        message = MakeSystemUtterance(self.newDialogState,self.dialogState,self.turnNumber,\
                                                      ' '.join(self.notifyPrompts),self.dialogStateIndex,\
                                                      self.sessionID,self.idSuffix,self.uttCount,\
                                                      query,result,version)
                        self.notifyPrompts.append(str(self.uttCount))
                        self.idSuffix += 1
                        self.uttCount += 1
                        self.outQueue.put(message)
                        self.inQueue.get()
                        self.inQueue.task_done()

                        # Backend lookup
#                        querySpec = {'departure_place':'',\
#                                'arrival_place':'',\
#                                'travel_time':'',\
#                                'route':'',\
#                                'month':'12',\
#                                'day':'9',\
#                                'year':'2011',\
#                                'weekday':'5',\
#                                'period_spec':'now',\
#                                'value':'1421',\
#                                'now':'true',\
#                                'time_type':'departure',\
#                                'departure_place_type':'stop',\
#                                'arrival_place_type':'stop',\
#                                'departure_stops':'',\
#                                'arrival_stops':''}
                        querySpec,belief = self.dialogManager.beliefState.GetTopUniqueUserGoal()
                        querySpec['departure_place_type'] = self.departurePlaceTypeDict[querySpec['departure_place']]
                        querySpec['arrival_place_type'] = self.arrivalPlaceTypeDict[querySpec['arrival_place']]
                        
                        message = MakeDeparturePlaceQuery(querySpec)
                        self.outQueue.put(message)
                        result = self.inQueue.get()
                        self.inQueue.task_done()
#                        if result:
#                        
#                        querySpec['now'] =
#                        querySpec['value'] =
#                        querySpec['period_spec'] =
#                        querySpec['weekday'] =
#                        querySpec['year'] =
#                        querySpec['day'] =
#                        querySpec['month'] =
#                        querySpec['time_type'] = 'departure'
                        
                        message = MakeDeparturePlaceQuery(querySpec)
                        self.outQueue.put(message)
                        result = self.inQueue.get()
                        self.inQueue.task_done()
                        if result:
                            querySpec['departure_stops'] = result[':outframe']
                        else:
                            self.appLogger.info('Backend query for place failed')
                        message = MakeArrivalPlaceQuery(querySpec)
                        self.outQueue.put(message)
                        result = self.inQueue.get()
                        self.inQueue.task_done()
                        if result:
                            querySpec['arrival_stops'] = result[':outframe']
                        else:
                            self.appLogger.info('Backend query for place failed')
        
                        message = MakeScheduleQuery(querySpec)
                        self.outQueue.put(message)
                        result = self.inQueue.get()
                        self.inQueue.task_done()
                        if result:
                            self.appLogger.info('Bus schedule: %s'%result)
                        else:
                            self.appLogger.info('Backend query for schedule failed')
        
                       
                        # inform success or failure
                        self.systemAction.force = 'inform'
                        self.systemAction.force = 'success'
                        self._GetNewDialogState()
                        self.appLogger.info('New dialog state: %s'%self.newDialogState)
                        message = MakeSystemUtterance(self.newDialogState,self.dialogState,self.turnNumber,\
                                                      ' '.join(self.notifyPrompts),self.dialogStateIndex,\
                                                      self.sessionID,self.idSuffix,self.uttCount,\
                                                      query,result,version)
                        self.notifyPrompts.append(str(self.uttCount))
                        self.idSuffix += 1
                        self.uttCount += 1
                        self.outQueue.put(message)
                        self.inQueue.get()
                        self.inQueue.task_done()
                        
                        # request next query
                        query = result = ''
                        self.systemAction.force = 'request'
                        self.systemAction.force = 'starting_new_query'
                        self._GetNewDialogState()
                        self.appLogger.info('New dialog state: %s'%self.newDialogState)
                        message = MakeSystemUtterance(self.newDialogState,self.dialogState,self.turnNumber,\
                                                      ' '.join(self.notifyPrompts),self.dialogStateIndex,\
                                                      self.sessionID,self.idSuffix,self.uttCount,\
                                                      query,result,version)
                        self.notifyPrompts.append(str(self.uttCount))
                        self.idSuffix += 1
                        self.uttCount += 1
                        self.outQueue.put(message)
                        self.inQueue.get()
                        self.inQueue.task_done()
                    elif self.systemAction.type == 'ask' and self.systemAction.force == 'confirm':
                        if 'departure_place' in self.systemAction.content:
                            query = 'query.departure_place\t{\nname\t%s\ntype\tstop\n}\n'%self.systemAction.content['departure_place']
                        elif 'arrival_place' in self.systemAction.content:
                            query = 'query.arrival_place\t{\nname\t%s\ntype\tneighborhood\n}\n'%self.systemAction.content['arrival_place']
                        elif 'travel_time' in self.systemAction.content:
                            query = 'query.travel_time.time\t{\nvalue\t1421\nnow\ttrue\ntype\tdeparture\n}\n'
                        elif 'route' in self.systemAction.content:
                            query = 'query.route_number\t%s\n'%self.systemAction.content['route']
                    self._GetNewDialogState()
                    self.appLogger.info('New dialog state: %s'%self.newDialogState)
                    message = MakeSystemUtterance(self.newDialogState,self.dialogState,self.turnNumber,\
                                                  ' '.join(self.notifyPrompts),self.dialogStateIndex,\
                                                  self.sessionID,self.idSuffix,self.uttCount,\
                                                  query,result,version)
                    self.notifyPrompts.append(str(self.uttCount))
                    self.idSuffix += 1
                    self.uttCount += 1
                    self.turnNumber += 1
                    self.outQueue.put(message)
                    self.inQueue.get()
                    self.inQueue.task_done()

                    message = {'type':'WAITINTERACTIONEVENT'}
                    self.outQueue.put(message)
                    
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
                    if self.uttCount == 2 and self.notifyPrompts == []: 
#                    if self.uttCount == 1 and self.notifyPrompts == []: 
                        self.systemAction = self.dialogManager.Init()
                        self._GetNewDialogState()
                        message = MakeSystemUtterance(self.newDialogState,self.dialogState,self.turnNumber,\
                                                      ' '.join(self.notifyPrompts),self.dialogStateIndex,\
                                                      self.sessionID,self.idSuffix,self.uttCount,'','','')
                        self.notifyPrompts.append(str(self.uttCount))
                        self.idSuffix += 1
                        self.uttCount += 1
                        self.outQueue.put(message)
                        self.inQueue.get()
                        self.inQueue.task_done()

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
                    self.inQueue.get()
                    self.inQueue.task_done()

                    message = {'type':'WAITINTERACTIONEVENT'}
                    self.outQueue.put(message)

                elif eventType == 'turn_timeout':
                    self.appLogger.info('turn_timeout')
                    self.idSuffix += 1

                    asrResult = ASRResult.FromHelios([userAction('non-understanding',{})],[1.0])
                    self.appLogger.info('ASRResult: %s'%str(asrResult))

                    self.systemAction = self.dialogManager.TakeTurn(asrResult)
                    self.appLogger.info('System action: %s'%str(self.systemAction))

                    self.appLogger.info('** PartitionDistribution: **\n%s'%(self.dialogManager.beliefState))
                    
                    self._GetNewDialogState()
                    self.appLogger.info('New dialog state: %s'%self.newDialogState)

                    query = result = version = ''
                    message = MakeSystemUtterance(self.newDialogState,self.dialogState,self.turnNumber,\
                                                  ' '.join(self.notifyPrompts),self.dialogStateIndex,\
                                                  self.sessionID,self.idSuffix,self.uttCount,\
                                                  query,result,version)
                    self.notifyPrompts.append(str(self.uttCount))
                    self.idSuffix += 1
                    self.uttCount += 1
                    self.outQueue.put(message)
                    self.inQueue.get()
                    self.inQueue.task_done()

                    message = {'type':'WAITINTERACTIONEVENT'}
                    self.outQueue.put(message)

                else:
                    self.appLogger.info(eventType)

                    message = {'type':'WAITINTERACTIONEVENT'}
                    self.outQueue.put(message)

            elif frame.name == 'end_session':
                self.appLogger.info('end_session')
                
            
