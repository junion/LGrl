'''

'''

import logging.config
import logging
import threading
import Queue
from datetime import datetime
import sys,traceback
from copy import deepcopy
from GlobalConfig import *
from DialogManager import SBSarsaDialogManager as DialogManager
#from DialogManager import OpenDialogManager as DialogManager
from GalaxyFrames import *
from DialogModules import UserAction,ASRResult,SystemAction

MY_ID = 'DialogThread'

class GotoException(Exception):
    pass
    
class SkipDialogProcessing(Exception):
    pass
    
class DialogThread(threading.Thread):
    def __init__(self,sessionID,logDir,inQueue,outQueue,resultQueue):
        threading.Thread.__init__(self)

        self.config = GetConfig()
        self.appLogger = logging.getLogger(MY_ID)

        self.useDirectedOpenQuestion = self.config.getboolean(MY_ID,'useDirectedOpenQuestion')
        
        self.sessionID = sessionID
        self.logDir = logDir
        self.turnNumber = 0
        self.idSuffix = 0
        self.uttCount = 0
        self.dialogStateIndex = 0
        self.dialogState = 'initial'
        self.floorStatus = 'system'
        self.systemAction = SystemAction('initial')
        self.systemActionToRepeat = None
        self.newDialogState = None
        self.inQueue = inQueue
        self.outQueue = outQueue
        self.resultQueue = resultQueue
        self.eventWaitTimeout = self.config.getint(MY_ID,'eventWaitTimeout')
        self.dialogResult = ''
        self._InitDataForNewQuery()
#        self.notifyPrompts = []
#        self.waitEvent = []
#        self.departurePlaceTypeDict = {}
#        self.arrivalPlaceTypeDict = {}
#        self.departurePlaceQuerySpecDict = {}
#        self.arrivalPlaceQuerySpecDict = {}
#        self.timeSpecDict = {}
#        self.asrResult = None
#        self.taskQueue = []
#        self.querySpec = None
#        self.result = None
#        self.rides = None
        self.dialogManager = DialogManager()
        
        self.appLogger.info('Dialog thread %s created'%self.getName())

    def _InitDataForNewQuery(self):
        self.notifyPrompts = []
        self.waitEvent = []
        self.departurePlaceTypeDict = {}
        self.arrivalPlaceTypeDict = {}
        self.departurePlaceQuerySpecDict = {}
        self.arrivalPlaceQuerySpecDict = {}
        self.timeSpecDict = {}
        self.asrResult = None
        self.taskQueue = []
        self.querySpec = None
        self.result = None
        self.rides = None
        self.needToDTMFConfirm = False
        self.needToGiveTip = False
        self.taskToRepeat = None
        self.giveTipCount = 0
        
    def _GetNewDialogState(self):
        self.appLogger.info('_GetNewDialogState')
#        if not self.systemAction:
        if self.systemAction.type == 'initial':
            self.newDialogState = 'inform_welcome'
            self.appLogger.info(self.newDialogState)
        elif self.systemAction.type == 'ask' and self.systemAction.force == 'request':
            if self.systemAction.content == 'all':
                self.newDialogState = 'request_all'
            elif self.systemAction.content == 'departure_place':
                self.newDialogState = 'request_departure_place'
            elif self.systemAction.content == 'arrival_place':
                self.newDialogState = 'request_arrival_place'
            elif self.systemAction.content == 'travel_time':
                self.newDialogState = 'request_travel_time'
            elif self.systemAction.content == 'exact_travel_time':
                self.newDialogState = 'request_exact_travel_time'
            elif self.systemAction.content == 'next_query':
                self.newDialogState = 'request_next_query'
            elif self.systemAction.content == 'next_query_error':
                self.newDialogState = 'request_next_query_error'
        elif self.systemAction.type == 'ask' and self.systemAction.force == 'confirm':
            if 'route' in self.systemAction.content:
                self.newDialogState = 'confirm_route'
            elif 'departure_place' in self.systemAction.content:
                self.newDialogState = 'confirm_departure_place'
            elif 'arrival_place' in self.systemAction.content:
                self.newDialogState = 'confirm_arrival_place'
            elif 'travel_time' in self.systemAction.content:
                self.newDialogState = 'confirm_travel_time'
            elif 'uncovered_place' in self.systemAction.content:
                self.newDialogState = 'confirm_uncovered_place'
            elif 'uncovered_route' in self.systemAction.content:
                self.newDialogState = 'confirm_uncovered_route'
            elif 'discontinued_route' in self.systemAction.content:
                self.newDialogState = 'confirm_discontinued_route'
            elif 'no_stop_matching' in self.systemAction.content:
                self.newDialogState = 'confirm_no_stop_matching'
        elif self.systemAction.type == 'inform':
            if self.systemAction.force == 'confirm_okay':
                if self.newDialogState == 'confirm_route':
                    self.newDialogState = 'inform_confirm_okay_route'
                elif self.newDialogState == 'confirm_departure_place':
                    self.newDialogState = 'inform_confirm_okay_departure_place'
                elif self.newDialogState == 'confirm_arrival_place':
                    self.newDialogState = 'inform_confirm_okay_arrival_place'
                elif self.newDialogState == 'confirm_travel_time':
                    self.newDialogState = 'inform_confirm_okay_travel_time'
                elif self.newDialogState == 'confirm_uncovered_place':
                    self.newDialogState = 'inform_confirm_okay_uncovered_place'
                elif self.newDialogState == 'confirm_uncovered_route':
                    self.newDialogState = 'inform_confirm_okay_uncovered_route'
                elif self.newDialogState == 'confirm_discontinued_route':
                    self.newDialogState = 'inform_confirm_okay_discontinued_route'
                elif self.newDialogState == 'confirm_no_stop_matching':
                    self.newDialogState = 'inform_confirm_okay_no_stop_matching'
            elif self.systemAction.force == 'processing':
                self.newDialogState = 'inform_processing'
            elif self.systemAction.force == 'success':
                self.newDialogState = 'inform_success'
            elif self.systemAction.force == 'error':
                self.newDialogState = 'inform_error'
            elif self.systemAction.force == 'subsequent_processing':
                self.newDialogState = 'inform_subsequent_processing'
            elif self.systemAction.force == 'starting_new_query':
                self.newDialogState = 'inform_starting_new_query'
            elif self.systemAction.force == 'quit':
                self.newDialogState = 'inform_quit'
            elif self.systemAction.force == 'uncovered_place':
                self.newDialogState = 'inform_uncovered_place'
            elif self.systemAction.force == 'uncovered_route':
                self.newDialogState = 'inform_uncovered_route'
            elif self.systemAction.force == 'discontinued_route':
                self.newDialogState = 'inform_discontinued_route'
            elif self.systemAction.force == 'no_stop_matching':
                self.newDialogState = 'inform_no_stop_matching'
            elif self.systemAction.force == 'generic_tips':
                self.newDialogState = 'inform_generic_tips'
        self.appLogger.info('New dialog state: %s'%self.newDialogState)

    def _BeginSessionHandler(self,frame):
        self.appLogger.info('begin_session')
                
    def _UserUtteranceEndHandler(self,frame):
        self.appLogger.info('user_utterance_end')

        self.appLogger.info('Previous system action: %s'%str(self.systemAction))

        userAction = UserAction('ig',{})

        self.appLogger.info('top_slots: %s'%frame[':properties'][':top_slots'])
        self.appLogger.info('hypothesis: %s'%frame[':properties'][':hypothesis'])
        self.appLogger.info('confidence: %s'%frame[':properties'][':confidence'])

        # DTMF
        if frame[':properties'].has_key(':[dtmf_key.dtmf_zero]') or \
        frame[':properties'].has_key(':[generic.help.general_help]'):
            userAction.content.update({'help':'help'})
        if frame[':properties'].has_key(':[dtmf_key.dtmf_one]'):
            userAction.content.update({'confirm':'YES'})
            frame[':properties'][':confidence'] = '1.0'
        if frame[':properties'].has_key(':[dtmf_key.dtmf_three]'):
            userAction.content.update({'confirm':'NO'})
            frame[':properties'][':confidence'] = '1.0'
        if frame[':properties'].has_key(':[dtmf_key.dtmf_four]'):
            userAction.content.update({'next':'SUCCESS'})
        if frame[':properties'].has_key(':[dtmf_key.dtmf_six]'):
            userAction.content.update({'next':'FAIL'})

        # Place                    
        if frame[':properties'].has_key(':[1_singleplace.stop_name.uncovered_place]'):
            userAction.content.update({'uncovered_place':frame[':properties'][':[1_singleplace.stop_name.uncovered_place]']})
        if frame[':properties'].has_key(':[2_departureplace.stop_name.uncovered_place]'):
            userAction.content.update({'uncovered_place':frame[':properties'][':[2_departureplace.stop_name.uncovered_place]']})
        if frame[':properties'].has_key(':[2_arrivalplace.stop_name.uncovered_place]'):
            userAction.content.update({'uncovered_place':frame[':properties'][':[2_arrivalplace.stop_name.uncovered_place]']})
            
        updateDeparturePlaceType = updateArrivalPlaceType = False
        if frame[':properties'].has_key(':[1_singleplace.stop_name.covered_place]'):
            hypothesis = frame[':properties'][':[1_singleplace.stop_name.covered_place]']
            if self.systemAction.type == 'ask' and self.systemAction.force == 'request':
                if self.systemAction.content == 'departure_place':
                    userAction.content.update({'departure_place':hypothesis})
                    updateDeparturePlaceType = True
                elif self.systemAction.content == 'arrival_place':
                    userAction.content.update({'arrival_place':hypothesis})
                    updateArrivalPlaceType = True
                elif self.useDirectedOpenQuestion and self.systemAction.content == 'all':
                    userAction.content.update({'departure_place':hypothesis})
                    updateDeparturePlaceType = True
                else:
                    userAction.content.update({'departure_place':hypothesis,'arrival_place':hypothesis})
                    updateDeparturePlaceType = True
                    updateArrivalPlaceType = True
            else:
                userAction.content.update({'departure_place':hypothesis})
                updateDeparturePlaceType = True
        if frame[':properties'].has_key(':[2_departureplace.stop_name.covered_place]'):
            hypothesis = frame[':properties'][':[2_departureplace.stop_name.covered_place]']
            userAction.content.update({'departure_place':hypothesis})
            updateDeparturePlaceType = True
        if frame[':properties'].has_key(':[3_arrivalplace.stop_name.covered_place]'):
            hypothesis = frame[':properties'][':[3_arrivalplace.stop_name.covered_place]']
            userAction.content.update({'arrival_place':hypothesis})
            updateArrivalPlaceType = True
        parse = frame[':properties'][':parse_str']
        if updateDeparturePlaceType:
            place = userAction.content['departure_place']
#            self.appLogger.info('%d'%parse.find(place))
            subParse = parse[parse.find(place)-20:parse.find(place)]
            self.appLogger.info('place %s, subParse %s'%(place,subParse))
            if subParse.find('neighborhood') > -1:
                self.departurePlaceTypeDict[place] = 'neighborhood'
            else:
                self.departurePlaceTypeDict[place] = 'stop'
            if place not in self.departurePlaceQuerySpecDict:
                querySpec = {}
                querySpec['departure_place'] = place
                querySpec['departure_place_type'] = self.departurePlaceTypeDict[place]
                if not self._RequestDeparturePlaceQuery(querySpec):
                    userAction.content = {'no_stop_matching':place}
#                self.taskQueue.append((False,True,self._RequestDeparturePlaceQuery,querySpec))
        if updateArrivalPlaceType:
            place = userAction.content['arrival_place']
            subParse = parse[parse.find(place)-20:parse.find(place)]
            self.appLogger.info('place %s, subParse %s'%(place,subParse))
            if subParse.find('neighborhood') > -1:
                self.arrivalPlaceTypeDict[place] = 'neighborhood'
            else:                        
                self.arrivalPlaceTypeDict[place] = 'stop'
            if place not in self.arrivalPlaceQuerySpecDict:
                querySpec = {}
                querySpec['arrival_place'] = place
                querySpec['arrival_place_type'] = self.arrivalPlaceTypeDict[place]
                if not self._RequestArrivalPlaceQuery(querySpec):
                    userAction.content = {'no_stop_matching':place}
#                self.taskQueue.append((False,True,self._RequestArrivalPlaceQuery,querySpec))

        # Route
        if frame[':properties'].has_key(':[0_busnumber.route.0_uncovered_route]'):
            userAction.content.update({'uncovered_route':frame[':properties'][':[0_busnumber.route.0_uncovered_route]']})
        if frame[':properties'].has_key(':[0_busnumber.route.0_discontinued_route]'):
            userAction.content.update({'discontinued_route':frame[':properties'][':[0_busnumber.route.0_discontinued_route]']})
        if frame[':properties'].has_key(':[0_busnumber.0_covered_route]'):
            userAction.content.update({'route':frame[':properties'][':[0_busnumber.0_covered_route]']})

        # Time
        if frame[':properties'].has_key(':[4_datetime]'):
            message = MakeParseDateTimeMessage(frame[':properties'][':gal_slotsframe'])
            self.outQueue.put(message)
#            result = self.inQueue.get()
#            self.inQueue.task_done()
            result = self.resultQueue.get()
            self.resultQueue.task_done()
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
#            self.appLogger.info('2')
            if gotTime:   
                parse = frame[':properties'][':parse_str']
                if parse.find('[4_ArrivalTime]') > -1 or\
                parse.find('[3_ArrivalPlace]') > -1 or\
                parse.find('[DisambiguateArrival]') > -1:
                    dateTime['time_type'] = 'arrival'
                else:
                    dateTime['time_type'] = 'departure'
    #            self.appLogger.info('3')
                if result[':timeperiod_spec'] != '':
                    dateTime['period_spec'] = result[':timeperiod_spec']
    #            self.appLogger.info('4')
                self.timeSpecDict.update({dateTime['value']:deepcopy(dateTime)})
                self.appLogger.info('dateTime: %s'%str(dateTime))
                userAction.content.update({'travel_time':dateTime['value']})
    #            self.appLogger.info('5')
            else:
                self.appLogger.info('No exact date time')
                userAction.content.update({'travel_time':'NEED EXACT TIME'})
        if frame[':properties'].has_key(':[4_busafterthatrequest]'):
            self.appLogger.info('%s'%frame[':properties'][':[4_busafterthatrequest]'])
            if self.systemAction.type == 'ask' and self.systemAction.force == 'request' and \
                self.systemAction.content == 'next_query': 
                userAction.content.update({'next':'NEXT BUS'})
            else:
                dateTime = {}
                dateTime['period_spec'] = 'now'
                dateTime['time_type'] = 'departure'
                dateTime['now'] = 'true'
                self.timeSpecDict.update({'NOW':deepcopy(dateTime)})
                self.appLogger.info('dateTime: %s'%str(dateTime))
                userAction.content.update({'travel_time':'NOW'})
        if frame[':properties'].has_key(':[4_busbeforethatrequest]'):
            self.appLogger.info('%s'%frame[':properties'][':[4_busbeforethatrequest]'])
            userAction.content.update({'next':'PREVIOUS BUS'})

        # Generic
        if frame[':properties'].has_key(':[generic.yes]'):
            userAction.content.update({'confirm':'YES'})
        if frame[':properties'].has_key(':[generic.no]'):
            userAction.content.update({'confirm':'NO'})
        if frame[':properties'].has_key(':[generic.quit]'):
            self.appLogger.info('Good bye')
            userAction.content.update({'next':'QUIT'})
        if frame[':properties'].has_key(':[generic.startover]'):
            self.appLogger.info('Start over')
            userAction.content.update({'next':'STARTOVER'})

        if self.systemAction.type == 'ask' and self.systemAction.force == 'confirm' and\
        ((frame[':properties'].has_key(':[4_datetime]') and frame[':properties'][':[4_datetime]'] == 'NOW') or\
        (('departure_place' in userAction.content and userAction.content['departure_place'] == 'MOON') or\
        ('arrival_place' in userAction.content and userAction.content['arrival_place'] == 'MOON') or\
        ('uncovered_place' in userAction.content and userAction.content['uncovered_place'] == 'MOON'))):
            userAction.content = {'confirm':'NO'}

        if 'confirm' in userAction.content:
            self.appLogger.info('For now, just deal with YES/NO only in a turn')
            userAction.content = {'confirm':userAction.content['confirm']}
                        
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
        if frame[':properties'][':utt_count'] in self.notifyPrompts:
            self.notifyPrompts.remove(frame[':properties'][':utt_count'])
        else:
            self.appLogger.info('Cannot remove utterance %s'%frame[':properties'][':utt_count'])
        self.appLogger.info('notifyPrompts: [ %s ]'%', '.join(self.notifyPrompts))

    def _SystemUtteranceCanceledHandler(self,frame):
        self.appLogger.info('system_utterance_canceled(%s)'%frame[':properties'][':utt_count'])
        if frame[':properties'][':utt_count'] in self.notifyPrompts:
            self.notifyPrompts.remove(frame[':properties'][':utt_count'])
        else:
            self.appLogger.info('Cannot remove utterance %s'%frame[':properties'][':utt_count'])
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
#        self.inQueue.get()
#        self.inQueue.task_done()
        self.resultQueue.get()
        self.resultQueue.task_done()

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
#        self.inQueue.get()
#        self.inQueue.task_done()
        self.resultQueue.get()
        self.resultQueue.task_done()

    def _RequestDeparturePlaceQuery(self,args):
        # Backend lookup
        querySpec = args
        message = MakeDeparturePlaceQuery(querySpec)
        self.outQueue.put(message)
#        result = self.inQueue.get()
#        self.inQueue.task_done()
        result = self.resultQueue.get()
        self.resultQueue.task_done()
#        self.appLogger.info('New dialog state: %s'%self.newDialogState)
        if result[':outframe'].find('failed\t1') > -1: 
            self.appLogger.info('Backend query for place failed')
            return False
        else:
            self.departurePlaceQuerySpecDict[querySpec['departure_place']] = result[':outframe']
            return True

    def _RequestArrivalPlaceQuery(self,args):
        querySpec = args
        message = MakeArrivalPlaceQuery(querySpec)
        self.outQueue.put(message)
#        result = self.inQueue.get()
#        self.inQueue.task_done()
        result = self.resultQueue.get()
        self.resultQueue.task_done()
        if result[':outframe'].find('failed\t1') > -1: 
            self.appLogger.info('Backend query for place failed')
            return False
        else:
            self.arrivalPlaceQuerySpecDict[querySpec['arrival_place']] = result[':outframe']
            return True

    def _RequestBackendQuery(self,args):
        # Backend lookup
        self.querySpec,belief = self.dialogManager.beliefState.GetTopUniqueUserGoal()
#        self.appLogger.info('query spec %s'%str(self.querySpec))
        self.querySpec['departure_place_type'] = self.departurePlaceTypeDict[self.querySpec['departure_place']]
        self.querySpec['arrival_place_type'] = self.arrivalPlaceTypeDict[self.querySpec['arrival_place']]
        self.appLogger.info('timeSpec %s'%str(self.timeSpecDict[self.querySpec['travel_time']]))
        self.querySpec.update(self.timeSpecDict[self.querySpec['travel_time']])
#        self.appLogger.info('query spec %s'%str(self.querySpec))
#
#        message = MakeDeparturePlaceQuery(self.querySpec)
#        self.outQueue.put(message)
#        result = self.inQueue.get()
#        self.inQueue.task_done()
#        if result:
#            self.querySpec['departure_stops'] = result[':outframe']
#        else:
#            self.appLogger.info('Backend query for place failed')
#
#        message = MakeArrivalPlaceQuery(self.querySpec)
#        self.outQueue.put(message)
#        result = self.inQueue.get()
#        self.inQueue.task_done()
#        if result:
#            self.querySpec['arrival_stops'] = result[':outframe']
#        else:
#            self.appLogger.info('Backend query for place failed')

        self.querySpec['departure_stops'] = self.departurePlaceQuerySpecDict[self.querySpec['departure_place']]
        self.querySpec['arrival_stops'] = self.arrivalPlaceQuerySpecDict[self.querySpec['arrival_place']]

        message = MakeScheduleQuery(self.querySpec)
        self.outQueue.put(message)
#        self.result = self.inQueue.get()
#        self.inQueue.task_done()
        self.result = self.resultQueue.get()
        self.resultQueue.task_done()
        if self.result:
            self.appLogger.info('Bus schedule: %s'%self.result.PPrint())
        else:
            self.appLogger.info('Backend query for schedule failed')

    def _RequestSubsequentBackendQuery(self,args):
#        next = args if args else None
        message = MakeScheduleQuery(self.querySpec,self.result[':outframe'],args)
        self.outQueue.put(message)
#        self.rides = self.inQueue.get()
#        self.inQueue.task_done()
        self.rides = self.resultQueue.get()
        self.resultQueue.task_done()
        self._MergeResultRide()
        if self.result:
            self.appLogger.info('Bus schedule: %s'%self.result.PPrint())
        else:
            self.appLogger.info('Backend query for schedule failed')

    def _RequestInformResult(self,args):
        # inform success or failure
        self.appLogger.info('_RequestInformResult')
        query = result = version = ''
        self.systemAction.type = 'inform'
        self.appLogger.info('%s'%self.result[':outframe'])
        if self.result[':outframe'].find('failed\t0') > -1: 
            self.systemAction.force = 'success'
            self.appLogger.info('success')
        else:
            self.systemAction.force = 'error'
            self.appLogger.info('error')
        self._GetNewDialogState()
#        self.appLogger.info('New dialog state: %s'%self.newDialogState)
        query,result = MakeScheduleSection(self.querySpec,self.result[':outframe'],args)
        self.appLogger.info('query: %s'%query)
        self.appLogger.info('result: %s'%result)
        message = MakeSystemUtterance(self.newDialogState,self.dialogState,self.turnNumber,\
                                      ' '.join(self.notifyPrompts),self.dialogStateIndex,\
                                      self.sessionID,self.idSuffix,self.uttCount,query,result,version)
        self.appLogger.info('message: %s'%message['content'])
        self.notifyPrompts.append(str(self.uttCount))
        self.idSuffix += 1
        self.uttCount += 1
        self.outQueue.put(message)
#        self.inQueue.get()
#        self.inQueue.task_done()
        self.resultQueue.get()
        self.resultQueue.task_done()
                
    def _MergeResultRide(self):
        newResult = []
        newSection = False
#        self.appLogger.info('result\n %s',self.result.PPrint())
#        self.appLogger.info('rides\n %s',self.rides.PPrint())
        for x in self.result[':outframe'].split('\n'):
#            self.appLogger.info('%s'%str(newResult))
            if x.find('rides') > -1:
                newSection = True
            if not newSection:
                newResult.append(x)
            if x.find('failed') > -1:
                newSection = False
                newResult += self.rides[':outframe'].split('\n')[2:-3]
        self.result[':outframe'] = '\n'.join(newResult)
#        self.appLogger.info('result\n %s',self.result.PPrint())
        
    def _DialogProcessing(self,eventType):
        try:
#            query = result = version = ''
            if eventType == 'begin_session':
                query = result = version = ''
                self.taskQueue.append((True,False,self._RequestSystemUtterance,('inform_welcome',query,result,version)))
                self.taskQueue.append((True,False,self._RequestSystemUtterance,('inform_how_to_get_help',query,result,version)))
    
            elif eventType == 'system_utterance_end':
                query = result = version = ''
#                if self.notifyPrompts == [] and not self.systemAction:
                if self.notifyPrompts == [] and self.taskQueue == [] and\
                 self.waitEvent == [] and self.systemAction.type == 'initial':
                    self.systemAction = self.dialogManager.Init()
                    self._GetNewDialogState()
                    self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
#                    self.appLogger.info('System action: %s'%str(self.systemAction))

#                elif self.notifyPrompts == [] and self.systemAction.type == 'inform' and \
#                self.systemAction.force in ['success','fail']:
                elif self.systemAction.type == 'inform' and self.systemAction.force in ['success','error']:
                    # request next query
#                    self.appLogger.info('1')
                    self.systemAction.content = 'next_query' if self.systemAction.force == 'success' else 'next_query_error'
                    self.systemAction.type = 'ask'
#                    self.appLogger.info('2')
                    self.systemAction.force = 'request'
#                    self.appLogger.info('3')
#                    self.appLogger.info('4')
                    self._GetNewDialogState()
#                    self.appLogger.info('5')
#                    self.appLogger.info('New dialog state: %s'%self.newDialogState)
                    self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
#                    self.appLogger.info('6')
#                self.appLogger.info('7')
                                    
            elif eventType == 'user_utterance_end' or eventType == 'turn_timeout':
                self.appLogger.info('%s'%eventType)
                userActionUnavailable = False

                for i,(interruptible,execution,function,args) in enumerate(self.taskQueue):
                    if interruptible and eventType == 'user_utterance_end': 
                        self.appLogger.info('Discard interruptible event')
                        self.appLogger.info('execution: %s'%str(execution))
                        self.appLogger.info('function: %s'%str(function))
                        self.appLogger.info('args: %s'%str(args))
                        self.taskQueue.pop(i)
                    elif eventType == 'turn_timeout':
                        self.appLogger.info('Discard turn_timeout!!!')
                        raise GotoException('Do task')

#                if not self.systemAction:
                if self.systemAction.type == 'initial':
                    self.systemAction = self.dialogManager.Init(True)

                query = result = version = ''
                    
                # Rule-parts
                if self.needToDTMFConfirm:
                    self.appLogger.info('Trigger confirmation with DTMF option')
                    self.needToDTMFConfirm = False
                    interruptible,execution,function,args = self.taskToRepeat
                    newDialogState,query,result,version = args
                    self.newDialogState = newDialogState
                    self.taskQueue.append((interruptible,execution,function,(newDialogState,query,result,'version\twhat_can_i_say\n')))
                    self.taskToRepeat = []
                    raise GotoException('Do task')
                    
                if self.needToGiveTip:
                    if self.giveTipCount == 1 or self.giveTipCount == 3:
                        self.systemAction.type = 'inform'
                        self.systemAction.force = 'generic_tips'
                        self._GetNewDialogState()
                        self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                    self.needToGiveTip = False
                    self.giveTipCount += 1
                    raise GotoException('Do task')
#                    interruptible,execution,function,args = self.taskToRepeat
#                    newDialogState,query,result,version = args
#                    self.newDialogState = newDialogState
#                    self.taskQueue.append(self.taskToRepeat)
#                    self.taskToRepeat = []
#                    raise GotoException('Do task')

                if self.asrResult.userActions[0].type != 'non-understanding' and \
                'help' in self.asrResult.userActions[0].content:
                    self.taskQueue.append((True,False,self._RequestSystemUtterance,(self.newDialogState,query,result,'version\texplain_more\n')))
                    self.taskQueue.append((True,False,self._RequestSystemUtterance,(self.newDialogState,query,result,'version\twhat_can_i_say\n')))
                    # dialog state broadcasting needed?
                    raise GotoException('Do task')
                
                elif self.asrResult.userActions[0].type != 'non-understanding' and \
                'next' in self.asrResult.userActions[0].content and \
                self.asrResult.userActions[0].content['next'] == 'STARTOVER':
                    self.systemAction.type = 'inform'
                    self.systemAction.force = 'starting_new_query'
                    self._GetNewDialogState()
#                    self.appLogger.info('New dialog state: %s'%self.newDialogState)
                    self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                    self._InitDataForNewQuery()
                    self.systemAction = self.dialogManager.Init()
                    self._GetNewDialogState()
                    self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                    raise GotoException('Do task')

                elif self.systemAction.type == 'ask' and self.systemAction.force == 'request' and \
                self.systemAction.content in ['next_query','next_query_error']:
                    if self.asrResult.userActions[0].type == 'non-understanding' or \
                    'next' not in self.asrResult.userActions[0].content:
#                        self.appLogger.info('discard')
                        if self.systemAction.content == 'next_query':
                            self.systemAction.content = 'next_query'
                            self.systemAction.type = 'ask'
                            self.systemAction.force = 'request'
                            self._GetNewDialogState()
    #                        self.appLogger.info('New dialog state: %s'%self.newDialogState)
                            self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,'version\twhat_can_i_say\n')))
                        else:
                            self.systemAction.content = 'next_query_error'
                            self.systemAction.type = 'ask'
                            self.systemAction.force = 'request'
                            self._GetNewDialogState()
    #                        self.appLogger.info('New dialog state: %s'%self.newDialogState)
                            self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                        raise GotoException('Do task')
                    next = self.asrResult.userActions[0].content['next']
                    if  next in ['NEXT BUS','PREVIOUS BUS']:
                        self.systemAction.type = 'inform'
                        self.systemAction.force = 'subsequent_processing'
                        self._GetNewDialogState()
#                        self.appLogger.info('New dialog state: %s'%self.newDialogState)
                        self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
#                        self._RequestSystemUtterance((self.newDialogState,query,result,version))
                        self.taskQueue.append((False,True,self._RequestSubsequentBackendQuery,(next)))
                        self.taskQueue.append((False,False,self._RequestInformResult,(next)))
                    elif next == 'QUIT':
                        self.systemAction.type = 'inform'
                        self.systemAction.force = 'quit'
                        self._GetNewDialogState()
#                        self.appLogger.info('New dialog state: %s'%self.newDialogState)
                        self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                    elif next in ['SUCCESS','FAIL']:
                        if next == 'SUCCESS':
                            self.appLogger.info('User evaluation: SUCCESS')
                        else:
                            self.appLogger.info('User evaluation: FAIL')
                        self.systemAction.content = 'next_query'
                        self.systemAction.type = 'ask'
                        self.systemAction.force = 'request'
                        self._GetNewDialogState()
#                        self.appLogger.info('New dialog state: %s'%self.newDialogState)
                        self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,'version\twhat_can_i_say\n')))
#                    elif next == 'STARTOVER':
#                        self.systemAction.type = 'inform'
#                        self.systemAction.force = 'starting_new_query'
#                        self._GetNewDialogState()
#                        self.appLogger.info('New dialog state: %s'%self.newDialogState)
#                        self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
#                        self.systemAction = self.dialogManager.Init()
#                        self._GetNewDialogState()
#                        self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                    raise GotoException('Do task')
                else:
                    if self.systemAction.type == 'inform' and self.systemAction.force not in ['confirm_okay','generic_tips']:
                        self.appLogger.info('Discard user utterance')
                        raise GotoException('Do task')
    
                    if self.asrResult.userActions[0].type != 'non-understanding' and \
                    'uncovered_place' in self.asrResult.userActions[0].content:
    #                    self.systemActionToRepeat = deepcopy(self.systemAction)
                        self.systemAction.type = 'ask'
                        self.systemAction.force = 'confirm'
                        self.systemAction.content = {'uncovered_place':self.asrResult.userActions[0].content['uncovered_place']}
                        query = 'uncovered_place\t{\nname\t%s\ntype\tstop\n}\n'%self.systemAction.content['uncovered_place']
                        self._GetNewDialogState()
    #                    self.appLogger.info('New dialog state: %s'%self.newDialogState)
                        self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                        raise GotoException('Do task')
    
                    if self.asrResult.userActions[0].type != 'non-understanding' and \
                    'uncovered_route' in self.asrResult.userActions[0].content:
    #                    self.systemActionToRepeat = deepcopy(self.systemAction)
                        self.systemAction.type = 'ask'
                        self.systemAction.force = 'confirm'
                        self.systemAction.content = {'uncovered_route':self.asrResult.userActions[0].content['uncovered_route']}
                        query = 'uncovered_route\t%s\n'%self.systemAction.content['uncovered_route']
                        self._GetNewDialogState()
    #                    self.appLogger.info('New dialog state: %s'%self.newDialogState)
                        self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                        raise GotoException('Do task')
    
                    if self.asrResult.userActions[0].type != 'non-understanding' and \
                    'discontinued_route' in self.asrResult.userActions[0].content:
    #                    self.systemActionToRepeat = deepcopy(self.systemAction)
                        self.systemAction.type = 'ask'
                        self.systemAction.force = 'confirm'
                        self.systemAction.content = {'discontinued_route':self.asrResult.userActions[0].content['discontinued_route']}
                        query = 'discontinued_route\t%s\n'%self.systemAction.content['discontinued_route']
                        self._GetNewDialogState()
    #                    self.appLogger.info('New dialog state: %s'%self.newDialogState)
                        self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                        raise GotoException('Do task')

                    if self.asrResult.userActions[0].type != 'non-understanding' and \
                    'no_stop_matching' in self.asrResult.userActions[0].content:
    #                    self.systemActionToRepeat = deepcopy(self.systemAction)
                        self.systemAction.type = 'ask'
                        self.systemAction.force = 'confirm'
                        self.systemAction.content = {'no_stop_matching':self.asrResult.userActions[0].content['no_stop_matching']}
                        query = 'uncovered_place\t{\nname\t%s\ntype\tstop\n}\n'%self.systemAction.content['no_stop_matching']
                        self._GetNewDialogState()
    #                    self.appLogger.info('New dialog state: %s'%self.newDialogState)
                        self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                        raise GotoException('Do task')

                    if self.asrResult.userActions[0].type != 'non-understanding' and \
                    'travel_time' in self.asrResult.userActions[0].content and \
                    self.asrResult.userActions[0].content['travel_time'] == 'NEED EXACT TIME':
                        self.systemAction.type = 'ask'
                        self.systemAction.force = 'request'
                        self.systemAction.content = 'exact_travel_time'
                        self._GetNewDialogState()
                        self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                        raise GotoException('Do task')
    
                    if self.systemAction.type == 'ask' and self.systemAction.force == 'confirm':
                        if self.asrResult.userActions[0].type == 'ig' and 'confirm' in self.asrResult.userActions[0].content and \
                        self.asrResult.userActions[0].content['confirm'] == 'YES':
                            self.systemAction.type = 'inform'
                            self.systemAction.force = 'confirm_okay'
                            self._GetNewDialogState()
                            self.taskQueue.append((True,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                            if self.newDialogState == 'inform_confirm_okay_uncovered_place':
                                self.systemAction.type = 'inform'
                                self.systemAction.force = 'uncovered_place'
                                self._GetNewDialogState()
                                self.taskQueue.append((True,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                                self.asrResult = ASRResult.FromHelios([UserAction('non-understanding')],[1.0])
                                userActionUnavailable = True
                                self.dialogResult = 'uncovered_place'
                            elif self.newDialogState == 'inform_confirm_okay_uncovered_route':
                                self.systemAction.type = 'inform'
                                self.systemAction.force = 'uncovered_route'
                                self._GetNewDialogState()
                                self.taskQueue.append((True,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                                self.asrResult = ASRResult.FromHelios([UserAction('non-understanding')],[1.0])
                                userActionUnavailable = True
                                self.dialogResult = 'uncovered_route'
                            elif self.newDialogState == 'inform_confirm_okay_discontinued_route':
                                self.systemAction.type = 'inform'
                                self.systemAction.force = 'discontinued_route'
                                self._GetNewDialogState()
                                self.taskQueue.append((True,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                                self.asrResult = ASRResult.FromHelios([UserAction('non-understanding')],[1.0])
                                userActionUnavailable = True
                                self.dialogResult = 'discontinued_route'
                            elif self.newDialogState == 'inform_confirm_okay_no_stop_matching':
                                self.systemAction.type = 'inform'
                                self.systemAction.force = 'no_stop_matching'
                                self._GetNewDialogState()
                                query = 'place\t{\nname\t%s\ntype\tstop\n}\n'%self.systemAction.content['no_stop_matching']
                                self.taskQueue.append((True,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                                self.asrResult = ASRResult.FromHelios([UserAction('non-understanding')],[1.0])
                                userActionUnavailable = True
                                self.dialogResult = 'no_stop_matching'
                        elif self.asrResult.userActions[0].type == 'ig' and 'confirm' in self.asrResult.userActions[0].content and \
                        self.asrResult.userActions[0].content['confirm'] == 'NO':
                            if self.newDialogState == 'inform_confirm_okay_uncovered_place' or\
                            self.newDialogState == 'inform_confirm_okay_uncovered_route' or\
                            self.newDialogState == 'inform_confirm_okay_discontinued_route' or\
                            self.newDialogState == 'inform_confirm_okay_no_stop_matching':
                                self.asrResult = ASRResult.FromHelios([UserAction('non-understanding')],[1.0])
                                userActionUnavailable = True
                    
                if self.asrResult.userActions[0].type != 'non-understanding' and \
                'next' in self.asrResult.userActions[0].content:
                    self.appLogger.info('Discard user utterance')
                    raise GotoException('Do task')
                
                # RL-DM parts
                self.systemAction = self.dialogManager.TakeTurn(self.asrResult)
                self.appLogger.info('System action: %s'%str(self.systemAction))
    
                if eventType == 'turn_timeout':
                    version = 'version\ttimeout\n'
    
                if self.systemAction.type == 'ask' and self.systemAction.force == 'request':
                    self._GetNewDialogState()
#                    self.appLogger.info('New dialog state: %s'%self.newDialogState)
                    self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
                    if self.asrResult.userActions[0].type == 'non-understanding' and not userActionUnavailable:
                        self.taskQueue.append((True,False,self._RequestSystemUtterance,(self.newDialogState,query,result,'version\twhat_can_i_say\n')))
                   
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
                            try:
                                query = 'query.travel_time.time\t{\nvalue\t%s\ntype\t%s\n}\n'%\
                                (timeSpec['value'],timeSpec['time_type'])
                            except:
                                query = 'query.travel_time.time\t{\nnow\t%s\ntype\t%s\n}\n'%\
                                (timeSpec['now'],timeSpec['time_type'])
                    elif 'route' in self.systemAction.content:
                        query = 'query.route_number\t%s\n'%self.systemAction.content['route']
                    self._GetNewDialogState()
#                    self.appLogger.info('New dialog state: %s'%self.newDialogState)
                    self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
    
                elif self.systemAction.type == 'inform':
                    query = result = version = ''
                    # inform processing
                    self.systemAction.force = 'processing'
                    self._GetNewDialogState()
#                    self.appLogger.info('New dialog state: %s'%self.newDialogState)
                    self.taskQueue.append((False,False,self._RequestSystemUtterance,(self.newDialogState,query,result,version)))
#                    self._RequestSystemUtterance((self.newDialogState,query,result,version))
                    self.taskQueue.append((False,True,self._RequestBackendQuery,None))
                    self.taskQueue.append((False,False,self._RequestInformResult,None))
        except GotoException:
            self.appLogger.info(traceback.format_exc())

        self.appLogger.info('Tasks in wait:')
        self.appLogger.info('->\n'.join([str(x) for x in self.taskQueue]))
        while self.notifyPrompts == [] and self.taskQueue != []:
            (interruptible,execution,function,args) = self.taskQueue.pop(0)
            if not interruptible or self.waitEvent == []:
                self.waitEvent = filter(lambda x: x[0] == 'end_session',self.waitEvent)
                self.appLogger.info('Execute a task:')
                self.appLogger.info('interruptible: %s'%str(interruptible))
                self.appLogger.info('execution: %s'%str(execution))
                self.appLogger.info('function: %s'%str(function))
                self.appLogger.info('args: %s'%str(args))
                function(args)
                self.taskToRepeat = (interruptible,execution,function,args)
                if not execution:
                    break

        if eventType == 'user_utterance_end':
            self.turnNumber += 1
        
    def run(self):
            dialogSuccess = ''
            while True:
                try:
                    skipDialogProcessing = False
                    self.appLogger.info('Events in wait:')
                    self.appLogger.info('->\n'.join([str(x[0]) for x in self.waitEvent]))
                    if self.notifyPrompts == [] and not self.waitEvent == []:
                        for i,event in enumerate(reversed(self.waitEvent)):
                            if event[0] == 'user_utterance_end':
                                del self.waitEvent[0:len(self.waitEvent)-i-1]
                                self.appLogger.info('Remained events after pruning:')
                                self.appLogger.info('\n'.join([str(x[0]) for x in self.waitEvent]))
                        event = self.waitEvent.pop(0)
                        if event[0] == 'turn_timeout' and len(self.waitEvent) > 0:
                            self.appLogger.info('Skip event in wait %s'%event[0])
                            continue
                        self.appLogger.info('Take event in wait %s'%event[0])
                        frame = event[1]
                    else:
                        self.appLogger.info('Wait event')
                        try:
                            frame = deepcopy(self.inQueue.get(timeout=self.eventWaitTimeout))
                            self.inQueue.task_done()
    #                    except Queue.Empty:
                        except:
                            self.appLogger.info('Warning: no event for a long time')
                            for event in self.waitEvent:
                                if event[0] == 'end_session':
                                    self.appLogger.info('Flush waiting events to process end session')
                                    self.notifyPrompts = []
#                            self.notifyPrompts = []
                            continue
                    if frame == None:
                        self.appLogger.info('Warning: null frame')
                        continue
    #                self.appLogger.info('Frame:\n%s'%frame.PPrint())
                    if frame.name == 'begin_session':
                        eventType = 'begin_session'
                        self._BeginSessionHandler(frame)
                    elif frame.name == 'DialogManager.handle_event':
                        eventType = frame[':event_type']
                        self.appLogger.info('event_type: %s'%eventType)
                        if eventType == 'user_utterance_end':
                            if len(self.notifyPrompts) > 0:
                                self.appLogger.info('notifyPrompts: %s'%str(self.notifyPrompts))
                                self.appLogger.info('Next utterance count: %d'%self.uttCount)
                                self.appLogger.info('Previous system action: %s'%str(self.systemAction))
                                if self.systemAction.type == 'ask' and \
                                ((self.systemAction.force == 'request' and 
                                 self.systemAction.content in ['departure_place','arrival_place','travel_time'])\
                                 or \
                                 (self.systemAction.force == 'confirm' and 
                                  (not frame[':properties'].has_key(':[generic.yes]') and not frame[':properties'].has_key(':[generic.no]')))) and\
                                str(self.uttCount-1) in self.notifyPrompts:
                                    self.appLogger.info('Give a tip and append user utterance to wait event queue')
                                    self.waitEvent.append(('user_utterance_end',frame))
                                    self.needToGiveTip = True
#                                    skipDialogProcessing = True
                                elif frame[':properties'][':total_num_parses'] != '0' or self.dialogState.find('request_next_query') > -1:
                                    self.appLogger.info('Append user utterance to wait event queue')
                                    self.waitEvent.append(('user_utterance_end',frame))
                                    skipDialogProcessing = True
                                else:
                                    self.appLogger.info('Discard event because of no parse')
                                    skipDialogProcessing = True
                            else:
                                self._UserUtteranceEndHandler(frame)
                                if self.systemAction.type == 'ask' and self.systemAction.force == 'confirm' and\
                                self.asrResult.userActions[0].type == 'non-understanding':
                                    self.appLogger.info('Need to recommend to confirm using DTMF')
                                    self.needToDTMFConfirm = True
                        elif eventType == 'system_utterance_start':
                            self._SystemUtteranceStartHandler(frame)
                        elif eventType == 'system_utterance_end':
                            self._SystemUtteranceEndHandler(frame)
                        elif eventType == 'system_utterance_canceled':
                            self._SystemUtteranceCanceledHandler(frame)
                        elif eventType == 'dialog_state_change':
                            self._DialogStateChangeHandler(frame)
                        elif eventType == 'turn_timeout':
                            if len(self.notifyPrompts) > 0:
                                self.appLogger.info('Append turn timeout to wait event queue')
                                self.waitEvent.append(('turn_timeout',frame))
                                skipDialogProcessing = True
                            else:
                                self._TurnTimeoutHandler(frame)
                        else:
                            self._UnknownEventHandler(frame)
                    elif frame.name == 'end_session':
                        eventType = 'end_session'
                        if len(self.notifyPrompts) > 0:
                            self.appLogger.info('Append end session to wait event queue')
                            self.waitEvent.append(('end_session',frame))
                            skipDialogProcessing = True
                        else:
                            if self.dialogResult != '':
                                self.appLogger.info('Dialog result: %s\nNumber of turns: %d'%(self.dialogResult,self.turnNumber))
                                self.appLogger.critical('Dialog result %s: %s, Number of turns: %d'%(self.logDir,self.dialogResult,self.turnNumber))
                            else:
                                self.appLogger.info('Dialog result: Fail\nNumber of turns: %d'%self.turnNumber)
                                self.appLogger.critical('Dialog result %s: Fail, Number of turns: %d'%(self.logDir,self.turnNumber))
                            self._EndSessionHandler(frame)
                            message = {'type':'ENDSESSION'}
                            self.outQueue.put(message)
                            break
                    if not skipDialogProcessing:
                        self._DialogProcessing(eventType)
                        if self.newDialogState == 'inform_success':
                            self.dialogResult = 'inform_success'
                        if self.newDialogState == 'inform_error':
                            self.dialogResult = 'inform_error'
                        if self.notifyPrompts == [] and self.dialogState == 'inform_quit':
                            self.appLogger.info('Terminate for %s'%self.dialogState)
                            message = {'type':'DIALOGFINISHED'}
                            self.outQueue.put(message)
                    if not self.notifyPrompts == [] and len(self.waitEvent) > 1:
                        self.appLogger.info('Broadcasting dialog state to get events')
                        self._DialogStateChangeHandler(None)
                    if not self.notifyPrompts == [] or self.waitEvent == []:
                        self.appLogger.info('Indicate waiting for interaction events')
                        message = {'type':'WAITINTERACTIONEVENT'}
                        self.outQueue.put(message)
                except Exception:
                    self.appLogger.info('Try to recover from crash:')
                    self.appLogger.info(traceback.format_exc())
                    self.appLogger.error(traceback.format_exc())
                    self.appLogger.info('Tasks in wait:')
                    self.appLogger.info('->\n'.join([str(x) for x in self.taskQueue]))
                    self._InitDataForNewQuery()
                    self.systemAction = self.dialogManager.Init()
                    self._GetNewDialogState()
                    self._RequestSystemUtterance((self.newDialogState,'','',''))
                    message = {'type':'WAITINTERACTIONEVENT'}
                    self.outQueue.put(message)
                    
#            exit()
#            self.appLogger.info('Terminate for %s'%self.dialogState)
#            message = {'type':'DIALOGFINISHED'}
#            self.outQueue.put(message)
#            while True
#                self.appLogger.info('Wait event')
#                frame = deepcopy(self.inQueue.get())
#                self.inQueue.task_done()
#                if frame.name == 'end_session':
#                    self._EndSessionHandler(frame)
#                    message = {'type':'ENDSESSION'}
#                    self.outQueue.put(message)
#                    break
#                else:
#                    self.appLogger.info('Terminate for %s'%self.dialogState)
#                    message = {'type':'DIALOGFINISHED'}
#                    self.outQueue.put(message)
#                    
            
