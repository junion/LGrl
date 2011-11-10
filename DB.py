'''
Database of listings.

This module implements a sqlite3 database of listings.

To build a database from a text file:

  CreateDB('mydb.txt','mydb.sqlite')

A number of internal optimizations are included in the sqlite3 database,
including column indexing.  Once created, the database is accessed via
an instance of the class DB.  To instantiate a DB, the function InitDB()
is called (once):

  from GlobalConfig import *
  InitConfig()
  config = GetConfig()
  config.add_section('DB')
  config.set('DB','dbStem','mydb')
  from DB import InitDB
  InitDB()

Application code can then can then retrieve a pointer to DB by calling
the function GetDB():

  from DB import GetDB
  db = GetDB()
  fields = db.GetFields()

This construction removes the need to pass handles to the DB through all
the applicaiton code.

DB queries are of the form:

  query['first'].type = 'equals'
  query['first'].equals = 'JASON'
  query['last'].type = 'excludes'
  query['last'].excludes = { 'WILLIAMS': True, 'WILPON': True, }
  query['city'].type = 'excludes'
  query['city'].excludes = {}
  query['state'].type = 'excludes'
  query['state'].excludes = {}

  count = db.GetListingCount(query)
  results = db.GetListingsByQuery(query)

This corresponds to "All listings with (first name equal to JASON) and (last name
not equal to either WILLIAMS or WILPON)".

This module requires that global logging and configuration have been
initialized.  See main README file.

Configuration option:

  dbStem: filestem for database.  The DB module will look for a sqlite DB in <stem>.sqlite

Part of the AT&T Statistical Dialog Toolkit (ASDT).

Jason D. Williams
jdw@research.att.com
www.research.att.com/people/Williams_Jason_D
'''

import sqlite3 as sqlite
import random
import logging
from copy import deepcopy
from GlobalConfig import GetConfig
#import resource
import os, sys
from Utils import CPU, Combinations

MY_ID = 'DB'
_TABLE = 'bus_specs'
_TABLE_COUNTS = 'counts'
_THE_DB = None

def InitDB():
    '''
    Initialize the DB.  This function must be called once (and only once)
    before the DB is accessed.
    '''
    global _THE_DB
    if (_THE_DB == None):
        _THE_DB = DB()
    else:
        raise RuntimeError,'InitDB called more than once'

def KillDB():
    '''
    Kill the DB.  After this is called, InitDB() may be called again
    (for example, to load a different DB).

    NOTE: This only affects future calls to GetDB().  It does not
    unload the old database, nor will it affect existing pointers to
    the old database.
    '''
    global _THE_DB
    if (_THE_DB == None):
        raise RuntimeError,'DB has not been Inited'
    else:
        _THE_DB = None

def GetDB():
    '''
    Return the global DB object.  Application code should call this
    function to get a handle to the DB.
    '''
    global _THE_DB
    return _THE_DB

class DB(object):
    '''
    Wraps a sqlite3 database of listings.
    '''
    def __init__(self):
        '''
        Creates a DB instance.
        '''
        self.appLogger = logging.getLogger(MY_ID)
        self.config = GetConfig()
        self.dbStem = self.config.get(MY_ID,'dbStem')
        self.dbFile = '%s.sqlite' % (self.dbStem)
        self.dbHitCounter = 0
        self.conn = sqlite.connect(self.dbFile)
        self.conn.text_factory = str
        self.cur = self.conn.cursor()
        tableInfo = self._ExecuteSQL("PRAGMA table_info(%s)" % (_TABLE),'all')
        if (len(tableInfo)==0):
            raise RuntimeError,'Could not connect to DB %s' % (self.dbFile)
        self.fieldNames = []
        for colInfo in tableInfo:
            colName = colInfo[1]
            if (colName == 'rowid'):
                continue
            self.fieldNames.append(colName)
        self.appLogger.info('DB has fields: %s' % (self.fieldNames))
        self.rowCount = self._ExecuteSQLOneItem("SELECT count FROM %s WHERE value='all'" % (_TABLE_COUNTS))
        self.fieldSize = {}
        for field in self.fieldNames:
            self.fieldSize[field] = int(self._ExecuteSQLOneItem("SELECT count(*) FROM %s_%s" % (_TABLE_COUNTS,field)))
        self.appLogger.info('Loaded db with %d rows' % (self.rowCount))

    def GetRandomListing(self):
        '''
        Returns a random listing.
        '''
        listing = None
        while (listing == None):
            rowid = random.randint(1,self.rowCount)
            listing = self.GetListingByRowID(rowid)
        self.appLogger.info('listing=%s' % (listing))
        return listing

    def GetListingByRowID(self,rowid):
        '''
        Returns the listing at rowid (an integer)
        '''
        row = self._ExecuteSQL('SELECT %s FROM %s WHERE rowid=%d LIMIT 1' % (','.join(self.fieldNames),_TABLE,rowid))
        listing = {}
        for (i,field) in enumerate(self.fieldNames):
            listing[field] = row[i]
        return listing

    def GetListingsByQuery(self,query):
        '''
        Returns an array of all the listings that match query.  Each listing is
        a dict.
        '''
        where = self._BuildWhereClause(query)
        rows = self._ExecuteSQL('SELECT %s FROM %s WHERE %s' % (','.join(self.fieldNames),_TABLE,where),fetch='all')
        listings = []
        for row in rows:
            if (row == None):
                raise RuntimeError,'row == None'
            listing = {}
            for (i,field) in enumerate(self.fieldNames):
                listing[field] = row[i]
            listings.append(listing)
        return listings

    def GetListingCount(self,query):
        '''
        Returns the number of listings that match query.
        '''
        fields = []
        for field in query:
            if (query[field].type == 'excludes' and len(query[field].excludes)==0):
                continue
            else:
                fields.append(field)
        if (len(fields) == 0):
            count = self.rowCount
        elif (len(fields) == 1 and fields[0] in self.fieldNames):
            # use pre-computed count
            if (query[fields[0]].type == 'equals'):
                val = query[fields[0]].equals
                count = self._ExecuteSQLOneItem("SELECT count FROM %s_%s WHERE value='%s'" % (_TABLE_COUNTS,fields[0],val))
            else:
                excludes = ["'%s'" % (item) for item in query[fields[0]].excludes]
                minusCount = self._ExecuteSQLOneItem("SELECT SUM(count) FROM %s_%s WHERE value IN (%s)" % (_TABLE_COUNTS,fields[0],','.join(excludes)))
                plusCount = self.GetListingCount({})
                count = plusCount - minusCount
        else:
            # do normal count
            where = self._BuildWhereClause(query)
            count = self._ExecuteSQLOneItem('SELECT COUNT(*) FROM %s WHERE %s' % (_TABLE,where))
        return count

    def GetFieldSize(self,field):
        '''
        Returns the number of distinct values in field.
        '''
        result = int(self._ExecuteSQLOneItem("SELECT count(*) FROM %s_%s" % (_TABLE_COUNTS,field)))
        return result

    def GetFieldElementByIndex(self,field,rowid):
        '''
        Returns the rowid-th value of field, where rowid>=1 and
        rowid <= self.GetFieldSize(field).
        '''
        result = self._ExecuteSQLOneItem("SELECT value FROM %s_%s WHERE rowid=%d LIMIT 1" % (_TABLE_COUNTS,field,rowid))
        return result

    def GetFields(self):
        '''
        Returns the list of fields in the DB.
        '''
        return deepcopy(self.fieldNames)

    def GetDBStem(self):
        '''
        Returns the DB stem.  DB file names are of the form
        "dbStem.sqlite"; here the DB stem is "dbStem".
        '''
        return self.dbStem

    def GetDBFile(self):
        '''
        Returns the DB filename.  DB file names are of the form
        "dbStem.sqlite".
        '''
        return self.dbFile

    def RowIterator(self):
        '''
        Return an iterator over all the listings.  Each result
        is a dict.
        '''
        stmt = "SELECT rowid,%s FROM %s" % (','.join(self.fieldNames),_TABLE)
        self.appLogger.info('Query (RowIterator): %s [results omitted for space]' % (stmt))
        self.cur.execute(stmt)
        for row in self.cur:
            result = {}
            for (i,item) in enumerate(row):
                if (i==0):
                    result['rowid'] = int(item)
                else:
                    result[ self.fieldNames[i-1] ] = item
            yield result

    def _ExecuteSQL(self,stmt,fetch='oneRow',noneOK=False):
        self.cur.execute(stmt)
        self.dbHitCounter += 1
        if (fetch == 'all'):
            result = self.cur.fetchall()
        else:
            result = self.cur.fetchone()
        if (not noneOK and result == None):
            raise RuntimeError,'row == None'
        self.appLogger.info('Query: %s [%s]' % (stmt,result))
        return result

    def _ExecuteSQLOneItem(self,stmt):
        row = self._ExecuteSQL(stmt, fetch='oneRow')
        result = row[0]
        return result

    def _BuildWhereClause(self,query):
        whereItems = []
        for field in query:
            if (query[field].type == 'excludes' and len(query[field].excludes)==0):
                continue
            elif (query[field].type == 'equals'):
                whereItems.append("%s = '%s'" % (field,query[field].equals))
            else:
                if (len(query[field].excludes) == 1):
                    whereItems.append("%s != '%s'" % (field,query[field].excludes.keys()[0]))
                else:
                    excludeItems = ["'%s'" % (item) for item in query[field].excludes]
                    whereItems.append("%s NOT IN (%s)" % (field,','.join(excludeItems)))
        return ' AND '.join(whereItems)

    def RunTest(self,testSpec,N):
        '''
        Runs N tests of the DB using a test specified by testSpec

        testSpec is a dict like:

        spec = {
                'first' : 10,
                'last' : 10,
                'city' : 10,
                'state' : None,
                }

        where values indicate:

            None : equals a randomly sampled item
            0 = exludes nothing
            1 = excludes 1 value, etc.

        In each iteration, a random target row is sampled.  Then random values to exclude are
        sampled.  Then the query is run.

        Returns:

            (avRandTime,avQueryTime,longestQueryTime,avReturnedCallees)
        '''
        randomTime = 0.0
        queryTime = 0.0
        longestCountQueryTime = 0.0
        listingCount = 0
        i = 0
        while(i < N):
            startCPU = CPU()
            randomListing = self.GetRandomListing()
            endCPU = CPU()
            randomTime += (endCPU-startCPU)
            query = {}
            for field in testSpec:
                query[field] = _QueryClass()
                if (testSpec[field] == None):
                    query[field].type = 'equals'
                    query[field].equals = randomListing[field]
                else:
                    query[field].type = 'excludes'
                    indexes = random.sample(xrange(self.fieldSize[field]), testSpec[field])
                    excludeItems = dict(zip(["%s" % self.GetFieldElementByIndex(field,index+1) for index in indexes],[True] * testSpec[field]))
                    # excludeItems = dict(zip(["%s%d" % (field,index) for index in indexes],[True] * testSpec[field]))
                    query[field].excludes = excludeItems
            startCPU = CPU()
            count = self.GetListingCount(query)
            endCPU = CPU()
            queryTime += (endCPU-startCPU)
            if ((endCPU-startCPU) > longestCountQueryTime):
                longestCountQueryTime = (endCPU-startCPU)
            listingCount += count
            i += 1
        return (float(randomTime / N),float(queryTime / N),float(longestCountQueryTime),float(1.0 * listingCount / N))

class _QueryClass:
    __slots__ = ['type','equals','excludes']
    def __init__(self):
        pass

def CreateDB(sourceFile,dbfile):
    '''
    Creates a database from text file "sourceFile", and
    writes a new sqlite database to "dbFile".

    sourceFile has the form:

      first,last,city,state
      PHILLIP,MCCANN,RALEIGH,NORTH CAROLINA
      PATRICIA,HOWARD,VALLEJO,CALIFORNIA
      ...

    '''
    rawdata = open(sourceFile, "r")
    line = rawdata.readline()
    line = line.strip()
    fieldNames = line.split(",")
    print "Data file has fields: %s..." % (fieldNames)
    print "Initializing database [%s]..." % (dbfile )
    if os.path.isfile(dbfile):
        os.remove(dbfile)
    dbconn = sqlite.connect(dbfile)
    dbcur = dbconn.cursor()
    createCols = ','.join(['%s VARCHAR' % (fieldName) for fieldName in fieldNames])
    dbcur.execute("CREATE TABLE %s ( rowid INTEGER PRIMARY KEY, %s )" % (_TABLE,createCols))
    dbconn.commit()
    lineno = 0
    fieldNamesStr = ','.join(fieldNames)
    counts = {}
    for fieldName in fieldNames:
        counts[fieldName] = {}
    print "Populating database..."
    for line in rawdata:
        sql = ""
        try:
            lineno += 1
            line = line.strip()
            if line == "":
                continue;
            fields = line.split(",")
            assert(len(fields) == len(fieldNames))
            for (i,fieldName) in enumerate(fieldNames):
                val = fields[i]
                if (val not in counts[fieldName]):
                    counts[fieldName][val] = 0
                counts[fieldName][val] += 1
            fieldsStr = ','.join(["'%s'" % (field) for field in fields])
            sql = "INSERT INTO %s (rowid,%s) VALUES(%d,%s)" % (_TABLE,fieldNamesStr,lineno,fieldsStr)
            dbcur.execute(sql)
        except Exception, err:
            print "createDbFile: processing line number " + str(lineno)
            print "createDbFile: line: " + line
            print "createDbFile: sql: " + sql
            raise
    dbconn.commit()
    print "Inserted " + str(lineno) + " database rows"
    print "Building indexes [%s]..." % dbfile
    dbcur.execute("CREATE INDEX rowid_idx ON %s (rowid)" % (_TABLE))
    for fieldCount in range(1,len(fieldNames)+1):
        for indexFields in Combinations(fieldNames,fieldCount):
            indexName = '_'.join(indexFields)
            print " Building index %s..." % (indexName)
            dbcur.execute("CREATE INDEX idx_%s ON %s (%s)" % (indexName,_TABLE,','.join(indexFields)))
    dbconn.commit()
    print "Building counts tables [%s]..." % dbfile
    for fieldName in fieldNames:
        print " Working on field %s..." % fieldName
        table = 'counts_%s' % (fieldName)
        dbcur.execute("CREATE TABLE %s (value VARCHAR, count INTEGER)" % (table))
        dbconn.commit()
        for val in counts[fieldName]:
            sql = "INSERT INTO %s (value,count) VALUES ('%s',%d)" % (table,val,counts[fieldName][val])
            dbcur.execute(sql)
        dbconn.commit()
    print "Building overall count table [%s]..." % dbfile
    dbcur.execute("CREATE TABLE counts (value VARCHAR, count INTEGER)")
    dbconn.commit()
    sql = "INSERT INTO counts (value,count) VALUES ('all',%d)" % (lineno)
    dbcur.execute(sql)
    dbconn.commit()
    dbconn.close()
    print "Done."
