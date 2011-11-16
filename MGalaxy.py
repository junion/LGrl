# This file (c) Copyright 1998 - 2002 The MITRE Corporation
#
# This file is part of the Galaxy Communicator system. It is licensed
# under the conditions described in the file LICENSE in the root
# directory of the Galaxy Communicator system.

# This file contains the Python equivalents of the
# MGal functionality, as far as it's needed.

# binary_utility.c: implemented
# broker_utility.c: partially not (type dispatch included in base server)
# dispatch_utility.c: not needed (included in base server)
# frame_utility.c: not needed (included in base server)
# hub_output_utility.c: implemented
# hub_stream_utility.c: implemented
# server_utility.c: not needed (included in base server)
# stdin_utility.c: implemented

MGAL_DOC = \
"""
MGal_ActivateStdinPoll(obj):            c.Activate()
MGalIO_CreateStdinPoll(prompt, ...):    c = StdinConnection(conn, prompt)
MGalSS_CreateStdinPoll(prompt, ...):    c = StdinConnection(conn, prompt)
MGal_FreeStdinPoll(obj):                [not needed]
MGal_PollStdin(obj):                    c.Callback() (approximately)
MGal_GetStdinPollData(...):             [not needed; use instance attributes]
MGal_SetStdinPollData(...):             [not needed; use instance attributes]
MGal_SetStdinPollPrompt(c, prompt):     c.prompt = prompt

MGal_CreateFullFrame(name, type, ...):  [not needed]

MGal_AddOutgoingBrokering(port, f, ...): [not implemented]
MGal_AddBrokerDTHandler(dt, val, h):     [not implemented]
MGal_AddIncomingBrokering(fr, ms, data): [not needed]

MGal_AddBinaryDataType(t, encoder, decoder):  p = OpaqueMapper(); p.AddBinaryDataType(t, class)
MGal_OpaqueObject(obj, dt):                   p.OpaqueObject(obj, dt)
MGal_GetOpaque(f, key, dt):                   p.GetOpaque(f, key)
MGal_GetOpaqueWarn(f, key, dt):               p.GetOpaque(f, key, dt)
"""


import GalaxyIO, Galaxy, sys, string, os, socket

##################################################
#
# Binary data utilities
#
##################################################

import pickle

# Default encode/decode is pickling.

class OpaqueMapper:
    def __init__(self):
        self.table = {}
        self.type_table = {}
        self.inverse_type_table = {}
        self.type_counter = 0
    def AddBinaryDataType(self, t, cl):
        # This way, I can use anything as the type, including
        # a class itself.
        self.table[t] = cl
        self.type_table[t] = self.type_counter
        self.inverse_type_table[self.type_counter] = t
        self.type_counter = self.type_counter + 1
    def OpaqueObject(self, obj, t):
        s = self.table[t](to_encode = obj)._FullEncode()
        o = Galaxy.BinaryObject(Galaxy.GAL_BINARY, s)
        return Galaxy.Frame("__opaque__", Galaxy.GAL_CLAUSE,
                            {":type": self.type_table[t], ":data": o})
    def GetOpaque(self, fr, key, t = None):
        if t: t = self.type_table[t]
        f = fr[key]
        if (not f) or \
           (f.name != "__opaque__") or \
           (not f.has_key(":type")) or \
           (not f.has_key(":data")):
            return None
        if (t != None) and (t != f[":data"]):
            raise Galaxy.ObjectTypeError, (t, f[":data"])
        o = string.joinfields(map(chr, f[":data"]), "")
        return self.table[self.inverse_type_table[f[":type"]]](to_decode = o)._FullDecode()

class OpaqueClass:
    def __init__(self, to_encode = None, to_decode = None):
        self.encoded = to_decode
        self.decoded = to_encode
    def _FullEncode(self, obj = None):
        if self.encoded and ((obj == None) or (obj == self.decoded)):
            self.decoded = obj
            return self.encoded
        elif self.decoded and obj == None:
            self.encoded = self.Encode(self.decoded)
            return self.encoded
        elif self.decoded or obj:
            self.decoded = obj
            self.encoded = self.Encode(self.decoded)
            return self.encoded
        else:
            raise OpaqueClassError, "No object to encode"
    def Encode(self, obj):
        return pickle.dumps(obj)
    def _FullDecode(self, obj = None):
        if self.decoded and ((obj == None) or (obj == self.encoded)):
            self.encoded = obj
            return self.decoded
        elif self.encoded and obj == None:
            self.decoded = self.Decode(self.encoded)
            return self.decoded
        elif self.encoded or obj:
            self.encoded = obj
            self.decoded = self.Decode(self.encoded)
            return self.decoded
        else:
            raise OpaqueClassError, "No object to decode"
    def Decode(self, rep):
        return pickle.loads(rep)

##################################################
#
# Stdin utility
#
##################################################

# I'll build a "fake" connection and add it to the server.

# This needs to take Disconnect, call the Register method on
# the server with the fileno for stdin, call the Unregister
# method if it ever dies, and define the Callback method.

# 10/18/00: Clarified that this takes a call environment as an
# argument, not a connection.

class StdinConnection:

    def __init__(self, env, prompt, activate = 0):
        self.env = env
        self.prompt = prompt
        self.active = 0
        if activate:
            self.Activate()

    def Activate(self):
        if not self.active:
            sys.stdout.write(self.prompt)
            sys.stdout.flush()
            self.active = 1
            self.env.server.ReaderRegister(self, sys.stdin.fileno())

    def Callback(self):

        # Only called when there's input; so first, disable
        # the registration.
        self.env.server.ReaderUnregister(sys.stdin.fileno())

        # Now, read characters from stdin
        l = sys.stdin.readline()[:-1]
        f = self.CreateFrame(l)
        self.env.WriteFrame(f)
        self.active = 0

    def CreateFrame(self, str):
        return None

    def Disconnect(self):
        if self.active:
            self.env.server.ReaderUnregister(sys.stdin.fileno())
            self.active = 0
