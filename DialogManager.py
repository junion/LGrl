'''
Two simple dialog managers.

This modules contains two simple dialog managers:

  RigidDialogManager: Asks for each field, one a time, regardless of
  input received so far.  This is useful for running simulations where
  it is necessary that all dialogs follow the same flow.

  DirectedDialogManager: This dialog manager asks for each field one
  at a time.  If it receives no evidence for a field, it stops and asks
  the field again.  As soon as there is sufficient belief in a single
  listing, it transfers the call.  If it asks for all of the slots and
  it has not obtained sufficient belief in a single listing, it proceeds
  by asking for the field with the lowest marginal belief.

  OpenDialogManager: This dialog manager starts by asking "Which listing?"
  If it has low belief in all the slots, it asks the same qustion again.
  If it has high belief in one field but low belief in others, it asks
  specifically for the low belief slots.

A dialog manager implements 2 methods:

  Init(): called to begin a new dialog.  Returns the first system
  action (the system always provides the first action).

  TakeTurn(asrResult): called after the user has taken a turn.  Returns
  the next system action.

For the demonstration, dialog managers also implement GetDisplayJSON(),
which returns JSON used to display dialog state on the demonstration
webpage.

This module requires that global logging, configuration, and database have been
initialized.  See main README file.

Configuration options:

  [DialogManager]
  useAllGrammar: if 'true', always uses the 'all' grammar which recognizes
  any field (and any combination of fields).  If 'false', then for field-specific
  questions (such as "First name?"), uses field-specific grammars, which only
  recognize elements of that field.  Used by all dialog managers.

  acceptThreshold: if belief in the top unique (i.e., count=1) partition is
  higher than this value, the call is transferred.  Otherwise, the system continues
  to ask questions.  Used by DirectedDialogManager and OpenDialogManager.

  openQuestionThreshold: if the maximum marginal belief in any field is below this
  value, the system asks the open question.  Otherwise, it asks slot-specific
  questions.  Only used by the OpenDialogManager.

Part of the AT&T Statistical Dialog Toolkit (ASDT).

Jason D. Williams
jdw@research.att.com
www.research.att.com/people/Williams_Jason_D
'''

import logging
from GlobalConfig import GetConfig
from BeliefState import BeliefState
from DB import GetDB
from DialogModules import SystemAction

MY_ID = 'DialogManager'

class DialogManager(object):
    '''
    Base class.  Not meant to be instantiated on its own.
    '''
    def __init__(self):
        self.appLogger = logging.getLogger(MY_ID)
        self.config = GetConfig()
        self.beliefState = BeliefState()
        self.db = GetDB()
#        self.fields = self.db.GetFields()
        self.prompts = LetsGoPrompts()

    def Init(self):
        pass

    def TakeTurn(self,asrResult):
        pass

    def GetDisplayJSON(self):
        '''
        Returns JSON for displaying the current belief state in the
        web-based demo.
        '''
        result = {
          'joint' : [],
          'marginal': [],
        }
        totalBelief = 0.0
        for (i,partitionEntry) in enumerate(reversed(self.beliefState.partitionDistribution.partitionEntryList)):
            textArray = []
            for field in self.fields:
                if (partitionEntry.partition.fields[field].type == 'equals'):
                    textArray.append(partitionEntry.partition.fields[field].equals)
                else:
                    textArray.append('*')
            textArray.append('(%d)' % partitionEntry.partition.count)
            text = ' '.join(textArray)
            belief = partitionEntry.belief
            totalBelief += belief
            json = {'text': text, 'prob': belief,}
            result['joint'].append(json)
        marginals = self.beliefState.GetMarginals()
        for field in self.db.GetFields():
            if (len(marginals[field]) == 0):
                bestValue = '[empty]'
                bestBelief = 0.0
            else:
                bestValue = marginals[field][-1]['equals']
                bestBelief = marginals[field][-1]['belief']
            json = {'text': '%s: %s' % (field,bestValue), 'prob': bestBelief}
            result['marginal'].append(json)
        return result

class RigidDialogManager(DialogManager):
    '''
    See module header for a description.
    '''
    def __init__(self,iterations=1):
        DialogManager.__init__(self)
        self.prevSysAction = None
        self.useAllGrammar = self.config.getboolean(MY_ID,'useAllGrammar')
        self.iterations = iterations

    def Init(self):
        self.beliefState.Init()
        self.prevSysAction = None
        self.actionsToTake = []
        for i in range(self.iterations):
            for field in self.fields:
                surface = self.prompts.WHQuestion(field)
                if (self.useAllGrammar):
                    grammarName = 'all'
                else:
                    grammarName = field
                sysAction = SystemAction('ask','request',field,surface=surface,grammarName=grammarName)
                self.actionsToTake.append(sysAction)
        sysAction = self.actionsToTake.pop(0)
        self.prevSysAction = sysAction
        return sysAction

    def TakeTurn(self,asrResult):
        self.beliefState.Update(asrResult,self.prevSysAction)
        if (len(self.actionsToTake)==0):
            (travelSpec,belief) = self.beliefState.GetTopUniqueUserGoal()
            if (not travelSpec == None):
                destination = '%s' % (travelSpec)
                surface = self.prompts.BusSchedule(travelSpec)
                result = SystemAction('transfer',content=travelSpec,surface=surface,destination=destination)
            else:
                result = SystemAction('hangup',surface='Sorry, I didnt find anyone matching your request.')
        else:
            result = self.actionsToTake.pop(0)
        self.prevSysAction = result
        return result

class DirectedDialogManager(DialogManager):
    '''
    See module header for a description.
    '''
    def __init__(self):
        DialogManager.__init__(self)
        self.useAllGrammar = self.config.getboolean(MY_ID,'useAllGrammar')
        self.acceptThreshold = self.config.getfloat(MY_ID,'acceptThreshold')

    def Init(self):
        self.beliefState.Init()
        self.fieldCounts = dict([(field,0) for field in self.fields])
        sysAction = self._ChooseAction()
        self.prevSysAction = sysAction
        return sysAction

    def TakeTurn(self,asrResult):
        self.beliefState.Update(asrResult,self.prevSysAction)
        sysAction = self._ChooseAction()
        self.prevSysAction = sysAction
        return sysAction

    def _ChooseAction(self):
        (travelSpec,belief) = self.beliefState.GetTopUniqueUserGoal()
        if (belief > self.acceptThreshold):
            destination = '%s' % (travelSpec)
            surface = self.prompts.BusSchedule(travelSpec)
            sysAction = SystemAction('transfer',content=travelSpec,surface=surface,destination=destination)
        else:
            marginals = self.beliefState.GetMarginals()
            askField = None
            for field in self.fields:
                if (len(marginals[field]) == 0):
                    askField = field
                    break
            if (askField == None):
                minBelief = 1.1
                for field in self.fields:
                    if (marginals[field][-1]['belief'] < minBelief):
                        askField = field
                        minBelief = marginals[field][-1]['belief']
            if (askField == None):
                # should never be here; case added as a check
                self.appLogger.warn('LOGIC ERROR')
                askField = self.fields[0]
            surface = self.prompts.WHQuestion(askField,self.fieldCounts[askField])
            self.fieldCounts[askField] += 1
            if (self.useAllGrammar):
                grammarName = 'all'
            else:
                grammarName = askField
            sysAction = SystemAction('ask','request',askField,surface=surface,grammarName=grammarName)
        return sysAction

class OpenDialogManager(DialogManager):
    '''
    See module header for a description.
    '''
    def __init__(self):
        DialogManager.__init__(self)
        self.fields = ['route','departure_place','arrival_place','travel_time']
        self.useAllGrammar = self.config.getboolean(MY_ID,'useAllGrammar')
        self.acceptThreshold = self.config.getfloat(MY_ID,'acceptThreshold')
        self.openQuestionThreshold = self.config.getfloat(MY_ID,'openQuestionThreshold')

    def Init(self):
        self.beliefState.Init()
        self.fieldCounts = dict([(field,0) for field in self.fields])
        self.fieldCounts['all'] = 0
        sysAction = self._ChooseAction()
        self.prevSysAction = sysAction
        return sysAction

    def TakeTurn(self,asrResult):
        self.beliefState.Update(asrResult,self.prevSysAction)
        sysAction = self._ChooseAction()
        self.prevSysAction = sysAction
        return sysAction

    def _ChooseAction(self):
        (travelSpec,belief) = self.beliefState.GetTopUniqueUserGoal()
        if (belief > self.acceptThreshold):
            destination = '%s' % (travelSpec)
            surface = self.prompts.BusSchedule(travelSpec)
            sysAction = SystemAction('inform',content=travelSpec,surface=surface,destination=destination)
        else:
            marginals = self.beliefState.GetMarginals()
            askField = None
            if (sum([len(marginals[elem]) for elem in marginals]) == 0):
                askField = 'all'
            if (askField == None):
                maxMarginals = []
                for field in self.fields:
                    if (len(marginals[field]) > 0):
                        maxMarginals.append(marginals[field][-1]['belief'])
                if (max(maxMarginals) < self.openQuestionThreshold):
                    askField = 'all'
            if (askField == None):
                for field in self.fields:
                    if (len(marginals[field]) == 0):
                        askField = field
                        break
            if (askField == None):
                minBelief = 1.1
                for field in self.fields:
                    if (marginals[field][-1]['belief'] < minBelief):
                        askField = field
                        minBelief = marginals[field][-1]['belief']
            if (askField == None):
                # should never be here; case added as a check
                self.appLogger.warn('LOGIC ERROR')
                askField = self.fields[0]
            surface = self.prompts.WHQuestion(askField,self.fieldCounts[askField])
            self.fieldCounts[askField] += 1
            if (self.useAllGrammar):
                grammarName = 'all'
            else:
                grammarName = askField
            sysAction = SystemAction('ask','request',askField,surface=surface,grammarName=grammarName)
        return sysAction

class LetsGoPrompts(object):
    '''
    Renders sysActions as TTS-playable prompts.  This is the only
    place (outside of the database) with references to the values of
    the fields ('first','last',etc.)
    '''
    def __init__(self):
        pass

    def WHQuestion(self,field,count=0):
        '''
        Ask for "field", e.g.,

          >>> ndp = NameDialerPrompts()
          >>> ndp.WHQuestion('first')
          What is the first name?
          >>> ndp.WHQuestion('city',1)
          Sorry, what is the city?

        '''
        if (count > 0):
            prefix = 'sorry, '
        else:
            prefix = ''
        if field == 'all':
            body = '%show may I help you?'%prefix
        elif field == 'departure_place':
            body = '%swhat is the departure place?'%prefix
        elif field == 'arrival_place':
            body = '%swhat is the arrival place?'%prefix
        elif field == 'route':
            body = '%swhich bus do you want?'%prefix
        else:
            body = '%swhen are you going to travel?'%prefix
        result = '%s%s' % (body[0].upper(),body[1:])
        return result

    def BusSchedule(self,travelSpec):
        '''
        Prompt to transfer the call to travelSpec (which is a dict)
        '''
        return 'Your bus information is %s, %s, %s, %s' % (travelSpec['route'],travelSpec['departure_place'],travelSpec['arrival_place'],travelSpec['travel_time'])
