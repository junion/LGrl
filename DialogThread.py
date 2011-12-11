'''

'''

import logging.config
import logging
import threading
import Queue
from datetime import datetime
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
        self.timeSpecDict = {}
        self.asrResult = None
        self.taskQueue = []
        self.dialogManager = DialogManager()

        self.appLogger.info('Dialog thread %s created'%self.getName())

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

    def _BeginSessionHandler(self,frame):
        self.appLogger.info('begin_session')
                
    def _UserUtteranceEndHandler(self,frame):
        self.appLogger.info('user_utterance_end')

        self.appLogger.info('Previous system action: %s'%str(self.systemAction))

        userAction = UserAction('ig',{})

        self.appLogger.info('top_slots: %s'%frame[':properties'][':top_slots'])
        self.appLogger.info('hypothesis: %s'%frame[':properties'][':hypothesis'])
        self.appLogger.info('confidence: %s'%frame[':properties'][':confidence'])
        
        updateDeparturePlaceType = updateArrivalPlaceType = False
        if frame[':properties'].has_key(':[1_singleplace.stop_name]'):
            hypothesis = frame[':properties'][':[1_singleplace.stop_name]']
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
        if frame[':properties'].has_key(':[2_departureplace.stop_name]'):
            hypothesis = frame[':properties'][':[2_departureplace.stop_name]']
            userAction.content.update({'departure_place':hypothesis})
            updateDeparturePlaceType = True
        if frame[':properties'].has_key(':[3_arrivalplace.stop_name]'):
            hypothesis = frame[':properties'][':[3_arrivalplace.stop_name]']
            userAction.content.update({'arrival_place':hypothesis})
            updateArrivalPlaceType = True
        if frame[':properties'].has_key(':[4_datetime]'):
            message = MakeParseDateTimeMessage(frame[':properties'][':gal_slotsframe'])
            self.outQueue.put(message)
            result = self.inQueue.get()
            self.inQueue.task_done()
            self.appLogger.info('Timeinfo: %s'%result.PPrint())
            dateTime = {}
            if result[':valid_date'] == 'true':
                dateTime['weekday'] = result[':weekday']
                dateTime['year'] = result[':year']
                dateTime['day'] = result[':day']
                dateTime['month'] = result[':month']
            gotTime = False
            if result[':valid_time'] == 'true' and result[':start_time'] == result[':end_time'] and \
            result[':start_time'] != '' and result[':start_time'] != '1199':
                dtTime = int(result[':start_time'])
                self.appLogger.info('dtTime: %d'%dtTime)
                iTime = datetime.now(); iTime = iTime.hour*100 + iTime.minute
                self.appLogger.info('iTime: %d'%iTime)
                if dtTime >= 1200: dtTime -= 1200
                self.appLogger.info('dtTime: %d'%dtTime)
                if iTime < 1200:
                    if dtTime < iTime - 15: dtTime += 1200
                    self.appLogger.info('a dtTime: %d'%dtTime)
                else:
                    if dtTime >= iTime - 1215: dtTime += 1200
                    self.appLogger.info('b dtTime: %d'%dtTime)
                if result[':timeperiod_spec'] == 'now ':
                    dateTime['value'] = '%d'%dtTime
                    dateTime['now'] = 'true'
                elif result[':timeperiod_spec'] == '' and result[':day'] == '-1':
                    dateTime['value'] = '%d'%dtTime
                else:
                    dateTime['value'] = result[':start_time']
                gotTime = True   
            self.appLogger.info('2')
            if gotTime:   
                parse = frame[':properties'][':parse_str']
                if parse.find('[4_ArrivalTime]') > -1 or\
                parse.find('[3_ArrivalPlace]') > -1 or\
                parse.find('[DisambiguateArrival]') > -1:
                    dateTime['time_type'] = 'arrival'
                else:
                    dateTime['time_type'] = 'departure'
            self.appLogger.info('3')
            if result[':timeperiod_spec'] != '':
                dateTime['period_spec'] = result[':timeperiod_spec']
            self.appLogger.info('4')
            self.timeSpecDict.update({dateTime['value']:dateTime})
            self.appLogger.info('dateTime: %s'%str(dateTime))
            userAction.content.update({'travel_time':dateTime['value']})
            self.appLogger.info('5')
        if frame[':properties'].has_key(':[0_busnumber.route]'):
            userAction.content.update({'route':frame[':properties'][':[0_busnumber.route]']})
        if frame[':properties'].has_key(':[generic.yes]'):
            userAction.content.update({'confirm':'YES'})
        if frame[':properties'].has_key(':[generic.no]'):
            userAction.content.update({'confirm':'NO'})
        if frame[':properties'].has_key(':[4_busafterthatrequest]'):
            self.appLogger.info('%s'%frame[':properties'][':[4_busafterthatrequest]'])
        if frame[':properties'].has_key(':[generic.quit]'):
            self.appLogger.info('Good bye')

        self.appLogger.info('6')

        parse = frame[':properties'][':parse_str']
        if updateDeparturePlaceType:
            place = userAction.content['departure_place']
            self.appLogger.info('%d'%parse.find(place))
            subParse = parse[parse.find(place)-20:parse.find(place)]
            self.appLogger.info('place %s, subParse %s'%(place,subParse))
            if subParse.find('neighborhood') > -1:
                self.departurePlaceTypeDict[place] = 'neighborhood'
            else:
                self.departurePlaceTypeDict[place] = 'stop'
        if updateArrivalPlaceType:
            place = userAction.content['arrival_place']
            subParse = parse[parse.find(place)-20:parse.find(place)]
            self.appLogger.info('place %s, subParse %s'%(place,subParse))
            if subParse.find('neighborhood') > -1:
                self.arrivalPlaceTypeDict[place] = 'neighborhood'
            else:                        
                self.arrivalPlaceTypeDict[place] = 'stop'

        self.appLogger.info('7')

        self.appLogger.info('userAction: %s'%str(userAction))

        if userAction.content == {}:
            self.asrResult = ASRResult.FromHelios([UserAction('non-understanding')],[1.0])
        else:
            userActions = [userAction]
            probs = [float(frame[':properties'][':confidence'])]
            self.asrResult = ASRResult.FromHelios(userActions,probs)

        self.appLogger.info('ASRResult: %s'%str(self.asrResult))
                
    def _SystemUtteranceStartHandler(self,frame):
        self.appLogger.info('system_utterance_start(%s) %s'%(frame[':properties'][':utt_count'],\
                                                             frame[':properties'][':tagged_prompt']))

    def _SystemUtteranceEndHandler(self,frame):
        self.appLogger.info('system_utterance_end(%s)'%frame[':properties'][':utt_count'])
        self.notifyPrompts.remove(frame[':properties'][':utt_count'])
        self.appLogger.info('notifyPrompts: [ %s ]'%', '.join(self.notifyPrompts))

    def _DialogStateChangeHandler(self,frame):
        self.appLogger.info('dialog_state_change')
        # update dialog state
        self.dialogState = 'inform_welcome' if not self.newDialogState else self.newDialogState
        self.dialogStateIndex += 1
        # broadcast dialog state
        message = MakeDialogStateMessage(self.dialogState,self.turnNumber,\
                                      ' '.join(self.notifyPrompts))
        self.outQueue.put(message)
        self.inQueue.get()
        self.inQueue.task_done()

    def _TurnTimeoutHandler(self,frame):
        self.appLogger.info('turn_timeout')
        self.idSuffix += 1

        self.asrResult = ASRResult.FromHelios([UserAction('non-understanding')],[1.0])
        self.appLogger.info('ASRResult: %s'%str(self.asrResult))

    def _UnknownEventHandler(self,frame):
        self.appLogger.info('Unknow event')

    def _EndSessionHandler(self,frame):
        self.appLogger.info('end_session')

    def _RequestSystemUtterance(self,args):
        newDialogState,query,result,version = args
        message = MakeSystemUtterance(newDialogState,self.dialogState,self.turnNumber,\
                                      ' '.join(self.notifyPrompts),self.dialogStateIndex,\
                                      self.sessionID,self.idSuffix,self.uttCount,query,result,version)
        self.notifyPrompts.append(str(self.uttCount))
        self.idSuffix += 1
        self.uttCount += 1
        self.outQueue.put(message)
        self.inQueue.get()
        self.inQueue.task_done()
        
    def _RequestBackendQuery(self,args):
        newDialogState,query,result,version = args
        message = MakeSystemUtterance(newDialogState,self.dialogState,self.turnNumber,\
                                      ' '.join(self.notifyPrompts),self.dialogStateIndex,\
                                      self.sessionID,self.idSuffix,self.uttCount,query,result,version)
        self.notifyPrompts.append(str(self.uttCount))
        self.idSuffix += 1
        self.uttCount += 1
        self.outQueue.put(message)
        self.inQueue.get()
        self.inQueue.task_done()
        
    def _DialogProcessing(self,eventType):
        if eventType == 'begin_session':
            query = result = version = ''
            self.taskQueue.append((True,self._RequestSystemUtterance,('inform_welcome',query,result,version)))
            self.taskQueue.append((True,self._RequestSystemUtterance,('inform_how_to_get_help',query,result,version)))

        elif eventType == 'system_utterance_end':
            if self.notifyPrompts == [] and not self.systemAction:
                query = result = version = ''
                self.systemAction = self.dialogManager.Init()
                self._GetNewDialogState()
                self.taskQueue.append((True,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                self.appLogger.info('System action: %s'%str(self.systemAction))
                
        elif eventType == 'user_utterance_end' or eventType == 'turn_timeout':
            for i,interruptible,function,arg in enumerate(self.taskQueue):
                if interruptible and eventType == 'user_utterance_end': 
                    self.taskQueue.pop(i)
                else:
                    self.appLogger.info('Discard %s!!!'%eventType)

            if not self.systemAction:
                self.systemAction = self.dialogManager.Init(True)

            self.systemAction = self.dialogManager.TakeTurn(self.asrResult)
            self.appLogger.info('System action: %s'%str(self.systemAction))

            query = result = version = ''
            if eventType == 'turn_timeout':
                version = 'version\ttimeout\n'

            if self.systemAction.type == 'ask' and self.systemAction.force == 'request':
                self._GetNewDialogState()
                self.appLogger.info('New dialog state: %s'%self.newDialogState)
                self.taskQueue.append((False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
               
            elif self.systemAction.type == 'ask' and self.systemAction.force == 'confirm':
                if 'departure_place' in self.systemAction.content:
                    query = 'query.departure_place\t{\nname\t%s\ntype\t%s\n}\n'%\
                    (self.systemAction.content['departure_place'],self.departurePlaceTypeDict[self.systemAction.content['departure_place']])
                elif 'arrival_place' in self.systemAction.content:
                    query = 'query.arrival_place\t{\nname\t%s\ntype\t%s\n}\n'%\
                    (self.systemAction.content['arrival_place'],self.arrivalPlaceTypeDict[self.systemAction.content['arrival_place']])
                elif 'travel_time' in self.systemAction.content:
                    self.appLogger.info('time: %s'%self.systemAction.content['travel_time'])
                    timeSpec = self.timeSpecDict[self.systemAction.content['travel_time']]
                    self.appLogger.info('timeSpec: %s'%str(timeSpec))
                    try:
                        query = 'query.travel_time.time\t{\nvalue\t%s\nnow\t%s\ntype\t%s\n}\n'%\
                        (timeSpec['value'],timeSpec['now'],timeSpec['time_type'])
                    except:
                        query = 'query.travel_time.time\t{\nvalue\t%s\ntype\t%s\n}\n'%\
                        (timeSpec['value'],timeSpec['time_type'])
                elif 'route' in self.systemAction.content:
                    query = 'query.route_number\t%s\n'%self.systemAction.content['route']
                self._GetNewDialogState()
                self.appLogger.info('New dialog state: %s'%self.newDialogState)
                self.taskQueue.append((False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))

            elif self.systemAction.type == 'inform':
                # inform processing
                self.systemAction.force = 'processing'
                self._GetNewDialogState()
                self.appLogger.info('New dialog state: %s'%self.newDialogState)
                self.taskQueue.append((False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))

                # Backend lookup
                querySpec,belief = self.dialogManager.beliefState.GetTopUniqueUserGoal()
#                self.appLogger.info('query spec %s'%str(querySpec))
                querySpec['departure_place_type'] = self.departurePlaceTypeDict[querySpec['departure_place']]
                querySpec['arrival_place_type'] = self.arrivalPlaceTypeDict[querySpec['arrival_place']]
#                self.appLogger.info('query spec %s'%str(querySpec))
                querySpec.update(self.timeSpecDict[querySpec['travel_time']])
#                self.appLogger.info('query spec %s'%str(querySpec))

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
                    self.appLogger.info('Bus schedule: %s'%result.PPrint())
                else:
                    self.appLogger.info('Backend query for schedule failed')

                # inform success or failure
                self.systemAction.force = 'success'
                self._GetNewDialogState()
                self.appLogger.info('New dialog state: %s'%self.newDialogState)
                query,result = MakeScheduleSection(querySpec,result[':outframe'])
#                self.appLogger.info('query: %s'%query)
#                self.appLogger.info('result: %s'%result)
                self.taskQueue.append((False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                
                # request next query
#                query = result = ''
#                self.systemAction.force = 'request'
#                self.systemAction.force = 'starting_new_query'
#                self._GetNewDialogState()
#                self.appLogger.info('New dialog state: %s'%self.newDialogState)
#                message = MakeSystemUtterance(self.newDialogState,self.dialogState,self.turnNumber,\
#                                              ' '.join(self.notifyPrompts),self.dialogStateIndex,\
#                                              self.sessionID,self.idSuffix,self.uttCount,\
#                                              query,result,version)
#                self.notifyPrompts.append(str(self.uttCount))
#                self.idSuffix += 1
#                self.uttCount += 1
#                self.outQueue.put(message)
#                self.inQueue.get()
#                self.inQueue.task_done()

#            message = {'type':'WAITINTERACTIONEVENT'}
#            self.outQueue.put(message)
#            
        if self.taskQueue == []:
            message = {'type':'WAITINTERACTIONEVENT'}
            self.outQueue.put(message)
        else:
            (interruptible,function,arg) = self.taskQueue.pop(0)
            function(arg)
        
    def run(self):
        while True:
            self.appLogger.info('Wait event')
            frame = self.inQueue.get()
            self.inQueue.task_done()
            self.appLogger.info('Frame:\n%s'%frame.PPrint())
            
            if frame.name == 'begin_session':
                eventType = 'begin_session'
                self._BeginSessionHandler(frame)
            elif frame.name == 'DialogManager.handle_event':
                eventType = frame[':event_type']
                self.appLogger.info('event_type: %s'%eventType)
                if eventType == 'user_utterance_end':
                    self._UserUtteranceEndHandler(frame)
                elif eventType == 'system_utterance_start':
                    self._SystemUtteranceStartHandler(frame)
                elif eventType == 'system_utterance_end':
                    self._SystemUtteranceEndHandler(frame)
                elif eventType == 'dialog_state_change':
                    self._DialogStateChangeHandler(frame)
                elif eventType == 'turn_timeout':
                    self._TurnTimeoutHandler(frame)
                else:
                    self._UnknownEventHandler(frame)
            elif frame.name == 'end_session':
                eventType = 'end_session'
                self._EndSessionHandler(frame)
                
            self._DialogProcessing(eventType)
                
            
