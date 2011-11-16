'''
Utilities for dialog systems.

This module contains a collection of utilities useful for
dialog systems.

Part of the AT&T Statistical Dialog Toolkit (ASDT).

Jason D. Williams
jdw@research.att.com
www.research.att.com/people/Williams_Jason_D
'''

from random import random
#import resource
from math import log
import logging
from re import search

def SampleFromDict(dict):
    '''
    Given a dict, representing a multinomial distribution,
    of the form:

      {
        'key1' : prob1,
        'key2' : prob2,
        ...
      }

    sample a key according to the distribution of probs.
    '''
    r = random()
    s = 0.0
    for f in dict:
        s += dict[f]
        if (r < s):
            return f
    raise RuntimeError,'Didnt sample anything from this hash: %s (r=%f)' % (str(dict),r)

def CPU():
    '''
    Returns the number of usage seconds elapsed since starting this process.
    '''
    return 0#(resource.getrusage(resource.RUSAGE_SELF).ru_utime+
            #resource.getrusage(resource.RUSAGE_SELF).ru_stime)

def Combinations(iterable, r):
    '''
    Given an iterable, return an iterable over all combinations of values
    of length r or shorter.
    '''
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = range(r)
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def Combination(n,r):
    '''
    Return the number of ways of choosing r elements from a set of
    size n.
    '''
    top = Factorial(n)
    bottom = Factorial(r) * Factorial(n-r)
    result = top/bottom
    return result

def Factorial(n):
    '''
    Returns n * (n-1) * (n-2) * 2 * 1
    '''
    result = 1
    for i in range(2,n+1):
        result *= i
    return result

def ConfigSectionToDict(config,section):
    '''
    Returns a dict of all items in section of the configuration object
    config.  Guess at their type (float or int or string).
    '''
    dict = {}
    for (option,val) in config.items(section):
        keys = option.split('_')
        d = dict
        lastKey = keys.pop(-1)
        for key in keys:
            if (not key in d):
                d[key] = {}
            d = d[key]
        if (search('\.',val)):
            try:
                valToStore = float(val)
            except ValueError:
                valToStore = val
        else:
            try:
                valToStore = int(val)
            except ValueError:
                valToStore = val
        d[lastKey] = valToStore
    return dict

def IsSubsetOf(dict1,dict2):
    '''
    Return True if dict1 is a subset of dict2 -- i.e., if, for all keys in
    dict1, the key is present in dict2 and dict1[key] == dict2[key]
    '''
    for field in dict1:
        if (field not in dict2):
            return False
        elif (not dict1[field] == dict2[field]):
            return False
    return True
