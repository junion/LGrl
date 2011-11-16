# This file (c) Copyright 1998 - 2002 The MITRE Corporation
#
# This file is part of the Galaxy Communicator system. It is licensed
# under the conditions described in the file LICENSE in the root
# directory of the Galaxy Communicator system.

# This covers the basics in libGalaxy/io and libGalaxy/ServerStub.

# ip_util.c: implemented
# broker_data.c: implemented as object, much is not needed
# hub_server.c: implemented
# sockqueue.c: implemented (also binary_io.c), much is not needed

# frame_util.c: implemented
# generic-server.c: implemented

GALIO_DOC = \
"""
GalIO_IPAddress():                    IPAddress()

GalIO_GetBrokerSocket(b):             [not implemented]
GalIO_GetBrokerCallerData(b):         [not needed; use instance attributes]
GalIO_BrokerSetFinalizer(b, f, data): [not implemented]
GalIO_BrokerWriteFrame(b, f):         b.Write(f)
GalIO_BrokerWriteString(b, s):        b.Write(s)
GalIO_BrokerWriteBinary(b, data, n):  b.Write(data)
GalIO_BrokerWriteInt16(b, data, n):   b.Write(data)
GalIO_BrokerWriteInt32(b, data, n):   b.Write(data)
GalIO_BrokerWriteInt64(b, data, n):   b.Write(data)
GalIO_BrokerWriteFloat32(b, data, n): b.Write(data)
GalIO_BrokerWriteFloat64(b, data, n): b.Write(data)
GalIO_BrokerDataDone(b):              b.DataDone()
GalIO_BrokerDataOutDone(b):           b.DataDone()
GalIO_BrokerDataOutInit(...):         b = BrokerDataOut(conn, timeout)
GalIO_CommBrokerDataInInit(...):      b = BrokerDataIn(conn, host, port, frame)
GalIO_BrokerStructQueuePop(b):        [not needed; no broker queues in Python]
GalIO_SetBrokerActive(b):             [not needed; no broker queues in Python]
GalIO_BrokerStructQueueAppend(...):   [not needed; no broker queues in Python]
GalIO_GetBrokerFrame(...):            [not implemented]
GalIO_BrokerStructDequeue(...):       [not needed; no broker queues in Python]
GalIO_FrameSetBrokerCallID(f, call_id): [not implemented]

GalIO_DestroyCommStruct(conn):        [not needed]
GalIO_GetServerListenPort(s):         s.ListenPort()
GalIO_GetCommSocket(conn):            [not implemented]
GalIO_CloseCommSocket(conn):          [not implemented]
GalIO_GetCommHost(conn):              [not implemented]
GalIO_GetCommFrame(conn):             [not implemented]
GalIO_GetCommServerData(conn):        [not needed; use instance attributes]
GalIO_SetCommDone(conn):              [not implemented]
GalIO_ResetCommSockets(s):            [not implemented]
GalIO_CommWriteFrame(c, f, block):    c.WriteFrame(f)
GalIO_CommDispatchFrame(c, f, key):   c.DispatchFrame(f)
GalIO_DispatchViaHub(c, f, msg):      c.DispatchFrame(f)
GalIO_CommFlushOutQueue(conn):        [not implemented]
GalIO_CommReadReady(conn):            [not implemented]
GalIO_ClientInit(...):                [not implemented]
GalIO_OutHandler(conn):               c.Callback() (approximately)
GalIO_InHandler(conn):                c.Callback() (approximately)
GalIO_ConnectionPoll(conn):           [not implemented; polling by select]
GalIO_ServerHandler(conn):            c.Callback() (approximately)
GalIO_HubHandler(conn):               [not implemented]
GalIO_ServerInit(port, require_port, ...): s = Server(port, require_port)
GalIO_SetServerDefaultPort(..):       [not implemented]
GalIO_CommValidating(c):              c.Validating()
GalIO_DestroyServerStruct(s):         [not implemented]
GalIO_EnableDispatchFnValidation(s):  s.EnableValidation()
GalIO_ServerPoll(s):                  [not implemented; polling by select]
GalIO_SetCommData(c, data):           [not needed; use instance attributes]
GalIO_ServerUsesTimedTasks(s):        [not implemented; polling by select]
GalIO_SetServerDone(s):               [not needed]
GalIO_GetServerDefaultPort(s):        [not implemented]
GalIO_GetServerData(s):               [not needed; use instance attributes]
GalIO_GetCommServerName(c):           c.server.ServerName()
GalIO_SetServerData(s, data):         [not needed; use instance attributes]
GalIO_SetServerMaxConnections(s, m):  s.MaxConnections(m)
GalIO_GetError(fr):                   [not needed; just catch DispatchError]
GalIO_SetServerName(s, name):         s.ServerName(name)
GalIO_GetUniqueConnection(s):         [not implemented]
GalIO_GetServerMaxConnections(s):     s.MaxConnections()
GalIO_GetCommData(c):                 [not needed; use instance attributes]
GalIO_GetServerName(s):               s.ServerName()

Gal_InitializeServerDefaults(name, port, fn_map): [not needed; use Server]
Gal_GetServerPort():                  [not implemented]

GalSS_AddDispatchFunction(...):       s.AddDispatchFunction(...)
GalSS_StartAndRunServer(s):           s.RunServer()
GalSS_ExtractServerArgs(...):         [not implemented]
GalSS_EnvError(e, errdesc):           [not implemented; just raise an error]
GalSS_EnvDestroyToken(e):             e.DestroyToken()
GalSS_EnvGetCommData(e):              [not needed; use instance attributes]
GalSS_InitializeServerDefaults(...):  [not implemented]
GalSS_EnvComm(e):                     e.conn
GalSS_CmdlineInitializeServer(...):   Server(...)
GalSS_EnvSetCommData(e, data):        [not needed; use instance attributes]
GalSS_EnvWriteFrame(e, fr):           e.WriteFrame(fr)
GalSS_InitializeServerFromServerArgs(...): [not implemented]
GalSS_InitializeServer(...):          Server(...)
GalSS_EnvDispatchFrame(e, fr):        e.DispatchFrame(fr)
"""

import socket, string, select, sys, types, time, copy, traceback
import signal
from Galaxy import Frame, _Sym, GetObjectType, _EncodingArray, \
     GAL_CLAUSE, BinaryObject, \
     GAL_FRAME, GAL_STRING, GAL_BINARY, GAL_INT_16, \
     GAL_INT_32, GAL_INT_64, GAL_FLOAT_32, GAL_FLOAT_64, \
     GAL_LIST, GAL_FLOAT, GAL_INT, GAL_SYMBOL, GAL_PROXY, \
     ObjectTypeString, GAL_KEY_ALWAYS, GAL_KEY_SOMETIMES, \
     GAL_OTHER_KEYS_MAYBE, GAL_OTHER_KEYS_NEVER, GAL_REPLY_PROVIDED, \
     GAL_REPLY_NONE, GAL_REPLY_UNKNOWN, _ValToObject, _ObjectToVal

from cGalaxy import GAL_SERVER_READS_ONLY_FROM_SESSION, \
     GAL_SESSION_WRITES_ONLY_TO_SERVER, \
     GAL_SERVER_WRITES_ONLY_TO_SESSION, \
     GAL_PERMANENT_LOCK

import SLSUtil, cGalaxy

##################################################
#
# Utilities
#
##################################################

def IPAddress():
    return cGalaxy.GalIO_IPAddress()

from cGalaxy import GAL_OBJECT_MSG_TYPE, GAL_MESSAGE_MSG_TYPE, \
     GAL_REPLY_MSG_TYPE, GAL_DESTROY_MSG_TYPE, GAL_POSTPONE_MSG_TYPE, \
     GAL_BROKER_START_MSG_TYPE, GAL_BROKER_END_MSG_TYPE, \
     GAL_ERROR_MSG_TYPE, GAL_DISCONNECT_MSG_TYPE, \
     GAL_APPLICATION_ERROR, GAL_NO_OPNAME_ERROR, \
     GAL_TRANSMISSION_ERROR, GAL_RECEPTION_ERROR, \
     GAL_SERVER_DOWN_ERROR, GAL_NO_FRAME_ERROR, \
     GAL_CONN_REJECTION_ERROR, \
     GAL_CONNECTION_LISTENER, GAL_HUB_CLIENT, GAL_SERVER_TYPE_MASK, \
     GAL_HUB_CLIENT_CONNECT_FAILURE_MASK, \
     GAL_HUB_CLIENT_CONNECT_FAILURE_RETRY, \
     GAL_HUB_CLIENT_CONNECT_FAILURE_NOOP, \
     GAL_HUB_CLIENT_CONNECT_FAILURE_SHUTDOWN, \
     GAL_HUB_CLIENT_DISCONNECT_MASK, \
     GAL_HUB_CLIENT_DISCONNECT_RETRY, \
     GAL_HUB_CLIENT_DISCONNECT_SHUTDOWN, \
     GAL_HUB_CLIENT_DISCONNECT_NOOP, \
     GAL_BROKER_DATA_DONE_EVENT, \
     GAL_BROKER_ABORT_EVENT, \
     GAL_BROKER_DESTRUCTION_EVENT, \
     GAL_BROKER_CONNECTION_EVENT

##################################################
#
# Broker connections
#
##################################################

BrokerInitError = "BrokerInitError"
BrokerProcessingError = "BrokerProcessingError"

# Connections, servers and brokers all call Register(),
# which takes an object and a file descriptor number (which need
# not be used). The object needs to take a Callback() method,
# as well as a Disconnect().

# Servers can change the way they loop and poll by changing
# the behavior of their Register() and Run() methods.

class BrokerData:
    def __init__(self, conn):
        self.conn = conn
        # for access to debug
        self.debug = self.conn.debug
        self.server = conn.server
        self.ostream = self.conn.ostream
        self.disconnected = 0

    # Register() is called as a side effect of
    # broker creation.

    def ReaderRegister(self, sock_num):
        if self not in self.conn.brokers:
            self.conn.brokers.append(self)
        self.conn.server.ReaderRegister(self, sock_num)

    def WriterRegister(self, sock_num):
        if self not in self.conn.brokers:
            self.conn.brokers.append(self)
        self.conn.server.WriterRegister(self, sock_num)

    def ReaderUnregister(self, sock_num):
        self.conn.server.ReaderUnregister(sock_num)

    def WriterUnregister(self, sock_num):
        self.conn.server.WriterUnregister(sock_num)

    # _Disconnect() is called by the broker finalizer.
    # By default, it doesn't force the broker to be
    # destroyed. Note that it destroys the broker
    # struct if force_destroy is 1, but it makes sure
    # to mark itself as disconnected first, so that
    # it's not called by recursion. I should also unset
    # the finalizer, just to be sure.

    def _Disconnect(self, force_destroy = 0):
        if force_destroy and self.c_broker:
            self.DataDone()
            cGalaxy.GalIO_DestroyBrokerStruct(self.c_broker)
        elif not self.disconnected:
            c_broker = self.c_broker
            if self in self.conn.brokers:
                self.conn.brokers.remove(self)
            self.c_broker = None
            self.disconnected = 1

    # This can be called by anyone, and it will
    # force the broker struct to be destroyed.
    def Disconnect(self):
        self._Disconnect(force_destroy = 1)

    # Fn is a function of no arguments (use lambdas)
    def AddCallback(self, event, fn):
        cGalaxy.GalIO_PyAddBrokerCallback(self.c_broker,
                                          event, fn)

class BrokerDataOut(BrokerData):
    def __init__(self, conn, timeout):
        BrokerData.__init__(self, conn)
        self.c_broker = cGalaxy.GalIO_PyBrokerDataOutInit(conn.c_conn, timeout)
        cGalaxy.GalIO_PyAddBrokerCallback(self.c_broker,
                                          cGalaxy.GAL_BROKER_DESTRUCTION_EVENT,
                                          self.DisconnectCallback)
        if self.c_broker:
            self.port = cGalaxy.GalIO_GetBrokerListenPort(self.c_broker)
            self.call_id = cGalaxy.GalIO_GetBrokerCallID(self.c_broker)
            self.conn.brokers.append(self)
        else:
            raise BrokerInitError, "no broker"

    def DataDone(self):
        cGalaxy.GalIO_BrokerDataOutDone(self.c_broker)

    def PopulateFrame(self, f, host_key, port_key):
        f[host_key] = IPAddress()
        f[port_key] = self.port
        f[":call_id"] = self.call_id

    def Write(self, obj):
        # We need to type the object and write it appropriately.
        in_t = GetObjectType(obj)
        if in_t in [GAL_BINARY, GAL_INT_16, GAL_INT_32, GAL_INT_64, \
                    GAL_FLOAT_32, GAL_FLOAT_64]:
            # It's an array. We can use tostring() to
            # generate something appropriate for digesting and
            # undigesting.
            s = obj.tostring()
            if in_t is GAL_BINARY:
                cGalaxy.GalIO_BrokerWriteBinary(self.c_broker, s, len(obj))
            elif in_t is GAL_INT_16:
                cGalaxy.GalIO_BrokerWriteInt16(self.c_broker, s, len(obj))
            elif in_t is GAL_INT_32:
                cGalaxy.GalIO_BrokerWriteInt32(self.c_broker, s, len(obj))
            elif in_t is GAL_INT_64:
                cGalaxy.GalIO_BrokerWriteInt64(self.c_broker, s, len(obj))
            elif in_t is GAL_FLOAT_32:
                cGalaxy.GalIO_BrokerWriteFloat32(self.c_broker, s, len(obj))
            elif in_t is GAL_FLOAT_64:
                cGalaxy.GalIO_BrokerWriteFloat64(self.c_broker, s, len(obj))
        elif in_t == GAL_FRAME:
            frame = obj._PythonToC()
            cGalaxy.GalIO_BrokerWriteFrame(self.c_broker, frame)
            cGalaxy.Gal_FreeFrame(frame)
        elif in_t == GAL_STRING:
            cGalaxy.GalIO_BrokerWriteString(self.c_broker, obj)
        # Current shortcut for the rest of stuff.
        elif in_t in [GAL_LIST, GAL_FLOAT, GAL_INT, GAL_SYMBOL]:
            # Build an object.
            c_obj = _ValToObject(obj)
            cGalaxy.GalIO_BrokerWriteObject(self.c_broker, c_obj)
            cGalaxy.Gal_FreeObject(c_obj)
        else:
            raise ObjectEncodingError, ("Can't encode", obj)

    # Return values are as follows:
    # 0: still polling
    # 1: it's done, and the broker has been destroyed.
    # This no longer ever fails. It doesn't have
    # a write socket associated with it, but rather there
    # are hidden connections in the broker.

    # This should all be handled in the callback handler now.

    def Callback(self):
        cGalaxy.GalIO_BrokerDataOutCallbackHandler(self.c_broker)

    def DisconnectCallback(self):
        self._Disconnect()

    def Expire(self):
        cGalaxy.GalIO_ForceBrokerExpiration(self.c_broker)

# For the incoming broker, I need to set up the callback.

class BrokerDataIn(BrokerData):
    def __init__(self, env_or_conn, host = None,
                 port = None, frame = None,
                 proxy = None):
        if isinstance(env_or_conn, Connection):
            conn = env_or_conn
            env = None
        elif isinstance(env_or_conn, CallEnvironment):
            conn = env_or_conn.conn
            env = env_or_conn
        else:
            raise BrokerInitError, "neither connection nor environment"
        if (proxy is not None) and (env is None):
            raise BrokerInitError, "proxy requires environment"
        if (not proxy) and (not (host and port)):
            raise BrokerInitError, "no host and port for client"
        BrokerData.__init__(self, conn)
        callback_fn = lambda dt, obj, s = self: s._HandleBrokerData(dt, obj)
        # Environments have to be copied, so that they don't
        # change between the time the broker is saved and
        # the time it's invoked.
        if proxy:
            self.c_broker = cGalaxy.GalSS_PyEnvBrokerProxyInInit(env.c_env,
                                                                 proxy.c_proxy,
                                                                 callback_fn)
        elif env:
            c_frame = frame._PythonToC()
            self.c_broker = cGalaxy.GalSS_PyEnvBrokerDataInInit(env.c_env,
                                                                host, port,
                                                                c_frame,
                                                                callback_fn)
            cGalaxy.Gal_FreeFrame(c_frame)
        else:
            c_frame = frame._PythonToC()
            self.c_broker = cGalaxy.GalIO_PyCommBrokerDataInInit(conn.c_conn,
                                                                 host, port,
                                                                 c_frame,
                                                                 callback_fn)
            cGalaxy.Gal_FreeFrame(c_frame)
        if self.c_broker:
            cGalaxy.GalIO_PyAddBrokerCallback(self.c_broker,
                                              cGalaxy.GAL_BROKER_DESTRUCTION_EVENT,
                                              self.DisconnectCallback)
            cGalaxy.GalIO_PyAddBrokerCallback(self.c_broker,
                                              cGalaxy.GAL_BROKER_DATA_DONE_EVENT,
                                              self.DataDoneCallback)
            cGalaxy.GalIO_PyAddBrokerCallback(self.c_broker,
                                              cGalaxy.GAL_BROKER_ABORT_EVENT,
                                              self.AbortCallback)
            if env:
                self.env = copy.copy(env)
                self.env.c_env = cGalaxy.GalSS_BrokerGetEnvironment(self.c_broker)
                cGalaxy.GalSS_EnvLock(self.env.c_env)
            else:
                self.env = None
            self.c_socknum = cGalaxy.GalIO_GetBrokerSocket(self.c_broker)
            self.ReaderRegister(self.c_socknum)
            cGalaxy.GalIO_SetBrokerActive(self.c_broker)
        else:
            raise BrokerInitError, "no client"

    # Return values are:
    # 1 if the broker is done and has been destroyed,
    # 0 if not done
    # -1 if error was encountered and the broker has been destroyed.

    # This should all happen in the callbacks now.

    def Callback(self):
        # Don't do read blocking right now.
        cGalaxy.GalIO_BrokerDataInCallbackHandler(self.c_broker, 0)

    def DataDone(self):
        cGalaxy.GalIO_BrokerDataDone(self.c_broker)

    # By default, this function doesn't force
    # the broker to shut down.

    def _Disconnect(self, force_destroy = 0):
        if force_destroy:
            BrokerData._Disconnect(self, force_destroy = force_destroy)
        elif not self.disconnected:
            if self.c_socknum is not None:
                self.ReaderUnregister(self.c_socknum)
                self.c_socknum = None
            BrokerData._Disconnect(self, force_destroy = force_destroy)

    def DisconnectCallback(self):
        self._Disconnect()

    def DataDoneCallback(self):
        pass

    def AbortCallback(self):
        pass

    def _HandleBrokerData(self, dt, obj):
        # I now consistently build a Gal_Object to pass
        # in here.
        o = _ObjectToVal(obj)
        if dt == GAL_FRAME:
            self.HandleFrame(o)
        elif dt == GAL_STRING:
            self.HandleString(o)
        elif dt == GAL_SYMBOL:
            self.HandleSymbol(o)
        elif dt == GAL_FLOAT:
            self.HandleFloat(o)
        elif dt == GAL_INT:
            self.HandleInt(o)
        elif dt == GAL_LIST:
            self.HandleList(o)
        elif dt == GAL_BINARY:
            self.HandleBinary(o)
        elif dt == GAL_INT_16:
            self.HandleInt16(o)
        elif dt == GAL_INT_32:
            self.HandleInt32(o)
        elif dt == GAL_INT_64:
            self.HandleInt64(o)
        elif dt == GAL_FLOAT_32:
            self.HandleFloat32(o)
        elif dt == GAL_FLOAT_64:
            self.HandleFloat64(o)
        elif dt == GAL_PROXY:
            self.HandleProxy(o)
    def HandleFrame(self, obj):
        if self.env:
            self.EnvHandleFrame(self.env, obj)
        else:
            raise BrokerProcessingError, "frame"
    def EnvHandleFrame(self, env, obj):
        raise BrokerProcessingError, "frame"
    def HandleString(self, obj):
        if self.env:
            self.EnvHandleString(self.env, obj)
        else:
            raise BrokerProcessingError, "string"
    def EnvHandleString(self, env, obj):
        raise BrokerProcessingError, "string"
    def HandleSymbol(self, obj):
        if self.env:
            self.EnvHandleSymbol(self.env, obj)
        else:
            raise BrokerProcessingError, "symbol"
    def EnvHandleSymbol(self, env, obj):
        raise BrokerProcessingError, "symbol"
    def HandleFloat(self, obj):
        if self.env:
            self.EnvHandleFloat(self.env, obj)
        else:
            raise BrokerProcessingError, "float"
    def EnvHandleFloat(self, env, obj):
        raise BrokerProcessingError, "float"
    def HandleInt(self, obj):
        if self.env:
            self.EnvHandleInt(self.env, obj)
        else:
            raise BrokerProcessingError, "int"
    def EnvHandleInt(self, env, obj):
        raise BrokerProcessingError, "int"
    def HandleList(self, obj):
        if self.env:
            self.EnvHandleList(self.env, obj)
        else:
            raise BrokerProcessingError, "list"
    def EnvHandleList(self, env, obj):
        raise BrokerProcessingError, "list"
    def HandleBinary(self, obj):
        if self.env:
            self.EnvHandleBinary(self.env, obj)
        else:
            raise BrokerProcessingError, "binary"
    def EnvHandleBinary(self, env, obj):
        raise BrokerProcessingError, "binary"
    def HandleInt16(self, obj):
        if self.env:
            self.EnvHandleInt16(self.env, obj)
        else:
            raise BrokerProcessingError, "int 16"
    def EnvHandleInt16(self, env, obj):
        raise BrokerProcessingError, "int 16"
    def HandleInt32(self, obj):
        if self.env:
            self.EnvHandleInt32(self.env, obj)
        else:
            raise BrokerProcessingError, "int 32"
    def EnvHandleInt32(self, env, obj):
        raise BrokerProcessingError, "int 32"
    def HandleInt64(self, obj):
        if self.env:
            self.EnvHandleInt64(self.env, obj)
        else:
            raise BrokerProcessingError, "int 64"
    def EnvHandleInt64(self, env, obj):
        raise BrokerProcessingError, "int 64"
    def HandleFloat32(self, obj):
        if self.env:
            self.EnvHandleFloat32(self.env, obj)
        else:
            raise BrokerProcessingError, "float 32"
    def EnvHandleFloat32(self, env, obj):
        raise BrokerProcessingError, "float 32"
    def HandleFloat64(self, obj):
        if self.env:
            self.EnvHandleFloat64(self.env, obj)
        else:
            raise BrokerProcessingError, "float 64"
    def EnvHandleFloat64(self, env, obj):
        raise BrokerProcessingError, "float 64"
    def HandleProxy(self, obj):
        if self.env:
            self.EnvHandleProxy(self.env, obj)
        else:
            raise BrokerProcessingError, "proxy"
    def EnvHandleProxy(self, env, obj):
        raise BrokerProcessingError, "proxy"

##################################################
#
# Broker proxies
#
##################################################

# I never want to make use of the C cache in the
# outbound or inbound proxies, since all the actual
# objects I manipulate are native. So I need to recreate
# the cache natively in Python.

# There's a slight problem with distinguishing
# between out proxies and in proxies. The problem is
# that when we read frames from C, we will assume
# in proxies by default. However, there are probably
# some cases where that will be a mistaken assumption.
# I can't think of them yet, though.

class BrokerProxy:

    _gal_type = GAL_PROXY

    def __init__(self, _gal_proxy, env = None):
        self.c_proxy = _gal_proxy
        self.env = env

        if not self.c_proxy:
            raise BrokerInitError, "no proxy"

    def __del__(self):
        if self.c_proxy:
            cGalaxy.GalSS_FreeBrokerProxy(self.c_proxy)

    def AddCallback(self, event, fn):
        if self.c_proxy:
            c_broker = cGalaxy.GalSS_BrokerProxyBroker(self.c_proxy)
            cGalaxy.GalIO_PyAddBrokerCallback(c_broker,
                                              event, fn)

    def Register(self):
        self.env.conn.proxies.append(self)

    def Disconnect(self):
        if self in self.env.conn.proxies:
            self.env.conn.proxies.remove(self)

class BrokerProxyOut(BrokerProxy):

    def __init__(self, env, timeout, obj = None, type = None):
        if (obj is None) and (type is None):
            raise BrokerInitError, "either obj or type required"
        if (obj is not None) and (type is not None) and \
           type != GetObjectType(obj):
            raise BrokerInitError, "obj and type don't match"
        if (type is None):
            type = GetObjectType(obj)
        self.type = type

        BrokerProxy.__init__(self, cGalaxy.GalSS_ProxifyObjectType(env.c_env,
                                                                   type, -1, timeout), env)
        self.Register()
        # Now, we set up the cache and write the object. Be sure
        # to write the list elements if it's an element of
        # type list.
        if obj is not None:
            self.obj = obj
            if self.type == GAL_LIST:
                for elt in obj:
                    cGalaxy.GalSS_ProxyWrite(self.c_proxy,
                                             _ValToObject(elt), 1)
            else:
                cGalaxy.GalSS_ProxyWrite(self.c_proxy, _ValToObject(obj), 1)
        else:
            self.obj = None

    def Write(self, obj):
        # If there's an obj, add it if possible. Write
        # it to the proxy.
        res = cGalaxy.GalSS_ProxyWrite(self.c_proxy, _ValToObject(obj), 1)
        if res < 0:
            raise BrokerProcessingError, "can't write obj"
        elif self.obj is not None:
            # This will only be a list or an array type.
            # No other types can stream, and we never cache
            # atomic objects which are written by type.
            t = GetObjectType(self.obj)
            if t == GAL_LIST:
                self.obj.append(obj)
            elif t in [GAL_BINARY, GAL_INT_16, GAL_INT_32, GAL_INT_64, \
                       GAL_FLOAT_32, GAL_FLOAT_64]:
                self.obj = self.obj + obj

    def DataDone(self):
        cGalaxy.GalSS_ProxyDone(self.c_proxy)

    def SelfTerminates(self):
        return cGalaxy.GalSS_ProxySelfTerminates(self.c_proxy)

    def Callback(self):
        res = cGalaxy.GalSS_BrokerProxyOutCallbackHandler(self.c_proxy)
        if res == 1:
            # We're done. Make sure we're removed.
            self.Disconnect()

    def Pollable(self):
        return (self.c_proxy is not None) and \
               cGalaxy.GalSS_BrokerProxyWriteReady(self.c_proxy)

    def Expire(self):
        cGalaxy.GalSS_ForceProxyExpiration(self.c_proxy)

class BrokerProxyInStream:
    def __init__(self, bp, env):
        self.bp = bp
        self.env = env
        self.ostream = env.conn.ostream
        self.type = cGalaxy.GalSS_BrokerProxyObjectType(bp.c_proxy)
    def HandleObject(self, obj):
        pass
    def DataDoneCallback(self):
        pass
    def AbortCallback(self):
        pass

class BrokerProxyIn(BrokerProxy):

    def __init__(self, _gal_proxy):
        # Make sure we COPY THE PROXY. The proxy will
        # always be freed here.
        BrokerProxy.__init__(self, cGalaxy.GalSS_CopyBrokerProxy(_gal_proxy))

    def ObjectType(self):
        return cGalaxy.GalSS_BrokerProxyObjectType(self.c_proxy)

    def Pollable(self):
        return (self.c_proxy is not None) and \
               cGalaxy.GalSS_BrokerProxyReadReady(self.c_proxy)

    def UnproxifyObject(self, env):
        # Later processing may require an environment here.
        self.env = env
        c_obj = cGalaxy.GalSS_UnproxifyObject(env.c_env, self.c_proxy)
        if c_obj:
            obj = _ObjectToVal(c_obj)
            cGalaxy.Gal_FreeObject(c_obj)
            return obj
        else:
            return None

    def Unproxify(self, env, proxy_stream_type = BrokerProxyInStream,
                  immediate = 1):
        self.bp_s = proxy_stream_type(self, env)
        callback_fn = lambda obj, s = self.bp_s: s.HandleObject(_ObjectToVal(obj))
        cGalaxy.GalSS_PyUnproxify(env.c_env,
                                  self.c_proxy,
                                  callback_fn,
                                  self.bp_s.DataDoneCallback,
                                  self.bp_s.AbortCallback,
                                  immediate)
        self.env = env
        self.c_socknum = cGalaxy.GalSS_GetBrokerProxySocket(self.c_proxy)
        self.env.conn.server.ReaderRegister(self, self.c_socknum)
        self.Register()

    def Disconnect(self):
        if self.c_socknum:
            self.env.conn.server.ReaderUnregister(self.c_socknum)
            self.c_socknum = None
        BrokerProxy.Disconnect(self)

    def Callback(self):
        res = cGalaxy.GalSS_BrokerProxyInCallbackHandler(self.c_proxy)
        if res == 1 and self.env:
            # We're done. Make sure we're removed.
            self.Disconnect()

##################################################
#
# Connections
#
##################################################

# This takes the place of the GalIO_CommStruct, but
# because the server handles multiple connections, the
# server object is distinct.

# I'm going to have to eviscerate this object and move
# the MGal-like behavior into MGalaxy.py.

ConnectionDead = 'ConnectionDead'
DispatchError = 'DispatchError'
WriteError = 'WriteError'

# For backward compatibility, I'm going to support the
# conn_class argument as actually being the class of a
# CALL ENVIRONMENT, and the Connection class here will
# also be the root CALL ENVIRONMENT class. I'll add a
# new CommConnection class to support what the connection
# class used to do.

# SAM 9/22/00: No longer. The call environment has gone
# away, and I no longer need to pretend this anymore.
# For compability, I'll make the connection's "conn" attribute
# point to itself.

# This is for the Hub mimic and the server side.

class BasicConnection:
    def __init__(self, ostream, debug = 0):
        self.disconnected = 0
        self.ostream = ostream
        self.debug = debug
        self.c_conn = None

    def AddCConnection(self, c_conn):
        self.c_conn = c_conn
        cGalaxy.GalIO_PyAddConnectionCallback(self.c_conn,
                                              cGalaxy.GAL_CONNECTION_SHUTDOWN_EVENT,
                                              lambda s = self: s._Disconnect())

    def _Disconnect(self, force_destroy = 0):
        if force_destroy and self.c_conn:
            # We can no longer unset the disconnect callback, so
            # we should just let it call back.
            cGalaxy.GalIO_SetCommDone(self.c_conn)
            cGalaxy.GalIO_DestroyCommStruct(self.c_conn)
        elif not self.disconnected:
            self.c_conn = None
            self.disconnected = 1

    def Disconnect(self):
        self._Disconnect(force_destroy = 1)

    def WriteMessage(self, f, msg_type):
        if not self.c_conn:
            raise ConnectionDead
        frame = f._PythonToC()
        res = cGalaxy.GalIO_CommWriteMessage(self.c_conn, frame, msg_type, 0)
        cGalaxy.Gal_FreeFrame(frame)
        if res == -1:
            raise WriteError, "Couldn't write message"

    def WriteFrame(self, f):
        if not self.c_conn:
            raise ConnectionDead
        frame = f._PythonToC()
        res = cGalaxy.GalIO_CommWriteFrame(self.c_conn, frame, 0)
        cGalaxy.Gal_FreeFrame(frame)
        if res == -1:
            raise WriteError, "Couldn't write frame"

    def DispatchFrame(self, out_frame):
        if not self.c_conn:
            raise ConnectionDead
        f = out_frame._PythonToC()
        res_array = cGalaxy.GBGalIO_DispatchViaHub(self.c_conn, f)
        return self._PostprocessReturn(res_array, f)

    def _PostprocessReturn(self, res_array, f):
        c_f = cGalaxy.GBGal_ResultArrayFrame(res_array)
        msg_type = cGalaxy.GBGal_ResultArrayMsgType(res_array)
        cGalaxy.GBGal_FreeResultArray(res_array)
        if c_f:
            r = Frame(_gal_frame = c_f)
        else:
            r = None
        if f != c_f:
            cGalaxy.Gal_FreeFrame(f)
        cGalaxy.Gal_FreeFrame(c_f)
        if msg_type == GAL_ERROR_MSG_TYPE:
            raise DispatchError, r
        return r

# We want to register this connection. In the
# C bindings, we'll use the data slot to store the
# python disconnect callback.

class Connection(BasicConnection):

    def __init__(self, server, c_conn):
        BasicConnection.__init__(self, server.ostream, \
                                 server.debug)
        self.c_socknum = None
        self.server = server
        self.brokers = []
        self.proxies = []
        # I won't use the broker startup callbacks, since I have
        # complete control over those.
        self.AddCConnection(c_conn)

    def AddCConnection(self, c_conn):
        BasicConnection.AddCConnection(self, c_conn)
        self.c_socknum = cGalaxy.GalIO_GetCommSocket(c_conn)
        self.server.conns[c_conn] = self
        self.server.ReaderRegister(self, self.c_socknum)

    # Return values are
    # -1 means an error was encountered and the connection has been destroyed.
    # 0 means we're in the midst of things.
    # 1 means we're done and the connection has been destroyed.
    # These should all be handled in the callbacks now.

    def Callback(self):
        cGalaxy.GalIO_ConnectionCallbackHandler(self.c_conn, 0)

    def _Disconnect(self, force_destroy = 0):
        c_conn = self.c_conn
        disconnected = self.disconnected
        BasicConnection._Disconnect(self, force_destroy)
        if (not (force_destroy and c_conn)) and \
           (not disconnected):
            # If we didn't truly shut it down, and
            # we weren't marked as disconnected, then
            # shut down the brokers and unregister the
            # socket.
            if self.c_socknum is not None:
                self.server.ReaderUnregister(self.c_socknum)
                self.c_socknum = None
            if c_conn is not None:
                del self.server.conns[c_conn]
            # Shut down all associated brokers.
            # Copy the list, because it's surgically altered
            # in the broker disconnect.
            for b in self.brokers[:]:
                b.Disconnect()
            for b in self.proxies[:]:
                b.Disconnect()

    def PollConnection(self):
        if self.c_conn is not None:
            if cGalaxy.GalIO_CommReadReady(self.c_conn) or \
               cGalaxy.GalIO_CommWriteReady(self.c_conn):
                self.Callback()
            for b in self.brokers:
                if (b.c_broker is not None) and \
                   ((cGalaxy.GalIO_BrokerReadReady(b.c_broker) or \
                     cGalaxy.GalIO_BrokerWriteReady(b.c_broker))):
                    b.Callback()
            for b in self.proxies:
                if b.Pollable():
                    b.Callback()

    def Validating(self):
        if self.c_conn is not None:
            return cGalaxy.GalIO_CommValidating(self.c_conn)
        else:
            return None

    # Make sure the result is coerced into a frame,
    # if it comes back as a dict.
    def _CallDispatchFn(self, fn, py_frame, py_env):
        try:
            res = fn(py_env, py_frame)
            if type(res) is types.DictType:
                # Ensure that it's a frame structure.
                res = Frame(contents = res)
        except:
            if sys.exc_type is SystemExit:
                # Reraise
                raise sys.exc_type, sys.exc_value, sys.exc_traceback
            if self.server.debug:
                traceback.print_exc()
            # Figure out where we are.
            tb = sys.exc_traceback
            while tb.tb_next:
                tb = tb.tb_next
            tb_fr = tb.tb_frame
            line_str = tb_fr.f_code.co_filename + ", line " + `tb_fr.f_lineno`
            py_env.Error(self.server.ServerName() + ": " + str(sys.exc_type) + ": " + str(sys.exc_value))
            res = None
        if res is None:
            return res
        else:
            return res._PythonToC()



##################################################
#
# Call environments
#
##################################################

# This used to be called a Connection, but since we've
# decided in 3.0 to do the "right thing" with call
# environments, we probably ought to reveal them to the world.

class CallEnvironment:

    def __init__(self, conn, c_env, create_p = 0):
        if create_p and (c_env is None):
            c_env = cGalaxy.GalSS_EnvCreate(conn.c_conn)
        self.conn = conn
        self.server = self.conn.server
        self.c_env = c_env
        # Make sure to lock the object, just in
        # case people save it away...
        cGalaxy.GalSS_EnvLock(c_env)
        self.ostream = self.conn.ostream

    def __del__(self):
        # And unlock the object when it's done.
        if self.c_env:
            cGalaxy.GalSS_EnvUnlock(self.c_env)

    def GetSessionID(self):
        return cGalaxy.GalSS_EnvGetSessionID(self.c_env)

    def UpdateSessionID(self, id):
        cGalaxy.GalSS_EnvUpdateSessionID(self.c_env, id)

    def ReturnRequired(self):
        return cGalaxy.GalSS_EnvReturnRequired(self.c_env)

    def GetOriginatingProvider(self):
        return cGalaxy.GalSS_EnvGetOriginatingProvider(self.c_env)

    def InheritTokenTimestamp(self):
        cGalaxy.GalSS_EnvInheritTokenTimestamp(self.c_env)

    def GetTokenTimestamp(self):
        return cGalaxy.GalSS_EnvGetTokenTimestamp(self.c_env)

    def DispatchFrame(self, out_frame, provider = None):
        if not self.conn.c_conn:
            raise ConnectionDead
        f = out_frame._PythonToC()
        if provider is not None:
            res_array = cGalaxy.GBGalSS_EnvDispatchFrameToProvider(self.c_env, f,
                                                                   provider)
        else:
            res_array = cGalaxy.GBGalSS_EnvDispatchFrame(self.c_env, f)
        return self.conn._PostprocessReturn(res_array, f)

    def DispatchFrameWithContinuation(self, out_frame, continuation_fn,
                                      provider = None):
        if not self.conn.c_conn:
            raise ConnectionDead
        f = out_frame._PythonToC()
        # We need to map back from the C continuation to
        # the Python one, and that's really for the connection
        # object to deal with.
        # First, we need to copy the current environment. Then,
        # we need to store away the new environment.
        new_env = copy.copy(self)
        new_env.continuation_fn = continuation_fn
        new_env.c_env = None
        if provider is not None:
            res = cGalaxy.GalSS_PyEnvDispatchFrameToProviderWithContinuation(self.c_env, f, provider,
                                                                   lambda env, reply_f, msg_type, py_env = new_env: py_env._Continue(reply_f, env, msg_type))
        else:
            res = cGalaxy.GalSS_PyEnvDispatchFrameWithContinuation(self.c_env, f,
                                                                   lambda env, reply_f, msg_type, py_env = new_env: py_env._Continue(reply_f, env, msg_type))
        cGalaxy.Gal_FreeFrame(f)
        if res == -1:
            raise WriteError, "Writing continuation failed"
        return None

    def _Continue(self, c_env, c_frame, msg_type):
        py_frame = Frame(_gal_frame = c_frame)
        self.c_env = c_env
        cGalaxy.GalSS_EnvLock(c_env)
        try:
            res = self.continuation_fn(self, py_frame, msg_type)
        except:
            if sys.exc_type is SystemExit:
                # Reraise
                raise sys.exc_type, sys.exc_value, sys.exc_traceback
            # Figure out where we are.
            if self.conn.debug:
                traceback.print_exc()
            tb = sys.exc_traceback
            while tb.tb_next:
                tb = tb.tb_next
            tb_fr = tb.tb_frame
            line_str = tb_fr.f_code.co_filename + ", line " + `tb_fr.f_lineno`
            self.Error(self.server.ServerName() + ": " + str(sys.exc_type) + ": " + str(sys.exc_value))
            res = None
        if res is None:
            return res
        else:
            return res._PythonToC()

    def WriteFrame(self, out_frame, provider = None):
        f = out_frame._PythonToC()
        if provider is not None:
            res = cGalaxy.GalSS_EnvWriteFrameToProvider(self.c_env, f, provider, 0)
        else:
            res = cGalaxy.GalSS_EnvWriteFrame(self.c_env, f, 0)
        cGalaxy.Gal_FreeFrame(f)
        if res == -1:
            raise WriteError, "Couldn't write frame"

    def DestroyToken(self):
        if cGalaxy.GalSS_EnvDestroyToken(self.c_env) == -1:
            raise WriteError, "Couldn't send destroy message; reply already sent"

    def Reply(self, out_frame):
        f = out_frame._PythonToC()
        res = cGalaxy.GalSS_EnvReply(self.c_env, f)
        cGalaxy.Gal_FreeFrame(f)
        if res == -1:
            raise WriteError, "Couldn't send reply"

    def Error(self, description, errno = GAL_APPLICATION_ERROR):
        if cGalaxy.GalSS_EnvErrorOfType(self.c_env, errno, description) == -1:
            raise WriteError, ("Couldn't send error message; reply already sent", description)

    def GetSessionProperties(self, keys):
        c_f = cGalaxy.GalSS_EnvGetSessionProperties(self.c_env, keys)
        if c_f:
            py_frame = Frame(_gal_frame = c_f)
            cGalaxy.Gal_FreeFrame(c_f)
            return py_frame
        else:
            return None

    def GetServerProperties(self, keys):
        c_f = cGalaxy.GalSS_EnvGetServerProperties(self.c_env, keys)
        if c_f:
            py_frame = Frame(_gal_frame = c_f)
            cGalaxy.Gal_FreeFrame(c_f)
            return py_frame
        else:
            return None

    def ModifySessionProperties(self, properties_to_set = None,
                                properties_to_delete = None):
        if (properties_to_set is None) and (properties_to_delete is None):
            return
        if (properties_to_set is not None):
            c_f = properties_to_set._PythonToC()
        else:
            c_f = "NULL"
        cGalaxy.GalSS_EnvModifySessionProperties(self.c_env,
                                                 c_f, properties_to_delete)

    def ModifyServerProperties(self, properties_to_set = None,
                                properties_to_delete = None):
        if (properties_to_set is None) and (properties_to_delete is None):
            return
        if (properties_to_set is not None):
            c_f = properties_to_set._PythonToC()
        else:
            c_f = "NULL"
        cGalaxy.GalSS_EnvModifyServerProperties(self.c_env,
                                                 c_f, properties_to_delete)

    def SetSession(self, session_name, lock_info = -1):
        cGalaxy.GalSS_EnvSetSession(self.c_env, session_name, lock_info)


# For seeds.

def CallEnvironmentSeed(conn, env_class = CallEnvironment,
                        session_id = None):
    env = env_class(conn, None, create_p = 1)
    if session_id is not None:
        env.UpdateSessionID(env, session_id)
    return env

##################################################
#
# Servers
#
##################################################

# This server object handles the toplevel work. It works
# using select. We incorporate some of the MGal tricks for
# registering callbacks, etc.

OAS = [("-port <port_num>", "server port number", [types.IntType]),
       ("-assert", "don't search for another port number if busy"),
       ("-validate", "check signatures for each dispatch function call"),
       ("-verbosity <num>", "set verbosity level", [types.IntType]),
       ("-maxconns <maxconns>", "maximum number of connections", [types.IntType]),
       ("-contact_hub host:port...", "run as client, contacting the Hubs at the specified host and port pairs (overrides -port)"),
       ("-session_id <id>", "if -contact_hub is used, lock this client to the specified Hub session"),
       ("-server_locations_file <file>", "a file of lines server host:port [hub|server]"),
       ("-slf_name <name>", "if -server_locations_file is used, optional file index"),
       ("-debug", "debug mode")]

# All the server should need is to set up the arguments and
# call the Run operation, and to maintain the mapping from
# Connection elements to the corresponding C classes.

# env_class is some subclass of CallEnvironment.

ServerError = "ServerError"

class Server:
    def __init__(self, in_args, server_name = "<unknown>", \
                 default_port = 0, \
                 verbosity = -1,
                 require_port = 0,
                 maxconns = 1,
                 validate = 0,
                 server_listen_status = GAL_CONNECTION_LISTENER,
                 client_pair_string = None,
                 session_id = None,
                 server_locations_file = None,
                 slf_name = None,
                 env_class = CallEnvironment):
        self.dispatch_fn_dict = {}
        self.read_conns = {}
        self.write_conns = {}
        self.conns = {}
        self.__server_name = server_name
        self.ostream = SLSUtil.OStream()
        self.debug = 0
        self.cur_connections = 0
        self.poll_clients = 0
        # Children need to be able to override this.
        self.env_class = env_class
        self.conn_class = Connection
        try:
            data_dict, in_args = self.CheckUsage(OAS, in_args)
            if in_args[1:]:
                apply(self.PrintUsage, SLSUtil.OAPrintUsage(OAS))
                sys.exit(1)
        except SLSUtil.OAError, (args, descs):
            self.PrintUsage(args, descs)
            sys.exit(1)
        if data_dict.has_key("-port"):
            port = data_dict["-port"][0]
            # Make sure that whatever else happens, listening is enabled.
            server_listen_status = server_listen_status | GAL_CONNECTION_LISTENER
        else:
            port = default_port
        if data_dict.has_key("-verbosity"):
            verbosity = data_dict["-verbosity"][0]
        if verbosity > -1:
            SLSUtil.VERBOSE_LEVEL = verbosity
        if data_dict.has_key("-debug"):
            self.debug = 1
        if data_dict.has_key("-assert"):
            require_port = 1
        if data_dict.has_key("-maxconns"):
            maxconns = data_dict["-maxconns"][0]
        self.__max_connections = maxconns
        if data_dict.has_key("-validate"):
            validate = 1
        # This is ignored if there's no -contact_hub argument.
        if data_dict.has_key("-session_id"):
            session_id = data_dict["-session_id"][0]
        if data_dict.has_key("-contact_hub"):
            client_pair_string = data_dict["-contact_hub"][0]
            if data_dict.has_key("-port"):
                server_listen_status = server_listen_status | GAL_HUB_CLIENT | GAL_CONNECTION_LISTENER
            else:
                # DISABLE LISTENING.
                server_listen_status = (server_listen_status & ~GAL_CONNECTION_LISTENER) | GAL_HUB_CLIENT
        if data_dict.has_key("-server_locations_file"):
            server_locations_file = data_dict["-server_locations_file"][0]
        if data_dict.has_key("-slf_name"):
            slf_name = data_dict["-slf_name"][0]
        self.c_server_socknum = None
        arg_pkg = cGalaxy._GBGalSS_EncapsulateArguments(server_name, port, maxconns, require_port, validate, verbosity, server_listen_status, client_pair_string, session_id, server_locations_file, slf_name)
        self._gal_server = cGalaxy.GBGalSS_SetupServer(arg_pkg)
        cGalaxy.GalSS_FreeArgPkg(arg_pkg)
        if self._gal_server is None:
            raise ServerError, "Couldn't set up server"
        # I'm setting this up here rather than by monitoring the
        # result of the server callback handler because the connection
        # can be made by virtue of polling the server locations
        # for the listener-in-Hub case.
        cGalaxy.GalIO_PyAddServerCallback(self._gal_server,
                                          cGalaxy.GAL_SERVER_LISTENER_STARTUP_EVENT,
                                          lambda s = self: s._RegisterListener())
        cGalaxy.GalIO_PyAddServerCallback(self._gal_server,
                                          cGalaxy.GAL_SERVER_CLIENT_POLL_STARTUP_EVENT,
                                          lambda s = self: s._RegisterClient())
        # Oops. Because this is assumed to be called inside
        # GalSS_SetupServer, BEFORE the command line stuff
        # is processed, this had better pass in port instead
        # of default_port.
        # Oops again. The problem is actually worse than that.
        # Either the -port OR -server_locations_file arguments
        # could have set this already. So the only thing to do
        # is go and get the value and pass it back in. Sigh.
        p = cGalaxy.GalIO_GetServerDefaultPort(self._gal_server)
        cGalaxy.GalSS_InitializeServerDefaults(self._gal_server,
                                               server_name, p)
        # The problem with signal handling in Python is
        # that any functions are postponed until the next
        # Python instruction step, which is no good when I'm
        # in the C loop. Furthermore, it's not possible to
        # return SIGINT to default behavior, because its
        # default behavior is to raise a keyboard interrupt,
        # which is installed even when I pass signal.SIG_DFL.
        # Grrr.
        if not self.debug:
            signal.signal(signal.SIGINT, self.Quit)

        # Update the registration of dispatch functions.
        cGalaxy._GalIO_PySetServerDispatchFnAccess(self._gal_server,
                                                   self._ListDispatchFnSigs,
                                                   self._SelectDispatchFn)

    def _ListDispatchFnSigs(self):
        return map(lambda x: x[1], self.dispatch_fn_dict.values())

    def _SelectDispatchFn(self, op_name):
        if self.dispatch_fn_dict.has_key(op_name):
            return self.dispatch_fn_dict[op_name]
        else:
            return None, None

    def AddServiceType(self, t):
        cGalaxy.GalIO_AddServiceType(self._gal_server, t)

    def ModifyProperties(self, properties_to_set = None, properties_to_delete = None):
        if (properties_to_set is None) and (properties_to_delete is None):
            return
        if properties_to_set is not None:
            c_f = properties_to_set._PythonToC()
        else:
            c_f = "NULL"
        cGalaxy.GalIO_ServerModifyProperties(self._gal_server,
                                             c_f, properties_to_delete)

    def ListenPort(self):
        if self._gal_server is not None:
            return cGalaxy.GalIO_GetServerListenPort(self._gal_server)
        else:
            return None

    def EnableValidation(self):
        if self._gal_server is not None:
            cGalaxy.GalIO_EnableDispatchFnValidation(self._gal_server)

    def ServerName(self, name = None):
        if name is None:
            return self.__server_name
        else:
            if self._gal_server:
                cGalaxy.GalIO_SetServerName(self._gal_server, name)
            self.__server_name = name
            return name

    def MaxConnections(self, num = None):
        if num is None:
            return self.__max_connections
        else:
            if self._gal_server:
                cGalaxy.GalIO_SetServerMaxConnections(self._gal_server, num)
            self.__max_connections = num
            return num

    def CheckUsage(self, oas_list, args):
        return SLSUtil.OAExtract(oas_list, args, self.ostream)

    def PrintUsage(self, args, descs):
        print "Usage: %s %s" % (self.__server_name, args)
        print
        print descs

    # Signatures have exactly the same form they do in the C bindings.
    # They're a five-tuple, where the zeroth and third elements are
    # a list of triples, whose zeroth element is a key name, first is
    # a type, and second is GAL_KEY_ALWAYS, etc.; and the first,
    # second and fourth are information about other keys permitted or
    # a reply provided. If there are no in or out keys, the entries
    # must be empty lists, not None.

    def AddDispatchFunction(self, name, fn, signature = None):
        if signature is None:
            signature = [[], GAL_OTHER_KEYS_MAYBE,
                         GAL_REPLY_UNKNOWN, [],
                         GAL_OTHER_KEYS_MAYBE]
        [in_keys, in_other_keys, reply_status, out_keys, out_other_keys] = signature
        # The easiest way to do this is to capture all the
        # dispatch functions and then translate the list into
        # a Gal_Object and decode it. But that won't quite
        # work, because if somebody uses their own
        # main loop, the wrong thing will happen. So I will
        # use C functions to build the key mappings,
        # and then pass them in.
        in_key_struct = cGalaxy._Gal_CreateEmptyDispatchFnKeyArray(len(in_keys))
        for i in range(len(in_keys)):
            [key, type, oblig] = in_keys[i]
            cGalaxy._Gal_PopulateDispatchFnKeyArrayCell(in_key_struct, i, key, type, oblig)
        out_key_struct = cGalaxy._Gal_CreateEmptyDispatchFnKeyArray(len(out_keys))
        for i in range(len(out_keys)):
            [key, type, oblig] = out_keys[i]
            cGalaxy._Gal_PopulateDispatchFnKeyArrayCell(out_key_struct, i, key, type, oblig)
        self.dispatch_fn_dict[name] = (lambda frame, env, fn = fn, s = self: s._CallDispatchFn(fn, frame, env), cGalaxy.Gal_CreateDispatchFnSignature(name, in_key_struct, in_other_keys, reply_status, out_key_struct, out_other_keys))

    # These are called with C pointers for frame and env,
    # and must be converted (on return, too). We need to
    # accumulate the connections and keep them
    # constant, because they're supposed to be
    # persistent data.

    def _CallDispatchFn(self, fn, frame, c_env):
        # Push this down to the connection.
        c_conn = cGalaxy.GalSS_EnvComm(c_env)
        py_conn = self.conns[c_conn]
        py_frame = Frame(_gal_frame = frame)
        py_env = self.env_class(py_conn, c_env)
        return py_conn._CallDispatchFn(fn, py_frame, py_env)

    def Quit(self, *args):
        sys.exit(1)

    def ServerIsClient(self):
        if self._gal_server is None:
            return None
        return cGalaxy.GalIO_ServerIsClient(self._gal_server)

    def ServerIsListener(self):
        if self._gal_server is None:
            return None
        return cGalaxy.GalIO_ServerIsListener(self._gal_server)

    def _RegisterListener(self):
        # Don't check if it's a listener, because
        # it won't be until it starts up.
        self.c_server_socknum = cGalaxy.GalIO_GetServerListenSocket(self._gal_server)
        self.ReaderRegister(self, self.c_server_socknum)
        cGalaxy.GalIO_PyAddServerCallback(self._gal_server,
                                          cGalaxy.GAL_SERVER_LISTENER_SHUTDOWN_EVENT,
                                          lambda s = self: s._UnregisterListener())

    def _RegisterClient(self):
        # Don't check if it's a client, because
        # it won't be until it starts up.
        self.poll_clients = 1

    def PollClients(self):
        cGalaxy.GalIO_ServerCheckHubContacts(self._gal_server)

    def RunServer(self):
        if not cGalaxy.GalIO_ServerStart(self._gal_server):
            return
        cGalaxy.GalIO_PyAddServerCallback(self._gal_server,
                                          cGalaxy.GAL_SERVER_DESTRUCTION_EVENT,
                                          lambda s = self: s._ExitLoop())
        cGalaxy.GalIO_PyAddServerConnectCallback(self._gal_server, lambda c_conn, s = self: s.CreateConnection(c_conn))
        self._ServerLoop()

    def _ServerLoop(self):
        self.loop_exit = 0
        i = 0
        while not self.loop_exit:
            self.PollConnections()
            # We want to check the listener-in-Hub stuff.
            # I don't want to check this every time, so let's
            # check it every ten times.
            if (i == 10):
                if self.ServerIsClient(): self.PollClients()
                i = 0
            else:
                i = i + 1

    # Checking sockets is probably not good enough. We
    # need also to check to see if there's anything in the
    # sockqueue. Sigh. Similarly for checking the client
    # connections.

    def PollConnections(self):
        # I'm not going to ever block anymore, because
        # I need to poll other things after the select()
        # returns. I'm going to block for no more than .1 seconds.
        # On Windows, you can't use select() to sleep. So we'll
        # only call select() if there's something in read_conns
        # or write_conns.
        if self.read_conns.keys() or self.write_conns.keys():
            eligible = select.select(self.read_conns.keys(),
                                     self.write_conns.keys(), [], 0.1)
        else:
            eligible = [], []
            time.sleep(0.1)
        for conn in eligible[0]:
            self.read_conns[conn].Callback()
        for conn in eligible[1]:
            self.write_conns[conn].Callback()
        # Now, we check all the connections, just
        # in case there's stuff in their queues.
        for py_conn in self.conns.values():
            py_conn.PollConnection()

    # Return values of GalIO_ServerCallbackHandler():
    # 1 if there's a new connection
    # 0 if not
    # -1 if error and the listener has been shut down
    # -2 if error and server has been destroyed.

    # All these cases are now handled by callbacks.

    def Callback(self):
        res = cGalaxy.GBGalIO_ServerCallbackHandler(self._gal_server, 0)
        cGalaxy.GBGal_FreeResultArray(res)

    def _UnregisterListener(self):
        self.ReaderUnregister(self.c_server_socknum)
        self.c_server_socknum = None

    def _ExitLoop(self):
        self._UnregisterListener()
        self._gal_server = None
        self.loop_exit = 1

    def Disconnect(self):
        # This is how we shut down a server.
        if self._gal_server is not None:
            if self.c_server_socknum:
                self.ReaderUnregister(self.c_server_socknum)
                self.c_server_socknum = None
            cGalaxy.GalIO_DestroyServerStruct(self._gal_server)
            self._gal_server = None

    def CreateConnection(self, c_conn):
        # Build the connection object. This will
        # do the registration.
        self.conn_class(self, c_conn)

    def ReaderRegister(self, obj, fd):
        self.read_conns[fd] = obj

    def ReaderUnregister(self, fd):
        try:
            del self.read_conns[fd]
        except: pass

    def WriterRegister(self, obj, fd):
        self.write_conns[fd] = obj

    def WriterUnregister(self, fd):
        try:
            del self.write_conns[fd]
        except: pass

#######################################################
#
# Mimicking a Hub connection (see GalIO_ClientConnect)
#
#######################################################

ClientConnectionError = "ClientConnectionError"

class ClientConnection(BasicConnection):
    def __init__(self, host, port, welcome_frame = None, \
                 connect = 1, retry = 1, debug = 0):
        BasicConnection.__init__(self, SLSUtil.OStream(), debug = debug)
        self.disconnected = 1
        self.host = host
        self.port = port
        if welcome_frame:
            self.f_wframe = welcome_frame._PythonToC()
        else:
            self.f_wframe = None
        if connect:
            self.Connect(retry)

    def Connect(self, retry = 0):
        if retry:
            while 1:
                try:
                    self.__ConnectOnce()
                    break
                except ClientConnectionError, val:
                    print val
                    time.sleep(1)
        else:
            self.__ConnectOnce()

    def __ConnectOnce(self):
        if self.disconnected == 0:
            print "Already connected."
            return
        res_array = cGalaxy.GBGalIO_ClientConnect("<unknown>",
                                                    self.host,
                                                    self.port,
                                                    0, self.f_wframe)
        c_conn = cGalaxy.GBGal_ResultArrayCommStruct(res_array)
        reply_c_frame = cGalaxy.GBGal_ResultArrayFrame(res_array)
        cGalaxy.GBGal_FreeResultArray(res_array)
        if not c_conn:
            raise ClientConnectionError, "Can't connect to server"
        else:
            self.AddCConnection(c_conn)

    def ReadFrame(self, blocking = 1):
        res_array = cGalaxy.GBGalIO_CommReadMessage(self.c_conn, blocking)
        status = cGalaxy.GBGal_ResultArrayStatus(res_array)
        c_f = cGalaxy.GBGal_ResultArrayFrame(res_array)
        msg_type = cGalaxy.GBGal_ResultArrayMsgType(res_array)
        cGalaxy.GBGal_FreeResultArray(res_array)
        if c_f:
            f = Frame(_gal_frame = c_f), msg_type
            cGalaxy.Gal_FreeFrame(c_f)
            return f
        else:
            return None, None
