'''
Illustration of a mixed initiative name dialer with
100k names.

To run this dialog manager, see httpd.py

Part of the AT&T Statistical Dialog Toolkit (ASDT).

Jason D. Williams
jdw@research.att.com
www.research.att.com/people/Williams_Jason_D
'''

import logging.config
import logging
import threading
import Queue
from GlobalConfig import *
from DialogManager import SBSarsaDialogManager as DialogManager

    
f_text = '''{c gal_be.launch_query 
                                :inframe "{
    query    {
        place    {
            name    MURRAY AND HAZELWOOD
            type    stop
        }
        type    100
    }
}\n"
                            }'''
    
class DialogThread(threading.Thread):
    def __init__(self,inQueue,outQueue):
        threading.Thread.__init__(self)
        self.appLogger = logging.getLogger('Transcript')
        self.inQueue = inQueue
        self.outQueue = outQueue
        dialogManager = DialogManager()
    
    def run(self):
        while True:
            event = self.inQueue.get()
            self.appLogger.info('Event:\n %s'%str(event))
            self.inQueue.task_done()
            message = {'type':'GALAXYCALL','data':f_text}
            self.outQueue.put(message)
                    
