# This file (c) Copyright 1998 - 2002 The MITRE Corporation
#
# This file is part of the Galaxy Communicator system. It is licensed
# under the conditions described in the file LICENSE in the root
# directory of the Galaxy Communicator system.

import sys,exceptions
import Galaxy,GalaxyIO

def reinitialize(env,dict):
    try:
        env.WriteFrame(Galaxy.Frame("DBQuery",
                                                Galaxy.GAL_CLAUSE,
                                                {":sql_query":"test"}))
    except GalaxyIO.DispatchError,error_frame:
        print error_frame

    return None

def begin_session(env,dict):
    return dict

def handle_event(env,dict):
    return dict

def process_parse(env,dict):
    try:
        resdict = env.DispatchFrame(Galaxy.Frame("gal_be",
                                                Galaxy.GAL_CLAUSE,
                                                {":sql_query":"parse"}))
        print resdict
    except GalaxyIO.DispatchError,error_frame:
        print error_frame
# reply
#    self.env.Reply(new_f)
    return None

def start_inactivity_timeout(env,dict):
    return dict

def cancel_inactivity_timeout(env,dict):
    return dict

def end_session(env,dict):
    return dict

def notify_output_manager(env,dict):
    return dict

# oas in C is -increment i.

#OAS = [("-increment i", "initial increment")]

# Write a wrapper for the usage check.

class LGrlServer(GalaxyIO.Server):
    pass
#    def __init__(self, in_args, server_name = "<unknown>",
#                 default_port = 0,
#                 verbosity = -1,
#                 require_port = 0,
#                 maxconns = 1,
#                 validate = 0,
#                 server_listen_status = GalaxyIO.GAL_CONNECTION_LISTENER,
#                 client_pair_string = None,
#                 session_id = None,
#                 server_locations_file = None,
#                 slf_name = None,
#                 env_class = GalaxyIO.CallEnvironment):
#        GalaxyIO.Server.__init__(self, in_args, server_name,
#                         default_port, verbosity,
#                         require_port, maxconns,
#                         validate, server_listen_status,
#                         client_pair_string, session_id,
#                         server_locations_file,
#                         slf_name,
#                         env_class)

#    def CheckUsage(self, oas_list, args):
#        global InitialIncrement
#        data, out_args = GalaxyIO.Server.CheckUsage(self, OAS + oas_list, args)
#        if data.has_key("-increment"):
#            InitialIncrement = data["-increment"][0]
#            del data["-increment"]
#        return data, out_args

def main():
    s = LGrlServer(sys.argv,"DialogManager",default_port = 17000,verbosity=3)
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
    s.AddDispatchFunction("process_parse",process_parse,
                        [[[":int", Galaxy.GAL_INT, Galaxy.GAL_KEY_ALWAYS]],
                        Galaxy.GAL_OTHER_KEYS_NEVER,
                        Galaxy.GAL_REPLY_NONE, [],
                        Galaxy.GAL_OTHER_KEYS_NEVER])
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
    s.AddDispatchFunction("notify_output_manager",notify_output_manager,
                        [[[":int", Galaxy.GAL_INT, Galaxy.GAL_KEY_ALWAYS]],
                        Galaxy.GAL_OTHER_KEYS_NEVER,
                        Galaxy.GAL_REPLY_NONE, [],
                        Galaxy.GAL_OTHER_KEYS_NEVER])
    s.AddDispatchFunction("reinitialize",reinitialize,
                          [[], Galaxy.GAL_OTHER_KEYS_NEVER,
                           Galaxy.GAL_REPLY_NONE, [],
                           Galaxy.GAL_OTHER_KEYS_NEVER])
    s.RunServer()

main()
