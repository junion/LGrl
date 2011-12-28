'''
Basic low-level classes for the name dialer dialog systems.

This module implements several low-level classes used for the
name dialer dialog systems:

  Grammar
  UserAction
  SystemAction
  ASRResult

This module requires that global logging, configuration, and
database have been initialized.  See main README file.

Part of the AT&T Statistical Dialog Toolkit (ASDT).

Jason D. Williams
jdw@research.att.com
www.research.att.com/people/Williams_Jason_D
'''

from copy import deepcopy
from GlobalConfig import GetConfig
from DB import GetDB
from Utils import Combination, ConfigSectionToDict
#from WatsonFeatures import ExtractFeatures
#from statlib.stats import lbetai
import math
import logging

class Grammar():
    '''
    Class representing a grammar.  The cardinality of a grammar
    (i.e., how many distinct utterances it can recognize) is
    available in

      grammar.cardinality

    Configuration option:

      [Grammar]
      useSharedGrammars: only relevant when using an interactive dialog manager
      with ASR on the AT&T Speech Mashup platform.  If 'true', then Grammar.GetFullName
      returns the public, shared versions of the grammars (e.g.,
      'asdt-demo-shared.db100k.all').  If 'false', Grammar.GetFullName returns the
      private versions of the grammars (e.g., 'db100k.all').  If you have not
      generated and built your own grammars, set this to 'false'.

    '''
    MY_ID = 'Grammar'
    def __init__(self,name):
        '''
        The "name" of the grammar is either:

          - a field name from the DB
          - "confirm" (which accepts "yes" and "no") only
          - "all" (which accepts any ordered subset of any listing, like
            "JASON" or "JASON WILLIAMS" or "JASON NEW YORK"

        '''
        self.config = GetConfig()
        db = GetDB()
#        assert (name in db.GetFields() or name in ['all','confirm']),'Unknown Grammar name: %s' % (name)
        assert (name in ['route','departure_place','arrival_place','travel_time'] or name in ['all','confirm']),'Unknown Grammar name: %s' % (name)
        
        self.name = name
        if (self.name == 'confirm'):
            self.fullName = 'confirm'
        else:
            stem = db.GetDBStem()
            self.fullName = '%s.%s' % (stem,self.name)
        if (self.config.has_option(self.MY_ID,'useSharedGrammars') and self.config.getboolean(self.MY_ID,'useSharedGrammars')):
            if (self.name == 'all'):
                self.fullName = 'asdt-demo-shared.%s.loc' % (self.fullName)
            else:
                self.fullName = 'asdt-demo-shared.%s' % (self.fullName)
        if (name == 'confirm'):
            self.cardinality = 2
        elif (name == 'all'):
            fields = ['route','departure_place','arrival_place','travel_time']#db.GetFields()
            fieldCount = len(fields)
            fieldCombos = 0
            for r in range(fieldCount):
                fieldCombos += Combination(fieldCount,r)
            self.cardinality = db.GetListingCount({}) * fieldCombos
        else:
            self.cardinality = db.GetFieldSize(self.name)

    def GetFullName(self):
        '''
        Returns the "fullName" of a grammar, i.e.,

          fullName.grxml

        For example, the "name" might be "first", but the "fullName"
        is "db-100k.first"
        '''
        return self.fullName

    def __str__(self):
        return '%s:%d' % (self.name,self.cardinality)

class UserAction():
    '''
    A single user action.  User actions have a type, which is one of

      'ig': in-grammar
      'oog': out of grammar
      'silent': user didnt say anything

    In-grammar utts have content.  Content is a dict, where each key is
    either a database field, or 'confirm' (which takes values "YES" or "NO")
    '''
    def __init__(self,type,content=None):
        '''
        Examples:

          userAction = UserAction('oog')
          userAction = UserAction('ig',{'first':'JASON'})
          userAction = UserAction('ig',{'confirm':'NO'})

        '''
        self.config = GetConfig()
        assert (type in ['ig','oog','non-understanding']),'Unknown UserAction type: %s' % (type)
        if (type == 'ig'):
            assert (not content == None),'Type == ig but content == None'
            db = GetDB()
            fields = ['route','departure_place','arrival_place','travel_time']#db.GetFields()
            for field in content:
                assert (field in fields or field in ['confirm']),'Unknown UserAction field: %s' % (field)
        else:
            assert (content == None),'UserAction type == %s but content not None' % (type)
        self.type = type
        self.content = content

    def __str__(self):
        if (self.type == 'ig'):
            elements = ['%s=%s' % (field,self.content[field]) for field in self.content]
            result = '[%s] %s' % (self.type,','.join(elements))
        else:
            result = '[%s]' % (self.type)
        return result

    def Equals(self,other):
        if (not self.type == other.type):
            return False
        if (not len(self.content) == len(other.content)):
            return False
        for field in self.content:
            if (field not in other.content or not self.content[field] == other.content[field]):
                return False
        return True

class SystemAction:
    '''
    Represents a system action.  System actions have a type:

      type='ask' : Play a prompt to the user and wait for a recognition
      type='transfer' : Play a prompt to the user and transfer the call
      type='hangup' : Play a prompt to the user and hang up

    For type='ask', system actions also have a 'force':

      force='request': Ask a wh-question for a SINGLE slot; e.g., "What is the first name?".
      force='confirm': Ask a yn-confirmation question; e.g., "Jason Williams, is that right?"

    For type='ask', system action also have 'content'.  For force='confirm' this
    is a dict of what is being confirmed; for force='request' this is the
    name of the field being asked.

    All actions can have a 'surface' property which is the surface form of the
    output prompt (i.e., what is passed to TTS)

    For type='transfer', system actions also have a 'destination' which is where
    to send the call (currently this is a placeholder; this application doesnt
    actually transfer calls)

    Finally, for type='ask', system actions have a 'grammarName', which is the
    name of the grammar to use (either the name of a field, 'all', or 'confirm')
    '''
    def __init__(self,type,force=None,content=None,surface=None,destination=None,grammarName=None):
        '''
        For explanation of the constructor fields, see above.

        If grammarName isnt provided, default to 'confirm' for force='confirm' and
        'all' for force='request'.

        Based on the grammarName, a Grammar object is created and stored in
        systemAction.grammar.
        '''
        self.config = GetConfig()
        assert (type in ['ask','inform','initial']),'Unknown SystemAction type: %s' % (type)
        assert (force in [None,'request','confirm']),'Unknown SystemAction force: %s' % (force)
        self.type = type
        self.force = force
        self.content = content
        self.surface = surface
        self.destination = destination
        if (self.type == 'ask'):
            # if grammarName isnt provided, default to 'all'
            if (grammarName == None):
                if (self.force == 'confirm'):
                    self.grammarName = 'confirm'
                else:
                    self.grammarName = 'all'
            else:
                self.grammarName = grammarName
            self.grammar = None #Grammar(self.grammarName)
        else:
            self.grammar = None

    def __str__(self):
        if (self.type == 'ask'):
            if (self.force == 'request'):
                content = self.content
            else:
                content = ','.join(['%s=%s' % (field,self.content[field]) for field in self.content])
#            force = '%s(%s) {%s}' % (self.force,content,self.grammar)
            force = '%s %s' % (self.force,content)
        elif (self.type == 'inform'):
            content = '' #','.join(['%s=%s' % (field,self.content[field]) for field in self.content])
            force = None#travel spec(%s)' % (content)
        elif (self.type == 'initial'):
            force = None
        else:
            raise RuntimeError,'Dont recognize type %s' % (self.type)
        result = '[%s]' % (self.type)
        if (not force == None):
            result = '%s %s' % (result,force)
#        if (not self.surface == None):
#            result = '%s "%s"' % (result,self.surface)
        return result

    def GetJSON(self):
        '''
        Gets JSON for the systemAction.  Used for the web-based demo.
        '''
        if (self.grammar == None):
            grammar = None
        else:
            grammar = self.grammar.GetFullName()
        json = {
          'tts' : self.surface,
          'grammar' : grammar,
        }
        if (self.type == 'ask'):
            json['action'] = 'ask'
        elif (self.type == 'transfer' or self.type == 'hangup'):
            json['action'] = 'endDialog'
        else:
            raise RuntimeError,'Dont recognize type %s' % (self.type)
        return json

class ASRResult:
    '''
    Represents an ASR result.

    Two constructors:

      ASRResult.FromWatson(watsonResult,grammar)
      ASRResult.Simulated(grammar,userActions,probs,isTerminal,correctPosition)

    '''
    MY_ID = 'ASRResult'
    def __init__(self):
        '''
        Not intended to be called directly.  Use one of the two
        constructors ASRResult.FromWatson(...) or
        ASRResult.Simulated(...).
        '''
        self.applogger = logging.getLogger(self.MY_ID)
        self.config = GetConfig()
        self.probTotal = 0.0
        self.correctPosition = None
#        self.watsonResult = None
        self.offListBeliefUpdateMethod = self.config.get('PartitionDistribution','offListBeliefUpdateMethod')
        self.numberOfRoute = self.config.getfloat('BeliefState','numberOfRoute')
        self.numberOfPlace = self.config.getfloat('BeliefState','numberOfPlace')
        self.numberOfTime = self.config.getfloat('BeliefState','numberOfTime')
        self.totalCount = self.numberOfRoute * self.numberOfPlace * self.numberOfPlace * self.numberOfTime

#    @classmethod
#    def FromWatson(cls,watsonResult,grammar):
#        '''
#        Constructor for creating an ASRResult object from a real speech recognition
#        output.
#
#        watsonResult is JSON in the form:
#
#        {
#          'nbest': [
#            { ... },
#            { ... },
#            ...
#          ],
#          'nlu-sisr' : [
#            { 'interp' : {
#                'first' : 'JASON',
#                'last' : 'WILLIAMS'
#                ...
#               },
#            },
#            { 'interp' : {
#                'first' : 'JAMISON',
#                'last' : 'WILLIAMS'
#                ...
#               },
#            },
#            ...
#          ],
#        }
#
#        and grammar is a Grammar object.
#
#        Based on the features in the recognition result, probabilities are estimated
#        for each of the N-Best list entries.
#        '''
#        self = cls()
#        self.grammar = grammar
#        self.isTerminal = False
#        self.userActions = []
#        self.probs = []
#        self.watsonResult = watsonResult
#        db = GetDB()
#        self.fields = ['route','departure_place','arrival_place','travel_time']#db.GetFields()
#        self.fields.append('confirm')
#        if ('nlu-sisr' in watsonResult):
#            for result in watsonResult['nlu-sisr']:
#                content = {}
#                if ('interp' in result):
#                    for field in self.fields:
#                        if (field in result['interp']):
#                            content[field] = result['interp'][field]
#                if (len(content)>0):
#                    self.userActions.append(UserAction('ig',content))
#        if (len(self.userActions) == 0):
#            return self
#        fullGrammarName = self.grammar.GetFullName()
#        fullSectionName = '%s_%s' % (self.MY_ID,fullGrammarName)
#        wildcardSectionName = '%s_*' % (self.MY_ID)
#        if (self.config.has_section(fullSectionName)):
#            sectionName = fullSectionName
#        elif (self.config.has_section(wildcardSectionName)):
#            sectionName = wildcardSectionName
#        else:
#            raise RuntimeError,'Configuration file has neither %s nor %s defined' % (fullSectionName,wildcardSectionName)
#        self.params = ConfigSectionToDict(self.config,sectionName)
#        self.applogger.debug('Params = %s' % (self.params))
#        turn = { 'recoResults': watsonResult, }
#        self.features = [1]
##        asrFeatures = ExtractFeatures(turn)
#        asrFeatures = {}
#        if (None in asrFeatures):
#            self.userActions = []
#            return
#        self.features.extend(asrFeatures)
#        partial = {}
#        if (len(self.userActions) == 1):
#            types = ['correct','offList']
#        else:
#            types = ['correct','onList','offList']
#        for type in types:
#            exponent = 0.0
#            for (i,feature) in enumerate(self.features):
#                exponent += feature * self.params['regression'][type][str(i)]
#            partial[type] = math.exp(exponent)
#        rawProbs = {}
#        sum = 0.0
#        for type in types:
#            sum += partial[type]
#        for type in types:
#            rawProbs[type] = partial[type] / sum
#        self.probs = [ rawProbs['correct'] ]
#        N = len(self.userActions)
#        alpha = self.params['onListFraction']['alpha']
#        beta = self.params['onListFraction']['beta']
#        for n in range(1,len(self.userActions)):
#            bucketLeftEdge = 1.0*(n-1)/N
#            bucketRightEdge = 1.0*n/N
#            betaRight = lbetai(alpha,beta,bucketRightEdge) / lbetai(alpha,beta,1.0)
#            betaLeft = lbetai(alpha,beta,bucketLeftEdge) / lbetai(alpha,beta,1.0)
#            betaPart = betaRight - betaLeft
#            self.probs.append( 1.0 * rawProbs['onList'] * betaPart )
#        self.probTotal = 0.0
#        for prob in self.probs:
#            self.probTotal += prob
#        assert (self.probTotal <= 1.0),'Total probability exceeds 1.0: %f' % (self.probTotal)
#        return self

    @classmethod
    def FromHelios(cls,userActions,probs,isTerminal=False,correctPosition=None):
        '''
        Creates an ASRResult object for use in a simulated environment.

        grammar is a Grammar object.

        userActions is a list of UserAction objects on the N-Best list.  Up to one 'silent'
        userAction can be included.  Do not include an 'oog' action.

        probs is the list of probabilities indicating the ASR probabilities of
        each of the userActions.

        isTerminal indicates if the user hung up.  If not provided, defaults to False.

        correctPosition indicates the position of the correct N-Best list entry.
          None: unknown
          -1: not anywhere on the list
          0: first entry on the list
          1: second entry on the list, etc.
        if not provided, defaults to None
        '''
        self = cls()
        assert (len(userActions) == len(probs)),'In ASRResult, length of userActions (%d) not equal to length of probs (%d)' % (len(userActions),len(probs))
        for userAction in userActions:
            assert (not userAction.type == 'oog'),'userAction type for ASR result cannot be oog -- oog is implicit in left-over mass'
        self.userActions = userActions
        self.probs = probs
        for prob in self.probs:
            self.probTotal += prob
        assert (self.probTotal <= 1.0),'Total probability exceeds 1.0: %f' % (self.probTotal)
        return self

    @classmethod
    def Simulated(cls,grammar,userActions,probs,isTerminal=False,correctPosition=None):
        '''
        Creates an ASRResult object for use in a simulated environment.

        grammar is a Grammar object.

        userActions is a list of UserAction objects on the N-Best list.  Up to one 'silent'
        userAction can be included.  Do not include an 'oog' action.

        probs is the list of probabilities indicating the ASR probabilities of
        each of the userActions.

        isTerminal indicates if the user hung up.  If not provided, defaults to False.

        correctPosition indicates the position of the correct N-Best list entry.
          None: unknown
          -1: not anywhere on the list
          0: first entry on the list
          1: second entry on the list, etc.
        if not provided, defaults to None
        '''
        self = cls()
        assert (len(userActions) == len(probs)),'In ASRResult, length of userActions (%d) not equal to length of probs (%d)' % (len(userActions),len(probs))
        for userAction in userActions:
            assert (not userAction.type == 'oog'),'userAction type for ASR result cannot be oog -- oog is implicit in left-over mass'
        self.grammar = grammar
        self.userActions = userActions
        self.probs = probs
        self.isTerminal = isTerminal
        self.correctPosition=correctPosition
        for prob in self.probs:
            self.probTotal += prob
        assert (self.probTotal <= 1.0),'Total probability exceeds 1.0: %f' % (self.probTotal)
        return self

    def GetTopResult(self):
        '''
        Returns the top user action, or None if the N-Best list is empty.
        '''
        if (len(self.userActions) == 0):
            return None
        else:
            return self.userActions[0]

    def GetProbs(self):
        '''
        Returns an array with ASR probs of the N-Best list
        '''
        return deepcopy(self.probs)

    def __str__(self):
        s = self._GetTranscript(maxShow=5)
        return s

    def _GetTranscript(self,maxShow=1):
        items = []
        for i in range(min(maxShow,len(self.userActions))):
            items.append('%s (%f)' % (self.userActions[i],self.probs[i]))
        if (maxShow < len(self.userActions)):
            items[-1] += ' + %d more' % (len(self.userActions) - maxShow)
        items.append('[rest] (%f)' % (1.0 - self.probTotal))
        s = '\n'.join(items)
        return s

    def __iter__(self):
        '''
        Iterates over the N-Best list; for each entry, outputs a tuple:

          (userAction,prob,offListProb)

        where

          - userAction: userAction object for this entry
          - prob: ASR prob of this entry
          - offListProb: the ASR probability of a userAction which has not (yet)
            been observed on the N-Best list (including 'silence' and 'oog')

        For example, if the grammar cardinality is 11, and 3 entries have been observed
        on the N-Best list so far with probabilities 0.4, 0.2 and 0.1, then offListProb would
        be:

           Mass remaining / remaining number of unseen user actions
           (1.0 - (0.4 + 0.2 + 0.1)) / (11 + 2 - 3) = 0.03

        '''
        self.releasedProb = 0.0
        self.releasedActions = 0
        i = 0
        while (i < len(self.userActions)):
            userAction = self.userActions[i]
            prob = self.probs[i]
            self.releasedProb += prob
            self.releasedActions += 1
#            offListProb = 1.0 * (1.0 - self.releasedProb) / (self.grammar.cardinality + 2 - self.releasedActions)
#            offListProb = 1.0 * (1.0 - self.releasedProb) / (3000000 + 2 - self.releasedActions)
            if self.offListBeliefUpdateMethod in ['plain','heuristicUsingPrior']:
                offListProb = 1.0 * (1.0 - self.releasedProb) / (self.totalCount + 2 - self.releasedActions)
            elif self.offListBeliefUpdateMethod == 'heuristicPossibleActions':
                offListProb = 1.0 - self.releasedProb
            else:
                raise RuntimeError,'Unknown offListBeliefUpdateMethod'
            yield (userAction,prob,offListProb)
            i += 1
