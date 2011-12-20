import urllib, urllib2, time
import cookielib
import json
from GlobalConfig import GetConfig
from DialogModules import UserAction,ASRResult

class UserSimulation(object):
    def __init__(self):
        self.config = GetConfig()
        assert (not self.config==None), 'Config file required'
        assert (self.config.has_option('LGus','LOGIN_PAGE')),'LGus section missing field LOGIN_PAGE'
        self.login_page = self.config.get('LGus','LOGIN_PAGE')
        assert (self.config.has_option('LGus','URL')),'LGus section missing field URL'
        self.url = self.config.get('LGus','URL')
        assert (self.config.has_option('LGus','ID')),'LGus section missing field ID'
        self.id = {'username':self.config.get('LGus','ID')}
        assert (self.config.has_option('LGus','PASSWD')),'LGus section missing field PASSWD'
        self.id['password'] = self.config.get('LGus','PASSWD')
        try:
            data = urllib.urlencode(self.id)
            req = urllib2.Request(self.login_page, data)
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

        req = urllib2.Request('http://%s/services/rest/usr_sim'%self.url, data, header)
        response = self.opener.open(req)
        return response.read()

    def Init(self,errorRate=-1):
        if errorRate == -1:
            self.send_json({'Command':'Start over'})
        else:
            self.send_json({'Command':'Start over','Error rate':errorRate})
        self.goal = json.loads(self.send_json({'Command':'Get user goal'}))

    def TakeTurn(self,systemAction):
        # map systemAction to an LGus action
        if systemAction.force == 'request':
            if systemAction.content == 'all':
                act_str = 'Request(Open)'
            else:
                if systemAction.content == 'route':
                    act_str = 'Request(Bus number)'
                if systemAction.content == 'departure_place':
                    act_str = 'Request(Departure place)'
                if systemAction.content == 'arrival_place':
                    act_str = 'Request(Arrival place)'
                if systemAction.content == 'travel_time':
                    act_str = 'Request(Travel time)'
        elif systemAction.force == 'confirm': 
                if systemAction.content.keys()[0] == 'route':
                    act_str = 'Confirm(Bus number:%s)'%systemAction.content['route']
                if systemAction.content.keys()[0] == 'departure_place':
                    act_str = 'Confirm(Departure place:%s)'%systemAction.content['departure_place']
                if systemAction.content.keys()[0] == 'arrival_place':
                    act_str = 'Confirm(Arrival place:%s)'%systemAction.content['arrival_place']
                if systemAction.content.keys()[0] == 'travel_time':
                    act_str = 'Confirm(Travel time:%s)'%systemAction.content['travel_time']
            
        else:
            raise RuntimeError,'Invalid system action force'
#        print act_str
        json_usr = self.send_json({'System action':act_str,'Approx':True})
#        print json_usr
        usr_act = json.loads(json_usr)
        if usr_act['User action'][0] == 'Non-understanding':
            userActionHyps = [UserAction('non-understanding')]
            probs = [1.0]
            correctPosition = -1
        else:
            ua_dict = {}
            for uact in usr_act['User action']:
                if uact.startswith('Inform'):
                    if uact.find('Bus number') > -1:
                        ua_dict.update({'route':uact.split(':')[1][:-1]})
                    if uact.find('Departure place') > -1:
                        ua_dict.update({'departure_place':uact.split(':')[1][:-1]})
                    if uact.find('Arrival place') > -1:
                        ua_dict.update({'arrival_place':uact.split(':')[1][:-1]})
                    if uact.find('Travel time') > -1:
                        ua_dict.update({'travel_time':uact.split(':')[1][:-1]})
                elif uact.startswith('Affirm'):
                    ua_dict.update({'confirm':'YES'})
                elif uact.startswith('Deny'):
                    ua_dict.update({'confirm':'NO'})
            userActionHyps = [UserAction('ig',ua_dict)]
            probs = [usr_act['Confidence score']]
            correctPosition = 0
        return ASRResult.Simulated(None,userActionHyps,probs,correctPosition=correctPosition)


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
