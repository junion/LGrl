import urllib, urllib2, time
import cookielib
import json
from GlobalConfig import GetConfig

class UserSimulation(object):
    def __init__(self):
        self.config = GetConfig()
        assert (not self.config == None), 'Config file required'
        assert (self.config.has_option('LGus','URL')),'LGus section missing field URL'
        self.url = self.config.get('LGus','URL')
        assert (self.config.has_option('LGus','ID')),'LGus section missing field ID'
        self.id = {'username' :self.config.get('LGus','ID')}
        assert (self.config.has_option('LGus','PASSWD')),'LGus section missing field PASSWD'
        self.id['password'] = self.config.get('LGus','PASSWD')
#        self.url = 'http://128.2.210.190:9090/do_login' # write ur URL here
#        self.id = {'username' : 'dd', #write ur specific key/value pair
#                  'password' : 'ddddd'
#                  }
        try:
            header = {'Cookie':'session_id="cc"'}
            data = urllib.urlencode(self.id)          
            req = urllib2.Request(self.url, data)
            cj = cookielib.CookieJar()
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            response = self.opener.open(req)
            the_page = response.read() 
#            print the_page 
        except Exception, detail: 
            print "Err ", detail 

    def send_json(self,json_data):
        data = json.dumps(json_data)
        clen = len(data)
        
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1',\
                  'Connection':'keep-alive',\
                  'Content-Type': 'application/json',\
                  'Content-Length': clen,\
                  'X-Requested-With':'XMLHttpRequest',\
                  'Accept':'application/json'}
        
        req = urllib2.Request('http://128.2.210.190:9090/services/rest/usr_sim', data, header)
        response = self.opener.open(req)
        return response.read()
    
    def Init(self):
        self.send_json({'Command':'Start over'})
        
    def TakeTurn(self,systemAction):
        # map systemAction to an LGus action
        # self.send_json('System action':'Request(Open)')
        pass
        
        
#temp_data = [{'System action':'Request(Open)'},\
#             {'System action':'Request(Bus number)'},\
#             {'System action':'Confirm(Bus number:28X)'},\
#             {'System action':'Request(Departure place)'},\
#             {'System action':'Confirm(Departure place:CMU)'},\
#             {'System action':'Request(Arrival place)'},\
#             {'System action':'Confirm(Arrival place:DOWNTOWN)'},\
#             {'System action':'Request(Travel time)'},\
#             {'System action':'Confirm(Travel time:now)'}\
#             ]

