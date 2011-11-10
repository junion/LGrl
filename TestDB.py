'''
Performs several tests of the name database

This script tests the DB module and the db-1k.sqlite and db-100k.sqlite names databases.
This is the database that the 'name-dialer' example application is based on.

Part of the AT&T Statistical Dialog Toolkit (ASDT).

Jason D. Williams
jdw@research.att.com
www.research.att.com/people/Williams_Jason_D
'''

# Extend sys.path to include src directory
import os, sys
#sys.path.append(os.path.join(os.path.dirname(__file__),'../../src'))

import logging.config
from DB import InitDB, GetDB, KillDB
from GlobalConfig import InitConfig, GetConfig

DBs = ['LGdb']

def main():
    InitConfig()
    config = GetConfig()
    config.add_section('DB')
    logging.config.fileConfig('logging.conf')
    for dbStem in DBs:
        config.set('DB','dbStem',dbStem)
        InitDB()
        db = GetDB()
        dbFile = db.GetDBFile()
        print '*** START : DB = %s ***' % (dbFile)
        print 'Records = %d' % (db.rowCount)
        tests = [
                     {
                      'desc' : 'Get count of all listings with a particular first name',
                      'N' : 1,
                      'spec' : {
                                'bus' : None,
                                'origin' : 0,
                                'destination' : 0,
                                'time' : 0,
                                },
                      },
                     {
                      'desc' : 'Get count of all listings with a particular first name and last name',
                      'N' : 1,
                      'spec' : {
                                'bus' : None,
                                'origin' : None,
                                'destination' : 0,
                                'time' : 0,
                                },
                      },
                     {
                      'desc' : 'Get count of all listings with a particular first name, last name, city, and state',
                      'N' : 1,
                      'spec' : {
                                'bus' : None,
                                'origin' : None,
                                'destination' : None,
                                'time' : None,
                                },
                      },
                     {
                      'desc' : 'Get count of all listings with a particular first name and excluding 50 last names',
                      'N' : 1,
                      'spec' : {
                                'bus' : None,
                                'origin' : 1,
                                'destination' : 0,
                                'time' : 0,
                                },
                      },
                     {
                      'desc' : 'Get count of all listings with a particular first name and excluding 50 last names, 50 cities, and 40 states',
                      'N' : 1,
                      'spec' : {
                                'bus' : None,
                                'origin' : 1,
                                'destination' : 1,
                                'time' : 1,
                                },
                      },
                     {
                      'desc' : 'Get count of all listings with a particular first name and excluding 1 last name, 1 city, and 1 state',
                      'N' : 1,
                      'spec' : {
                                'bus' : None,
                                'origin' : 1,
                                'destination' : 1,
                                'time' : 1,
                                },
                      },
                      ]
        for (i,test) in enumerate(tests):
            print '*** TEST %d : DB = %s ***' % (i,dbFile)
            print 'Description: %s' % (test['desc'])
            print 'Spec: %s' % (test['spec'])
            print 'N: %d' % (test['N'])
            (avRandTime,avQueryTime,longestQueryTime,avReturnedCallees) = db.RunTest(test['spec'],test['N'])
            print 'average randomTime = %f' % (avRandTime)
            print 'average queryTime = %f' % (avQueryTime)
            print 'longest queryTime = %f' % (longestQueryTime)
            print 'average returned callees = %f' % (avReturnedCallees)
            print ''
        KillDB()

if (__name__ == '__main__'):
    main()
