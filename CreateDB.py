'''
Example of how to create a DB from a text file

Illustrates how to call the DB.CreateDB() function to create a
sqlite DB from a text file.

Part of the AT&T Statistical Dialog Toolkit (ASDT).

Jason D. Williams
jdw@research.att.com
www.research.att.com/people/Williams_Jason_D
'''

# Extend sys.path to include src directory
import os, sys
#sys.path.append(os.path.join(os.path.dirname(__file__),'../../src'))

from DB import CreateDB

DBs = ['LGdb']

def main():
    for db in DBs:
        CreateDB('%s.txt' % (db),'%s.sqlite' % (db))

if (__name__ == '__main__'):
    main()
