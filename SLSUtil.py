# This file (c) Copyright 1998 - 2002 The MITRE Corporation
#
# This file is part of the Galaxy Communicator system. It is licensed
# under the conditions described in the file LICENSE in the root
# directory of the Galaxy Communicator system.

# Here's where we implement the streams. See sls_verbose.c.

# We don't support the color stuff.

SLSUTIL_DOC = \
"""
GalUtil_Fatal(format, ...):                      conn.ostream.fatal(msg)
GalUtil_Warn(format, ...):                       conn.ostream.warn(msg)
GalUtil_Error(format, ...):                      conn.ostream.error(msg)
GalUtil_Print(level, format, ...):               conn.ostream.write_level(level, msg)
GalUtil_Cprint(level, fore, back, format, ...):  [not implemented]
GalUtil_PInfo1(format, ...):                     conn.ostream.pinfo1(msg)
GalUtil_PInfo2(format, ...):                     conn.ostream.pinfo2(msg)
GalUtil_CPInfo1(fore, back, format, ...):        [not implemented]
GalUtil_CPInfo2(fore, back, format, ...):        [not implemented]
GalUtil_Debug1(format, ...):                     conn.ostream.debug1(msg)
GalUtil_Debug2(format, ...):                     conn.ostream.debug2(msg)
GalUtil_Assert(truth, format, ...):              conn.ostream.p_assert(truth, msg)
GalUtil_VerboseUseColor():                       [not implemented]
GalUtil_VerboseUseBW():                          [not implemented]
GalUtil_CPrint(...):                             [not implemented]

GalUtil_OACheckUsage(argc, argv, oas, first_real_arg): [not implemented]
GalUtil_OAPrintUsage(argc, argv, oas):                 OAPrintUsage(oas)
GalUtil_OAExtract(argc, argv, oas, key, ...):           OAExtract(oas, argv, ostream)
GalUtil_OAExtractAsserting(argc, argv, oas, key, ...): [not implemented]
"""

import os, string, signal, sys

FATAL_LEVEL = 0
WARNING_LEVEL = 1
PINFO1_LEVEL = 2
PINFO2_LEVEL = 3
DEBUG1_LEVEL = 4
DEBUG2_LEVEL = 5

import cGalaxy

cGalaxy.Gal_InitializeStatics()

try:
    VERBOSE_LEVEL = string.atoi(os.environ["GAL_VERBOSE"])
except KeyError:
    VERBOSE_LEVEL = 3

class OStream:
    def __init__(self, *args):
        pass
    def set_verbosity(self, verbosity_level):
        VERBOSE_LEVEL = verbosity_level
        cGalaxy.GalUtil_SetVerbose(verbosity_level)
    def fatal(self, msg):
        if VERBOSE_LEVEL > FATAL_LEVEL:
            self._fatal(msg)
        # Raise a SIGQUIT
        os.kill(os.getpid(), signal.SIGQUIT)
    def p_assert(self, truth, msg):
        if not truth:
            self.fatal(msg)
    def error(self, msg):
        if VERBOSE_LEVEL > FATAL_LEVEL:
            self._error(msg)
    def warn(self, msg):
        if VERBOSE_LEVEL > WARNING_LEVEL:
            self._warn(msg)
    def write_level(self, level, msg):
        if VERBOSE_LEVEL > level:
            self._print(msg, level)
    def write(self, msg):
        self._print(msg, -1)
    def pinfo1(self, msg):
        if VERBOSE_LEVEL > PINFO1_LEVEL:
            self._print(msg, PINFO1_LEVEL)
    def pinfo2(self, msg):
        if VERBOSE_LEVEL > PINFO2_LEVEL:
            self._print(msg, PINFO2_LEVEL)
    def debug1(self, msg):
        if VERBOSE_LEVEL > DEBUG1_LEVEL:
            self._print(msg, DEBUG1_LEVEL)
    def debug2(self, msg):
        if VERBOSE_LEVEL > DEBUG2_LEVEL:
            self._print(msg, DEBUG2_LEVEL)
    # Implementation - override if necessary.
    # These can't be __ private variables, because the
    # class name is prefixed and they thus can't be
    # overridden by inheritance.
    def _fatal(self, msg):
        self._print("  (FATAL ERROR: " + msg + ")", FATAL_LEVEL, sys.stderr)
    def _error(self, msg):
        self._print("  (ERROR: " + msg + ")", FATAL_LEVEL, sys.stderr)
    def _warn(self, msg):
        self._print("  (WARNING: " + msg + ")", WARNING_LEVEL, sys.stderr)
    def _print(self, msg, level, fp = sys.stdout):
        if fp == sys.stdout:
            print msg
        else: fp.write(msg + "\n")
        fp.flush()

# I surrender. Time to write a command-line argument parsing library.

# Specification is kind of like MIT's:

# OAS = [("-utts utts_file", "text utterance file for sequencing",
#        (types.StringType), (Utterance_File)]
#       ("-stdin", "Read sentences from stdin instead of a file")]

# The first element is the argument. The second
# is a description. The third element, if present, is a sequence of
# types, and the fourth element, if present, is a sequence of defaults.
# If there aren't enough types, types.StringType is used; if
# there is a defaults list but not enough defaults, the appropriate
# null value is used (0, 0.0, or ""). If the fourth element is
# present, the return value will contain the defaults if the key
# is not present in the arglist.
# The library produces a dictionary of elements and values, along with
# a modified argument list.

import types

OAError = "OAError"

def OAExtract(oas_list, argv, ostream):
    in_args = argv[:]
    argc = len(in_args)
    i = 0
    # First, preprocess the list so it's easier to
    # deal with.
    OASDict ={}
    result_dict = {}
    for entry in oas_list:
        spec = entry[0]
        desc = entry[1]
        if len(entry) > 2:
            oas_types = entry[2]
            if not oas_types:
                oas_types = []
        else:
            oas_types = []
        if len(entry) > 3:
            defaults = entry[3]
        else:
            defaults = None
        tokens = string.split(spec)
        args = []
        for j in range(len(tokens[1:])):
            # For each token, make sure there's
            # a type and a default.
            if (defaults is not None) and \
               (len(defaults) > j):
                cur_default = defaults[j]
            else:
                cur_default = None
            # If there aren't enough types, use the
            # type of the default, or string.
            if len(oas_types) > j:
                cur_type = oas_types[j]
            elif cur_default is not None:
                cur_type = type(cur_default)
            else:
                cur_type = types.StringType
            if cur_type not in [types.StringType, types.IntType,
                                types.FloatType]:
                ostream.error("Type restriction on %s is not string, float, or integer" % tokens[j + 1])
                raise OAError, OAPrintUsage(oas_list)
            if defaults is not None and cur_default is None:
                if cur_type is types.StringType:
                    defaults.append("")
                elif cur_type is types.IntType:
                    defaults.append(0)
                elif cur_type is types.FloatType:
                    defaults.append(0.0)
            args.append((tokens[j + 1], cur_type))
        OASDict[tokens[0]] = desc, defaults, args
    while i < argc:
        if in_args[i] == "-help":
            raise OAError, OAPrintUsage(oas_list)
        elif OASDict.has_key(in_args[i]):
            # If there's an entry for this key.
            desc, defaults, args = OASDict[in_args[i]]
            # If there aren't enough arguments, punt.
            if i + len(args) >= argc:
                raise OAError, OAPrintUsage(oas_list)
            else:
                j = 0
                total = []
                for arg_name, t in args:
                    # Make sure each arg matches.
                    if t == types.IntType:
                        try:
                            total.append(string.atoi(in_args[i + j + 1]))
                        except:
                            ostream.error("%s is not an integer" % arg_name)
                            raise OAError, OAPrintUsage(oas_list)
                    elif t == types.FloatType:
                        try:
                            total.append(string.atof(in_args[i + j + 1]))
                        except:
                            ostream.error("%s is not an integer" % arg_name)
                            raise OAError, OAPrintUsage(oas_list)
                    elif t == types.StringType:
                        total.append(in_args[i + j + 1])
                    else:
                        ostream.error("Type restriction on %s is string, float, or integer")
                        raise OAError, OAPrintUsage(oas_list)
                    j = j + 1
                result_dict[in_args[i]] = total
                in_args[i:i+j+1] = []
                argc = len(in_args)
        else:
            # If it's an arg but we don't know about it,
            # skip it over.
            i = i + 1
    for key, (desc, defaults, args) in OASDict.items():
        if defaults and not result_dict.has_key(key):
            result_dict[key] = defaults
    return result_dict, in_args

def OAPrintUsage(oas_list):
    specs = []
    descriptions = []
    for entry in oas_list:
        specs.append(entry[0])
        descriptions.append(entry[0] + ": " + entry[1])
    specs.append("-help")
    descriptions.append("-help: print this usage message")
    return string.join(specs), string.joinfields(descriptions, "\n")
