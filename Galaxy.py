# This file (c) Copyright 1998 - 2002 The MITRE Corporation
#
# This file is part of the Galaxy Communicator system. It is licensed
# under the conditions described in the file LICENSE in the root
# directory of the Galaxy Communicator system.

# In this file, you'll find the objects corresponding to
# libGalaxy/galaxy.

# dispatch_function.c:
# grovel.c: not implemented (unneeded utilities)
# io_util.c: private functions for server support - see GalaxyIO.py
# nfio.c: implemented as Frame method
# nframe.c: implemented
# plist.c: not needed
# pr_util.c: partially implemented as Frame methods
# sym.c: implemented
# timed_tasks.c: not implemented (different polling strategy used)
# tobj.c: mostly not implemented (Python types used)
# uucode.c: implemented
# vlist.c: not needed

GAL_DOC = \
"""
Gal_ReadFrameFromString(s):            Frame(str = s)
Gal_ReadFrameFromFile(fp):             [not implemented]
Gal_ReadObjectFromString(s):           _read_irp_value(s)
Gal_ReadObjectFromFile(fp):            [not implemented]
Gal_MakeFrame(name, type):             Frame(name = name, type = type)
Gal_MakeTopicFrame(name):              Frame(name = name, type = GAL_TOPIC)
Gal_MakePredFrame(name):               Frame(name = name, type = GAL_PRED)
Gal_MakeClauseFrame(name):             Frame(name = name, type = GAL_CLAUSE)
Gal_FreeFrame(f):                      [not needed]
Gal_CopyFrame(f):                      f.Copy()
Gal_FrameEqual(f1, f2):                f1.Equal(f2)
Gal_MatchFrame(f1, f2):                f1.Match(f2) [not yet implemented]
Gal_SetFrameName(f, name):             f.name = name
Gal_SetFrameType(f, type):             f.type = type
Gal_FrameName(f):                      f.name
Gal_FrameNameEq(f, name):              f.name == name
Gal_FrameNamesEq(f1, f2):              f1.name == f2.name
Gal_FrameIsType(f, type):              f.type == type
Gal_AddPred(f, pred):                  f.preds.append(pred)
Gal_GetPred(f, i):                     f.preds[i]
Gal_GetPredByName(f, name):            f.GetPredByName(name)
Gal_RemPred(f, i):                     p = f.preds[i]; del f.preds[i]; return p
Gal_RemPredByName(f, name):            p = f.GetPredByName(name); f.preds.remove(p); return p
Gal_DelPred(f, i):                     del f.preds[i]
Gal_DelPredByName(f, name):            p = f.GetPredByName(name); f.preds.remove(p)
Gal_NumPreds(f):                       len(f.preds)
Gal_ClearPreds(f):                     f.preds = []
Gal_SetProp(f, key, obj):              f[key] = obj
Gal_GetObject(f, key):                 f[key]
Gal_GetFrame(f, key):                  f.GetValue(key, GAL_FRAME)
Gal_GetTopicFrame(f, key):             [not implemented]
Gal_TopicValue(...):                   [not implemented]
Gal_GetString(f, key):                 f.GetValue(key, GAL_STRING)
Gal_GetInt(f, key):                    f.GetValue(key, GAL_INT)
Gal_GetFloat(f, key):                  f.GetValue(key, GAL_FLOAT)
Gal_GetList(f, key):                   f.GetValue(key, GAL_LIST)
Gal_GetBinary(f, key):                 f.GetValue(key, GAL_BINARY)
Gal_RemProp(f, key):                   p = f[key]; del f[key]; return p
Gal_DelProp(f, key):                   del f[key]
Gal_NumProperties(f):                  len(f)
Gal_GetProperties(f):                  f.keys()

Gal_PrFrame(f):                        print f.Print() OR f.Pr()
Gal_PPFrame(f):                        print f.PPrint() OR f.PP()
GalUtil_PPFrame(verbose_level, fr):    SLSUtil.OStream().write_level(fr.PPrint(), verbose_level)
GalUtil_CPPFrame(verbose_level, fr):   [not implemented]
Gal_PrFrameToString(f, buf, size):     f.Print()
Gal_PPFrameToString(f, buf, size):     f.PPrint()
Gal_PrFrameToFile(f, fp):              fp.write(f.Print())
Gal_PPFrameToFile(f, fp):              fp.write(f.PPrint())
Gal_PPObjectToFile(o, fp):             fp.write(OPr(o, PP_TYPE))
Gal_PPObject(o):                       print OPr(o, PP_TYPE)
Gal_OutlineFrame(f, verbose_level):    print f.OPrint() OR f.Outline() [not implemented yet]
Gal_OutlineObject(f, verbose_level):   [not implemented]
Gal_PrObject(obj):                     print OPr(obj) OR PrObject(obj)
Gal_ObjectToString(obj):               OPr(obj)
GalUtil_PrObject(v_level, o):          SLSUtil.OStream().write_level(OPr(o), v_level)
GalUtil_PPObject(v_level, o):          SLSUtil.OStream().write_level(OPr(o, PP_TYPE), v_level)
GalUtil_CPPObject(v_level, o):         [not implemented]
Gal_PrObjectToFile(obj, fp):           fp.write(OPr(obj))

Gal_GetObjectType(obj):                GetObjectType(obj)
Gal_GetDetailedType(obj):              GetDetailedType(obj)
Gal_ObjectTypeString(type):            ObjectTypeString(type)
Gal_GetObjectTypeString(obj):          ObjectTypeString(GetObjectType(obj))

# not implemented: grovel.c

Gal_FindKey(f, name):                  [not implemented]
Gal_MatchKeyValue(f, name, obj):       [not implemented]
Gal_FindPred(f, pred_name):            [not implemented]
Gal_FindTopic(f, name):                [not implemented]
Gal_DeletePreds(f, name):              [not implemented]
Gal_FindPredParent(f, name, parent, findpar, nth): [not implemented]

# end

# not implemented: signal.c

Gal_AddSignalHandler(...):             [not implemented]
Gal_SignalsInitialized():              [not implemented]
Gal_InitializeSignals():               [not implemented]

# not implemented: timed_tasks.c

Gal_AddTimedTask(task, val, ms):       [not implemented]
Gal_RemoveTimedTask(task, val):        [not implemented]
Gal_TimedTasksLoopHandler(tv):         [not implemented]
Gal_TimedTasksLoop():                  [not implemented]
Gal_TimedTasksLoopExit():              [not implemented]
Gal_TaskPkgBlocking(pkg):              [not implemented]
Gal_TaskPkgData(pkg):                  [not implemented]
Gal_EnableTimedTaskThreads():          [not implemented]
Gal_RemoveTask(...):                   [not implemented]
Gal_AddTask(...):                      [not implemented]
Gal_AddTimedTaskWithIO(...):           [not implemented]
Gal_ReAddTask(...):                    [not implemented]
Gal_TimedTaskThreadsEnabled():         [not implemented]

#end

# end

Gal_Predp(obj):                        GetDetailedType(obj) == GAL_PRED
Gal_FreeObject(obj):                   [not needed]
Gal_FrameObject(f):                    [not needed]
Gal_StringObject(obj):                 [not needed]
Gal_ListObject(obj):                   [not needed]
Gal_ListObjectFromElements(...):       [not needed]
Gal_IntObject(obj):                    [not needed]
Gal_BinaryObject(data, size):          BinaryObject(GAL_BINARY, data)
Gal_PointerObject(obj):                [not implemented]
Gal_FloatObject(float):                [not needed]
Gal_ObjectEqual(obj1, obj2):           ObjectEqual(obj1, obj2)
Gal_ObjectCaseEqual(obj1, obj2):       ObjectEqual(obj1, obj2, ignore_case = 1)
Gal_Floatp(obj):                       GetObjectType(obj) == GAL_FLOAT OR type(obj) is types.FloatType
Gal_Topicp(obj):                       GetDetailedType(obj) == GAL_TOPIC
Gal_TopicFramep(obj):                  GetDetailedType(obj) == GAL_TOPIC
Gal_PredFramep(obj):                   GetDetailedType(obj) == GAL_PRED
Gal_Clausep(obj):                      GetDetailedType(obj) == GAL_CLAUSE
Gal_ClauseFramep(obj):                 GetDetailedType(obj) == GAL_CLAUSE
Gal_Listp(obj):                        GetObjectType(obj) == GAL_LIST OR type(obj) is types.ListType
Gal_Binaryp(obj):                      GetObjectType(obj) == GAL_BINARY
Gal_Framep(obj):                       GetObjectType(obj) == GAL_FRAME
Gal_Stringp(obj):                      GetObjectType(obj) == GAL_STRING OR type(obj) is types.StringType
Gal_Intp(obj):                         GetObjectType(obj) == GAL_INT OR type(obj) is types.IntType
Gal_ListLength(obj):                   len(obj)
Gal_GetListValue(obj, n, t):           ValueWarn(obj[n], t)
Gal_StringValue(obj):                  ValueWarn(obj, GAL_STRING)
Gal_BinaryValue(obj):                  ValueWarn(obj, GAL_BINARY)
Gal_ListValue(obj):                    ValueWarn(obj, GAL_LIST)
Gal_FrameValue(obj):                   ValueWarn(obj, GAL_FRAME)
Gal_PredValue(obj):                    [not implemented]
Gal_ClauseValue(obj):                  [not implemented]
Gal_IntValue(obj):                     ValueWarn(obj, GAL_INT)
Gal_FloatValue(obj):                   ValueWarn(obj, GAL_FLOAT)
Gal_BinarySize(obj):                   len(obj)
Gal_GetFrameType(obj):                 f.type
Gal_CopyObject(obj):                   [not implemented]
Gal_GetListObject(obj, n):             obj[n]
Gal_Symbolp(obj):                      GetObjectType(obj) == GAL_SYMBOL
Gal_FreeWrapper(obj):                  [not needed]

# dispatch_function.c

Gal_FreeDispatchFnKeyArray(entry):     [not needed]
Gal_CreateDispatchFnKeyArray(...):     [not needed]


"""

import string, UserDict, types, copy, sys, array

##################################################
#
# Errors
#
##################################################

FramePrintingError = "FramePrintingError"
FrameParsingError = "FrameParsingError"

##################################################
#
# Types
#
##################################################

import cGalaxy

cGalaxy.Gal_InitializeStatics()

from cGalaxy import GC_VERSION, GAL_KEY_ALWAYS, GAL_KEY_SOMETIMES, \
     GAL_OTHER_KEYS_MAYBE, GAL_OTHER_KEYS_NEVER, GAL_REPLY_PROVIDED, \
     GAL_REPLY_NONE, GAL_REPLY_UNKNOWN, GAL_TOPIC, GAL_CLAUSE, GAL_PRED, \
     GAL_FREE, GAL_FRAME, GAL_STRING, GAL_INT, GAL_FLOAT, GAL_SYMBOL, \
     GAL_LIST, GAL_TOPIC_FRAME, GAL_CLAUSE_FRAME, GAL_PRED_FRAME, \
     GAL_BINARY, GAL_INT_16, GAL_INT_32, GAL_INT_64, GAL_FLOAT_32, \
     GAL_FLOAT_64, GAL_PROXY

GAL_ERROR_NUMBER_FRAME_KEY = cGalaxy.cvar.GAL_ERROR_NUMBER_FRAME_KEY
GAL_ERROR_DESCRIPTION_FRAME_KEY = cGalaxy.cvar.GAL_ERROR_DESCRIPTION_FRAME_KEY
GAL_SESSION_ID_FRAME_KEY = cGalaxy.cvar.GAL_SESSION_ID_FRAME_KEY
GAL_SERVER_TOKEN_INDEX_FRAME_KEY = cGalaxy.cvar.GAL_SERVER_TOKEN_INDEX_FRAME_KEY
GAL_HUB_OPAQUE_DATA_FRAME_KEY = cGalaxy.cvar.GAL_HUB_OPAQUE_DATA_FRAME_KEY
GAL_ROUND_TRIP_FRAME_KEY = cGalaxy.cvar.GAL_ROUND_TRIP_FRAME_KEY

_FrameTypeDict = {GAL_TOPIC: GAL_TOPIC_FRAME,
                  GAL_CLAUSE: GAL_CLAUSE_FRAME,
                  GAL_PRED: GAL_PRED_FRAME}

_IntSizeArray = {}
_FloatSizeArray = {}
_EncodingArray = {}

_ArrayType = type(array.array("B"))

for x in ["B", "H", "I", "L"]:
    i = array.array(x).itemsize
    if not _IntSizeArray.has_key(i):
        _IntSizeArray[i] = x
    if i == 1:
        _EncodingArray[x] = GAL_BINARY
    elif i == 2:
        _EncodingArray[x] = GAL_INT_16
    elif i == 4:
        _EncodingArray[x] = GAL_INT_32
    elif i == 8:
        _EncodingArray[x] = GAL_INT_64

if not _IntSizeArray.has_key(1):
    # If we can't read/write unsigned bytes, we're doomed
    sys.stderr.write("Don't have a translation for unsigned bytes; exiting...\n")
    sys.exit(1)

for x in ["f", "d"]:
    i = array.array(x).itemsize
    if not _FloatSizeArray.has_key(i):
        _FloatSizeArray[i] = x
    if i == 4:
        _EncodingArray[x] = GAL_FLOAT_32
    elif i == 8:
        _EncodingArray[x] = GAL_FLOAT_64

# These need to remain in Python, because the Gal_Object
# structure is only present in the frame slots. Sigh.

def GetObjectType(val):
    if type(val) is types.IntType:
        return GAL_INT
    elif type(val) is types.FloatType:
        return GAL_FLOAT
    elif type(val) is types.ListType:
        return GAL_LIST
    elif type(val) is types.StringType:
        return GAL_STRING
    elif type(val) is types.InstanceType:
        return val._gal_type
    elif type(val) is _ArrayType:
        return _EncodingArray[val.typecode]

def ObjectEqual(obj1, obj2, ignore_case = 0):
    t1 = GetObjectType(obj1)
    t2 = GetObjectType(obj2)
    if t1 != t2:
        return 0
    if t1 in [GAL_FRAME, GAL_SYMBOL]:
        return obj1.Equal(obj2)
    elif (t1 is GAL_STRING) and ignore_case:
        return string.lower(obj1) == string.lower(obj2)
    else: return obj1 == obj2

def GetDetailedType(obj):
    t = GetObjectType(obj)
    if t == GAL_FRAME:
        return _FrameTypeDict[t.type]
    else: return t

# These can refer directly into C.

def ObjectTypeString(t):
    if type(t) is not types.IntType:
        raise TypeError, "not object type"
    return cGalaxy.Gal_ObjectTypeString(t)

##################################################
#
# Binary data
#
##################################################

_TypeLengthTable = {GAL_BINARY: 1,
                    GAL_INT_16: 2,
                    GAL_INT_32: 4,
                    GAL_INT_64: 8,
                    GAL_FLOAT_32: 4,
                    GAL_FLOAT_64: 8}

# I'm thinking I should keep this on the Python side,
# because I want to be able to have common types for the
# frame and for the brokering.

def BinaryObject(t, elements = []):
    if t not in [GAL_BINARY, GAL_INT_16, GAL_INT_32, GAL_INT_64, \
                 GAL_FLOAT_32, GAL_FLOAT_64]:
        raise ObjectTypeError, "not binary type"
    binary_size = _TypeLengthTable[t]
    if t in [GAL_BINARY, GAL_INT_16, GAL_INT_32, GAL_INT_64]:
        if not _IntSizeArray.has_key(binary_size):
            raise ObjectTypeError, ("can't construct %d byte arrays" % binary_size)
        return array.array(_IntSizeArray[binary_size], elements)
    else:
        if not _FloatSizeArray.has_key(binary_size):
            raise ObjectTypeError, ("can't construct %d byte arrays" % binary_size)
        return array.array(_FloatSizeArray[binary_size], elements)

##################################################
#
# Object printing
#
##################################################

# I have been defeated by the memory model of Galaxy frames.
# In particular, if I retrieve a key value which is itself
# a frame, I have no control over when that element is
# destroyed. If it's overwritten, it's destroyed, so I should
# copy it; but I can't copy it, because updates to that
# element should be reflected in the frame I got it out of.
# For the time being, I will simply translate frames
# into native elements and then back out again. I don't seem
# to have any choice in this matter, unless I want to
# rewrite the frame library.

# Printing types

IRP_TYPE = cGalaxy.GAL_PR_PRINT
PP_TYPE  = cGalaxy.GAL_PP_PRINT

# This will be an expensive operation, because in order to do it,
# I need to create a Gal_Object of the appropriate type. Except for
# frames (which is good, because that's the one case where the
# memory model is poor - frames are not copied when objects wrapping
# them are created, but ARE freed when the object wrapping it is freed).

NoObjectTranslation = "NoObjectTranslation"

def _ValToObject(val):
    gal_type = GetObjectType(val)
    if gal_type is GAL_INT:
        return cGalaxy.Gal_IntObject(val)
    elif gal_type is GAL_FLOAT:
        return cGalaxy.Gal_FloatObject(val)
    elif gal_type is GAL_LIST:
        p = cGalaxy.GBGal_EmptyListObject()
        # We have to be careful to fill every position!
        for v in val:
            cGalaxy.Gal_ListObjectAdd(p, _ValToObject(v))
        return p
    elif gal_type is GAL_BINARY:
        # I need to do something similar for binary data.
        # But I can set it up so that I can use arrays of bytes.
        s = val.tostring()
        return cGalaxy.Gal_CreateBinaryObject(s, len(s), 1)
    elif gal_type is GAL_INT_16:
        return cGalaxy.Gal_CreateInt16Object(val.tostring(), len(val), 1)
    elif gal_type is GAL_INT_32:
        return cGalaxy.Gal_CreateInt32Object(val.tostring(), len(val), 1)
    elif gal_type is GAL_INT_64:
        return cGalaxy.Gal_CreateInt64Object(val.tostring(), len(val), 1)
    elif gal_type is GAL_FLOAT_32:
        return cGalaxy.Gal_CreateFloat32Object(val.tostring(), len(val), 1)
    elif gal_type is GAL_FLOAT_64:
        return cGalaxy.Gal_CreateFloat64Object(val.tostring(), len(val), 1)
    elif gal_type is GAL_STRING:
        return cGalaxy.Gal_StringObject(val)
    elif gal_type is GAL_FRAME:
        # This will require something more complex.
        return cGalaxy.Gal_FrameObject(val._PythonToC())
    elif gal_type is GAL_SYMBOL:
        return cGalaxy.Gal_SymbolObject(val.str)
    elif gal_type is GAL_PROXY:
        return cGalaxy.Gal_CreateProxyObject(val.c_proxy, 0)
    else:
        raise NoObjectTranslation, val

def _ObjectToVal(o):
    # Now, I need to unwind the object.
    t = cGalaxy.Gal_GetObjectType(o)
    if t is GAL_FRAME:
        return Frame(_gal_frame = cGalaxy.Gal_FrameValue(o))
    elif t is GAL_INT:
        return cGalaxy.Gal_IntValue(o)
    elif t is GAL_FLOAT:
        return cGalaxy.Gal_FloatValue(o)
    elif t is GAL_STRING:
        return cGalaxy.Gal_StringValue(o)
    elif t is GAL_LIST:
        list_len = cGalaxy.Gal_ListLength(o)
        l = []
        for i in range(list_len):
            p = cGalaxy.Gal_GetListObject(o, i)
            l.append(_ObjectToVal(p))
        return l
    elif t in [GAL_BINARY, GAL_INT_16, GAL_INT_32, GAL_INT_64,
               GAL_FLOAT_32, GAL_FLOAT_64]:
        p = BinaryObject(t)
        d = cGalaxy.GBGal_ArrayValue(o)
        p.fromstring(d)
        return p
    elif t is GAL_SYMBOL:
        return _Sym(str = cGalaxy.Gal_KeywordValue(o))
    elif t is GAL_PROXY:
        import GalaxyIO
        return GalaxyIO.BrokerProxyIn(_gal_proxy = cGalaxy.Gal_ProxyValue(o))
    else:
        raise NoObjectTranslation, o

def OPr(val, how_to = IRP_TYPE):
    gal_type = GetObjectType(val)
    if gal_type in [GAL_FRAME, GAL_SYMBOL]:
        return val._Print(how_to)
    else:
        temp = _ValToObject(val)
        s = cGalaxy.Gal_ObjectToString(temp)
        cGalaxy.Gal_FreeWrapper(temp)
        return s

def PrObject(val):
    print OPr(val)

##################################################
#
# Frames
#
##################################################

# As I mentioned above, I can't map directly to C because
# the underlying memory management model is broken. So I
# will translate into native Python.

class Frame(UserDict.UserDict):

    _gal_type = GAL_FRAME

    def __init__(self, name = None, \
                 type = None, contents = None, \
                 preds = None, str = None,
                 _gal_frame = None):
        UserDict.UserDict.__init__(self)
        if _gal_frame and (str or name or type or contents or preds):
            raise FrameCreationError, "_gal_frame must be specified alone"
        elif str and (_gal_frame or name or type or contents or preds):
            raise FrameCreationError, "str must be specified alone"
        if str:
            _gal_frame = cGalaxy.Gal_ReadFrameFromString(str)
            if _gal_frame is None:
                # Couldn't turn the string into a frame.
                raise FrameParsingError, str
        if _gal_frame:
            self._CToPython(_gal_frame)
        else:
            if type:
                self.type = type
            else: self.type = GAL_CLAUSE
            if name is not None:
                self.name = name
            else: self.name = ""
            if contents:
                for key, value in contents.items():
                    self[key] = value
            if preds:
                self.preds = preds
            else:
                self.preds = []

    # Conversion to C frames.

    def _PythonToC(self):
        _gal_frame = cGalaxy.Gal_MakeFrame(self.name, self.type)
        for key, val in self.items():
            o = _ValToObject(val)
            cGalaxy.Gal_SetProp(_gal_frame, key, o)
        for p in self.preds:
            cGalaxy.Gal_AddPred(_gal_frame, p._PythonToC())
        return _gal_frame

    def _CToPython(self, _gal_frame):
        # Translate the fucking thing into Python. Grrrr.
        self.type = cGalaxy.Gal_GetFrameType(_gal_frame)
        self.name = cGalaxy.Gal_FrameName(_gal_frame)
        for key in cGalaxy.GBGal_GetProperties(_gal_frame):
            o = cGalaxy.Gal_GetObject(_gal_frame, key)
            self[key] = _ObjectToVal(o)
        self.preds = []
        for i in range(cGalaxy.Gal_NumPreds(_gal_frame)):
            p = cGalaxy.Gal_GetPred(_gal_frame, i)
            self.preds.append(Frame(_gal_frame = p))

    def __repr__(self):
        if self.type == GAL_TOPIC:
            t = "q"
        elif self.type == GAL_PRED:
            t = "p"
        elif self.type == GAL_CLAUSE:
            t = "c"
        return "<frame %s %s %s %s>" % (t, self.name, \
                                        UserDict.UserDict.__repr__(self), \
                                        str(self.preds))

    def Str(self):
        return self.__str__()

    # Printing

    def Print(self):
        return self._Print(IRP_TYPE)

    def Pr(self):
        print self.Print()

    def PPrint(self):
        return self._Print(PP_TYPE)

    def PP(self):
        print self.PPrint()

    def _Print(self, how_to):
        f = self._PythonToC()
        s = cGalaxy.Gal_FrameToString(f, how_to)
        cGalaxy.Gal_FreeFrame(f)
        return s

    # Copying
    def __getinitargs__(self):
        # For deepcopy
        return (self.type,)
    def Copy(self):
        return copy.deepcopy(self)

    # Type checking
    def GetValue(self, key, t):
        return ValueWarn(self[key], t)

    # Simple implementations
    def GetPredByName(self, name):
        for p in self.preds:
            if p.name == name:
                return p
        return None
    def Equal(self, f):
        return (self.name == f.name) and \
               self.__preds_equal(f.preds) and \
               self.__data_equal(f)
    def __preds_equal(self, pred_list):
        if len(pred_list) != len(self.preds):
            return 0
        matched = []
        for pred in self.preds:
            # Find a match for each, but each
            # match only counts once.
            for pred2 in pred_list:
                if pred2 not in matched:
                    if pred.Match(pred2):
                        matched.append(pred2)
                        break
            else:
                # Didn't break out of the loop, so didn't match
                return 0
        return 1
    def __data_equal(self, d):
        if len(self.data) != len(d):
            return 0
        for key, value in d.items():
            t = GetObjectType(value)
            try:
                val = self.GetValue(key, t)
            except:
                return 0
            if t in [GAL_FRAME, GAL_SYMBOL]:
                if not val.Equal(value):
                    return 0
            else:
                if val != value:
                    return 0
        return 1

# Frame string parsing utilities. We can parse an
# object and then take it apart and return the native types.
# For backward compatibility, return a pair.

def _read_irp_value(msg):
    if msg[:6] == "NULLObject":
        return None, ""
    temp = cGalaxy.Gal_ReadObjectFromString(msg)
    # Now, I need to unwind the object.
    t = _ObjectToVal(temp)
    cGalaxy.Gal_FreeObject(temp)
    return t, ""

##################################################
#
# Symbols
#
##################################################

# Sam 7/29/98: This isn't working exactly right, because
# strings and symbols are getting confused. So I'm going to
# introduce a value which is a Sym, and we can deal with
# everything else later. The one without the quotes will be
# the Symbol.

class _Sym:
    _gal_type = GAL_SYMBOL
    def __init__(self, str):
        self.str = str
    def _Print(self, how_to, indent):
        return self.str
    def Equal(self, val):
        return self.str == val.str
