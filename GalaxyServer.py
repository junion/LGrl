# This file (c) Copyright 1998 - 2002 The MITRE Corporation
#
# This file is part of the Galaxy Communicator system. It is licensed
# under the conditions described in the file LICENSE in the root
# directory of the Galaxy Communicator system.

import sys,exceptions
import logging.config
import logging
import threading
import Queue
from GlobalConfig import *
import Galaxy,GalaxyIO
from DialogThread import *

sys.path.append("E:/Development/LGrl-G")

InitConfig()
config = GetConfig()
config.read(['E:/Development/LGrl-G/LGrl.conf'])

logging.config.fileConfig('E:/Development/LGrl-G/logging.conf')
appLogger = logging.getLogger('Galaxy')

appLogger.info('GalaxyServer')

dialogThread = None
inSession = False
sessionID = None
lastEnv = None
lastFrame = None
properties = None
metaInfo = []
timeoutPeriod = 8

inQueue = None
outQueue = None

def CallGalaxyModuleFunction(galaxyCall):
    global lastEnv

    frameToHub = Galaxy.Frame(str=galaxyCall)
    try:
        frameFromHub = lastEnv.DispatchFrame(frameToHub)
        appLogger.info('frameFromHub:\n %s'%str(frameFromHub)) 
        return frameFromHub
    except GalaxyIO.DispatchError:
        appLogger.info('dispatch error')
        return None
    
def SendActionThroughHub(galaxyCall):
    global lastEnv

    frameToHub = Galaxy.Frame(str=galaxyCall)
    lastEnv.WriteFrame(frameToHub)

def DoDialogFlow(frame=None):
    global inQueue
    global outQueue
    global lastFrame

    appLogger.info('DoDialogFlow')
#    appLogger.info('lastFrame:\n %s'%str(lastFrame))
    inQueue.put(frame)
    appLogger.info('Message out')

    while True:
        message = outQueue.get()
        appLogger.info('Message in')
        appLogger.info('%s'%message['content'])
        outQueue.task_done()
        if message['type'] == 'GALAXYCALL':
            appLogger.info('GALAXYCALL')
            result = CallGalaxyModuleFunction(message['content'])
            appLogger.info('Message sent')
            inQueue.put(result)
        elif message['type'] == 'GALAXYACTIONCALL':
            appLogger.info('GALAXYACTIONCALL')
            SendActionThroughHub(message['content'])
            appLogger.info('Message sent')
            inQueue.put(None)
        elif message['type'] == 'WAITINPUT':
            return
        elif message['type'] == 'WAITINTERACTIONEVENT':
            appLogger.info('Wait interaction event')
            return
        elif message['type'] == 'DIALOGFINISHED':
            return


def reinitialize(env,frame):
    global lastEnv
    global incomingFrame

    lastEnv = env
    incomingFrame = frame

    appLogger.info('reinitialize called. Hub connection completed.')
    return frame

def begin_session(env,frame):
    global inSession
    global lastEnv
    global incomingFrame
    global lastFrame
    global dialogThread
    global inQueue
    global outQueue
    
    if inSession:
        end_session(env,frame)
    
    inSession = True

    lastEnv = env
    incomingFrame = frame
    lastFrame = frame

    appLogger.info('begin_session called.')
#    appLogger.info('frame:\n %s.'%str(frame))
    try:
        timeStamp = frame[':session_start_timestamp']
        appLogger.info('Init timestamp: %s.'%str(timeStamp))
    except KeyError:
        appLogger.info("Can't find :session_start_timestamp")
    try:
        sessionID = frame[':sess_id']
        appLogger.info('Init session ID: %s.'%str(sessionID))
    except KeyError:
        appLogger.info("Can't find :sess_id")
 
    inQueue = Queue.Queue()
    outQueue = Queue.Queue()
   
#    appLogger.info("Dialog thread creation")
    dialogThread = DialogThread(str(sessionID),inQueue,outQueue)
#    appLogger.info("Done")
    dialogThread.setDaemon(True)
#    appLogger.info("Daemonized")
    dialogThread.start()
#    appLogger.info("Started")
    
    DoDialogFlow(frame)
    
    appLogger.info('DM processing finished.')
    
    return frame

def end_session(env,frame):
    global inSession
    global lastEnv
    global lastFrame
    global properties
    global dialogThread
    global inQueue
    global outQueue

    if not inSession:
        return frame
    
    lastEnv = env
    lastFrame = frame
    
    lastFrame[':event_type'] = 'end_session'
    lastFrame[':event_complete'] = 1
    
    properties = Galaxy.Frame(type = Galaxy.GAL_CLAUSE,name = "properties")
    properties[':terminate_session'] = 'true'
    
    lastFrame[':properties'] = properties
    
    appLogger.info('end_session called; sending terminate to Core')
    
    DoDialogFlow(frame)

    appLogger.info('DM processing finished.')

    dialogThread.join()
    appLogger.info('Dialog thread terminated.')

    dialogThread = None
    inQueue = None
    outQueue = None
    
    inSession = False
    
    return frame

def handle_event(env,frame):
    global inSession
    global lastEnv
    global lastFrame

    appLogger.info('handle_event')
    appLogger.info('frame:\n%s'%frame.PPrint())
   
    if not inSession:
        return frame
    
    lastEnv = env
    lastFrame = frame
    
    DoDialogFlow(frame)
    
    appLogger.info('DM processing finished.')
    
    return frame
    
def service_timeout():
    global inSession
    global metaInfo

    if not inSession:
        return
    
    appLogger.info('service_timeout called.')
    metaInfo = []
    metaInfo[':timeout_elapsed'] = True
    
    DoDialogFlow()
    
    appLogger.info('DM processing finished.')
    
def start_inactivity_timeout(env,frame):
    global inSession
    global lastEnv
    global incomingFrame
    
    if not inSession:
        return frame

    lastEnv = env
    incomingFrame = frame

    appLogger.info('start_inactivity_timeout called; installing time trigger (%d secs)'%timeoutPeriod)
    
#    Gal_AddTimedTask(service_timeout, NULL, 1000*iTimeoutPeriod)

    return frame

def cancel_inactivity_timeout(env,frame):
    global inSession
    global lastEnv
    global incomingFrame

    if not inSession:
        return frame
    
    lastEnv = env
    incomingFrame = frame

    appLogger.info('cancel_inactivity_timeout called; removing the trigger')
    
#    Gal_RemoveTimedTask(service_timeout, NULL)

    return frame


#def process_parse(env,frame):
#    try:
#        resframe = env.DispatchFrame(Galaxy.Frame("gal_be",
#                                                Galaxy.GAL_CLAUSE,
#                                                {":sql_query":"parse"}))
#        print resframe
#    except GalaxyIO.DispatchError,error_frame:
#        print error_frame
# reply
#    self.env.Reply(new_f)
#    return None

#def notify_output_manager(env,frame):
#    return frame

# oas in C is -increment i.

#OAS = [("-increment i", "initial increment")]

# Write a wrapper for the usage check.

class LGrlServer(GalaxyIO.Server):
    def __init__(self, in_args, server_name = "<unknown>",
                 default_port = 0,
                 verbosity = -1,
                 require_port = 0,
                 maxconns = 1,
                 validate = 0,
                 server_listen_status = GalaxyIO.GAL_CONNECTION_LISTENER,
                 client_pair_string = None,
                 session_id = None,
                 server_locations_file = None,
                 slf_name = None,
                 env_class = GalaxyIO.CallEnvironment):
        GalaxyIO.Server.__init__(self, in_args, server_name,
                         default_port, verbosity,
                         require_port, maxconns,
                         validate, server_listen_status,
                         client_pair_string, session_id,
                         server_locations_file,
                         slf_name,
                         env_class)

#    def CheckUsage(self, oas_list, args):
#        global InitialIncrement
#        data, out_args = GalaxyIO.Server.CheckUsage(self, OAS + oas_list, args)
#        if data.has_key("-increment"):
#            InitialIncrement = data["-increment"][0]
#            del data["-increment"]
#        return data, out_args

def main():
    s = LGrlServer(sys.argv,"DialogManager",default_port=17000,verbosity=3)
    s.AddDispatchFunction("begin_session",begin_session,
                        [[[":int", Galaxy.GAL_INT, Galaxy.GAL_KEY_ALWAYS]],
                        Galaxy.GAL_OTHER_KEYS_NEVER,
                        Galaxy.GAL_REPLY_NONE, [],
                        Galaxy.GAL_OTHER_KEYS_NEVER])
    s.AddDispatchFunction("handle_event",handle_event,
                        [[[":int", Galaxy.GAL_INT, Galaxy.GAL_KEY_ALWAYS]],
                        Galaxy.GAL_OTHER_KEYS_NEVER,
                        Galaxy.GAL_REPLY_NONE, [],
                        Galaxy.GAL_OTHER_KEYS_NEVER])
#    s.AddDispatchFunction("process_parse",process_parse,
#                        [[[":int", Galaxy.GAL_INT, Galaxy.GAL_KEY_ALWAYS]],
#                        Galaxy.GAL_OTHER_KEYS_NEVER,
#                        Galaxy.GAL_REPLY_NONE, [],
#                        Galaxy.GAL_OTHER_KEYS_NEVER])
    s.AddDispatchFunction("start_inactivity_timeout",start_inactivity_timeout,
                        [[[":int", Galaxy.GAL_INT, Galaxy.GAL_KEY_ALWAYS]],
                        Galaxy.GAL_OTHER_KEYS_NEVER,
                        Galaxy.GAL_REPLY_NONE, [],
                        Galaxy.GAL_OTHER_KEYS_NEVER])
    s.AddDispatchFunction("cancel_inactivity_timeout",cancel_inactivity_timeout,
                        [[[":int", Galaxy.GAL_INT, Galaxy.GAL_KEY_ALWAYS]],
                        Galaxy.GAL_OTHER_KEYS_NEVER,
                        Galaxy.GAL_REPLY_NONE, [],
                        Galaxy.GAL_OTHER_KEYS_NEVER])
    s.AddDispatchFunction("end_session",end_session,
                        [[[":int", Galaxy.GAL_INT, Galaxy.GAL_KEY_ALWAYS]],
                        Galaxy.GAL_OTHER_KEYS_NEVER,
                        Galaxy.GAL_REPLY_NONE, [],
                        Galaxy.GAL_OTHER_KEYS_NEVER])
#    s.AddDispatchFunction("notify_output_manager",notify_output_manager,
#                        [[[":int", Galaxy.GAL_INT, Galaxy.GAL_KEY_ALWAYS]],
#                        Galaxy.GAL_OTHER_KEYS_NEVER,
#                        Galaxy.GAL_REPLY_NONE, [],
#                        Galaxy.GAL_OTHER_KEYS_NEVER])
    s.AddDispatchFunction("reinitialize",reinitialize,
                          [[], Galaxy.GAL_OTHER_KEYS_NEVER,
                           Galaxy.GAL_REPLY_NONE, [],
                           Galaxy.GAL_OTHER_KEYS_NEVER])
    s.RunServer()

main()
