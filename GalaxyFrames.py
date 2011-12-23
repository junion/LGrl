#===============================================================================
# Dialog State
#===============================================================================
stateElementsDict = {'initial':{},'request_all':{},'request_departure_place':{},'request_arrival_place':{},'request_travel_time':{},\
					'request_exact_travel_time':{},'request_next_query':{},'request_next_query_error':{},\
					'confirm_route':{},'confirm_departure_place':{},'confirm_arrival_place':{},'confirm_travel_time':{},\
					'confirm_uncovered_place':{},'confirm_uncovered_route':{},'confirm_discontinued_route':{},'confirm_no_stop_matching':{},\
					'inform_welcome':{},'inform_confirm_okay_route':{},'inform_confirm_okay_departure_place':{},\
					'inform_confirm_okay_arrival_place':{},'inform_confirm_okay_travel_time':{},\
					'inform_confirm_okay_uncovered_place':{},'inform_confirm_okay_uncovered_route':{},\
					'inform_confirm_okay_discontinued_route':{},\
					'inform_processing':{},'inform_success':{},'inform_error':{},'inform_subsequent_processing':{},\
					'inform_starting_new_query':{},'inform_uncovered_place':{},'inform_uncovered_route':{},\
                    'inform_discontinued_route':{},'inform_no_stop_matching':{},'inform_quit':{},'inform_generic_tips':{}}

#===============================================================================
# Initial State
#===============================================================================
stateElementsDict['initial']['DialogState'] = '/LetsGoPublic'
stateElementsDict['initial']['Stack'] = '/LetsGoPublic'
stateElementsDict['initial']['Agenda'] = '0:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_one]V,X[dtmf_three]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[finalquit]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[quit]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,X[startover]V,X[stop_name.monument]S,X[stop_name.registered_stop]S,O[turn_timeout:timeout]V,O[yes]V,X[yes]V'
stateElementsDict['initial']['LineConfig'] = 'set_dtmf_len = 1, set_lm = first_query'

#===============================================================================
# Request
#===============================================================================
stateElementsDict['request_all']['DialogState'] = '/LetsGoPublic/PerformTask/GetQuerySpecs/AskHowMayIHelpYou'
stateElementsDict['request_all']['Stack'] = '''//LetsGoPublic/PerformTask/GetQuerySpecs/AskHowMayIHelpYou
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['request_all']['Agenda'] = '''0:
1:O[0_covered_route]S,X[0_covered_route]S,O[0_discontinued_route]S,X[0_discontinued_route]S,O[0_uncovered_route]S,X[0_uncovered_route]S,O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,O[1_singleplace.stop_name.uncovered_place]S,O[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,O[2_departureplace.stop_name.covered_place.covered_neighborhood]S,O[2_departureplace.stop_name.covered_place.monument]S,O[2_departureplace.stop_name.covered_place.registered_stop]S,O[2_departureplace.stop_name.uncovered_place]S,O[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,O[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,O[3_arrivalplace.stop_name.covered_place.monument]S,O[3_arrivalplace.stop_name.covered_place.registered_stop]S,O[3_arrivalplace.stop_name.uncovered_place]S,O[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,O[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
2:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['request_all']['LineConfig'] = 'set_dtmf_len = 1, set_lm = first_query'

stateElementsDict['request_departure_place']['DialogState'] = '/LetsGoPublic/PerformTask/GetQuerySpecs/GetDeparturePlace/RequestDeparturePlace'
stateElementsDict['request_departure_place']['Stack'] = '''/LetsGoPublic/PerformTask/GetQuerySpecs/GetDeparturePlace/RequestDeparturePlace
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetDeparturePlace
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['request_departure_place']['Agenda'] = '''0:O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,O[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,O[2_departureplace.stop_name.covered_place.covered_neighborhood]S,O[2_departureplace.stop_name.covered_place.monument]S,O[2_departureplace.stop_name.covered_place.registered_stop]S
1:X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[dontknow]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,O[1_singleplace.stop_name.uncovered_place]S,O[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dtmf_one]V,X[dtmf_three]V
3:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
4:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['request_departure_place']['LineConfig'] = 'set_dtmf_len = 1, set_lm = place'

stateElementsDict['request_arrival_place']['DialogState'] = '/LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace/RequestArrivalPlace'
stateElementsDict['request_arrival_place']['Stack'] = '''/LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace/RequestArrivalPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['request_arrival_place']['Agenda'] = '''0:O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,O[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,O[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,O[3_arrivalplace.stop_name.covered_place.monument]S,O[3_arrivalplace.stop_name.covered_place.registered_stop]S
1:X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dtmf_one]V,X[dtmf_three]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,O[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,O[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[dontknow]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
4:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['request_arrival_place']['LineConfig'] = 'set_dtmf_len = 1, set_lm = place'

stateElementsDict['request_travel_time']['DialogState'] = '/LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime/RequestTravelTime'
stateElementsDict['request_travel_time']['Stack'] = '''/LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime/RequestTravelTime
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['request_travel_time']['Agenda'] = '''0:O[4_busafterthatrequest]S,O[date_time]S
1:X[4_busafterthatrequest]S,X[date_time]S
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
4:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['request_travel_time']['LineConfig'] = 'set_dtmf_len = 1, set_lm = time'

stateElementsDict['request_exact_travel_time']['DialogState'] = '/LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime/RequestExactTravelTime'
stateElementsDict['request_exact_travel_time']['Stack'] = '''/LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime/RequestExactTravelTime
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['request_exact_travel_time']['Agenda'] = '''0:O[4_busafterthatrequest]S,O[date_time]S
1:X[4_busafterthatrequest]S,X[date_time]S
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
4:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['request_exact_travel_time']['LineConfig'] = 'set_dtmf_len = 1, set_lm = time'

stateElementsDict['request_next_query']['DialogState'] = '/LetsGoPublic/PerformTask/GiveResults/RequestNextQuery'
stateElementsDict['request_next_query']['Stack'] = '''/LetsGoPublic/PerformTask/GiveResults/RequestNextQuery
  /LetsGoPublic/PerformTask/GiveResults
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['request_next_query']['Agenda'] = '''0:O[4_busafterthatrequest]V,O[4_busbeforethatrequest]V,O[startover]V
1:O[finalquit]V,O[quit]V,O[repeat]V,X[startover]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['request_next_query']['LineConfig'] = 'set_dtmf_len = 1, set_lm = next_query'

stateElementsDict['request_next_query_error']['DialogState'] = '/LetsGoPublic/PerformTask/GiveResults/RequestNextQueryError'
stateElementsDict['request_next_query_error']['Stack'] = '''/LetsGoPublic/PerformTask/GiveResults/RequestNextQueryError
  /LetsGoPublic/PerformTask/GiveResults
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['request_next_query_error']['Agenda'] = '''0:O[startover]V
1:O[4_busafterthatrequest]V,O[4_busbeforethatrequest]V,O[finalquit]V,O[quit]V,O[repeat]V,O[startover]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['request_next_query_error']['LineConfig'] = 'set_dtmf_len = 1, set_lm = next_query'

#===============================================================================
# Confirm
#===============================================================================
stateElementsDict['confirm_route']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/query.route_number]/RequestConfirm'
stateElementsDict['confirm_route']['Stack'] = '''/_ExplicitConfirm[/LetsGoPublic/query.route_number]/RequestConfirm
  /_ExplicitConfirm[/LetsGoPublic/query.route_number]
  /LetsGoPublic/PerformTask/GetQuerySpecs/AskHowMayIHelpYou
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['confirm_route']['Agenda'] = '''0:O[dtmf_one]V,O[dtmf_three]V,O[no]V,O[yes]V
1:
2:
3:O[0_covered_route]S,X[0_covered_route]S,O[0_discontinued_route]S,X[0_discontinued_route]S,O[0_uncovered_route]S,X[0_uncovered_route]S,O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,O[1_singleplace.stop_name.uncovered_place]S,O[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,O[2_departureplace.stop_name.covered_place.covered_neighborhood]S,O[2_departureplace.stop_name.covered_place.monument]S,O[2_departureplace.stop_name.covered_place.registered_stop]S,O[2_departureplace.stop_name.uncovered_place]S,O[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,O[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,O[3_arrivalplace.stop_name.covered_place.monument]S,O[3_arrivalplace.stop_name.covered_place.registered_stop]S,O[3_arrivalplace.stop_name.uncovered_place]S,O[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,O[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
4:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
5:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['confirm_route']['LineConfig'] = 'set_dtmf_len = 1, set_lm = yes_no'

stateElementsDict['confirm_departure_place']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/query.departure_place]/RequestConfirm'
stateElementsDict['confirm_departure_place']['Stack'] = '''/_ExplicitConfirm[/LetsGoPublic/query.departure_place]/RequestConfirm
  /_ExplicitConfirm[/LetsGoPublic/query.departure_place]
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetDeparturePlace/RequestDeparturePlace
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetDeparturePlace
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['confirm_departure_place']['Agenda'] = '''0:O[dtmf_one]V,O[dtmf_three]V,O[no]V,O[yes]V
1:
2:O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,O[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,O[2_departureplace.stop_name.covered_place.covered_neighborhood]S,O[2_departureplace.stop_name.covered_place.monument]S,O[2_departureplace.stop_name.covered_place.registered_stop]S
3:X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[dontknow]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
4:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,O[1_singleplace.stop_name.uncovered_place]S,O[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dtmf_one]V,X[dtmf_three]V
5:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
6:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['confirm_departure_place']['LineConfig'] = 'set_dtmf_len = 1, set_lm = yes_no'

stateElementsDict['confirm_arrival_place']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/query.arrival_place]/RequestConfirm'
stateElementsDict['confirm_arrival_place']['Stack'] = '''/_ExplicitConfirm[/LetsGoPublic/query.arrival_place]/RequestConfirm
  /_ExplicitConfirm[/LetsGoPublic/query.arrival_place]
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace/RequestArrivalPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['confirm_arrival_place']['Agenda'] = '''0:O[dtmf_one]V,O[dtmf_three]V,O[no]V,O[yes]V
1:
2:O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,O[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,O[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,O[3_arrivalplace.stop_name.covered_place.monument]S,O[3_arrivalplace.stop_name.covered_place.registered_stop]S
3:X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dtmf_one]V,X[dtmf_three]V
4:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,O[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,O[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[dontknow]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
5:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
6:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['confirm_arrival_place']['LineConfig'] = 'set_dtmf_len = 1, set_lm = yes_no'

stateElementsDict['confirm_travel_time']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/query.travel_time.time]/RequestConfirm'
stateElementsDict['confirm_travel_time']['Stack'] = '''/_ExplicitConfirm[/LetsGoPublic/query.travel_time.time]/RequestConfirm
  /_ExplicitConfirm[/LetsGoPublic/query.travel_time.time]
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime/RequestTravelTime
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['confirm_travel_time']['Agenda'] = '''0:O[dtmf_one]V,O[dtmf_three]V,O[no]V,O[yes]V
1:
2:O[4_busafterthatrequest]S,O[date_time]S
3:X[4_busafterthatrequest]S,X[date_time]S
4:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
5:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
6:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['confirm_travel_time']['LineConfig'] = 'set_dtmf_len = 1, set_lm = yes_no'

stateElementsDict['confirm_uncovered_place']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/uncovered_place]/RequestConfirm'
stateElementsDict['confirm_uncovered_place']['Stack'] = '''//_ExplicitConfirm[/LetsGoPublic/uncovered_place]/RequestConfirm
  /_ExplicitConfirm[/LetsGoPublic/uncovered_place]
  /LetsGoPublic/PerformTask/GetQuerySpecs/AskHowMayIHelpYou
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['confirm_uncovered_place']['Agenda'] = '''0:O[dtmf_one]V,O[dtmf_three]V,O[no]V,O[yes]V
1:
2:
3:O[0_covered_route]S,X[0_covered_route]S,O[0_discontinued_route]S,X[0_discontinued_route]S,O[0_uncovered_route]S,X[0_uncovered_route]S,O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,O[1_singleplace.stop_name.uncovered_place]S,O[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,O[2_departureplace.stop_name.covered_place.covered_neighborhood]S,O[2_departureplace.stop_name.covered_place.monument]S,O[2_departureplace.stop_name.covered_place.registered_stop]S,O[2_departureplace.stop_name.uncovered_place]S,O[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,O[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,O[3_arrivalplace.stop_name.covered_place.monument]S,O[3_arrivalplace.stop_name.covered_place.registered_stop]S,O[3_arrivalplace.stop_name.uncovered_place]S,O[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,O[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
4:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
5:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['confirm_uncovered_place']['LineConfig'] = 'set_dtmf_len = 1, set_lm = yes_no'

stateElementsDict['confirm_uncovered_route']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/uncovered_route]/RequestConfirm'
stateElementsDict['confirm_uncovered_route']['Stack'] = '''/_ExplicitConfirm[/LetsGoPublic/uncovered_route]/RequestConfirm
  /_ExplicitConfirm[/LetsGoPublic/uncovered_route]
  /LetsGoPublic/PerformTask/GetQuerySpecs/AskHowMayIHelpYou
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['confirm_uncovered_route']['Agenda'] = '''0:O[dtmf_one]V,O[dtmf_three]V,O[no]V,O[yes]V
1:
2:
3:O[0_covered_route]S,X[0_covered_route]S,O[0_discontinued_route]S,X[0_discontinued_route]S,O[0_uncovered_route]S,X[0_uncovered_route]S,O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,O[1_singleplace.stop_name.uncovered_place]S,O[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,O[2_departureplace.stop_name.covered_place.covered_neighborhood]S,O[2_departureplace.stop_name.covered_place.monument]S,O[2_departureplace.stop_name.covered_place.registered_stop]S,O[2_departureplace.stop_name.uncovered_place]S,O[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,O[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,O[3_arrivalplace.stop_name.covered_place.monument]S,O[3_arrivalplace.stop_name.covered_place.registered_stop]S,O[3_arrivalplace.stop_name.uncovered_place]S,O[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,O[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
4:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
5:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['confirm_uncovered_route']['LineConfig'] = 'set_dtmf_len = 1, set_lm = yes_no'

stateElementsDict['confirm_discontinued_route']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/discontinued_route]/RequestConfirm'
stateElementsDict['confirm_discontinued_route']['Stack'] = '''/_ExplicitConfirm[/LetsGoPublic/discontinued_route]/RequestConfirm
  /_ExplicitConfirm[/LetsGoPublic/discontinued_route]
  /LetsGoPublic/PerformTask/GetQuerySpecs/AskHowMayIHelpYou
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['confirm_discontinued_route']['Agenda'] = '''0:O[dtmf_one]V,O[dtmf_three]V,O[no]V,O[yes]V
1:
2:
3:O[0_covered_route]S,X[0_covered_route]S,O[0_discontinued_route]S,X[0_discontinued_route]S,O[0_uncovered_route]S,X[0_uncovered_route]S,O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,O[1_singleplace.stop_name.uncovered_place]S,O[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,O[2_departureplace.stop_name.covered_place.covered_neighborhood]S,O[2_departureplace.stop_name.covered_place.monument]S,O[2_departureplace.stop_name.covered_place.registered_stop]S,O[2_departureplace.stop_name.uncovered_place]S,O[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,O[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,O[3_arrivalplace.stop_name.covered_place.monument]S,O[3_arrivalplace.stop_name.covered_place.registered_stop]S,O[3_arrivalplace.stop_name.uncovered_place]S,O[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,O[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
4:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
5:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['confirm_discontinued_route']['LineConfig'] = 'set_dtmf_len = 1, set_lm = yes_no'

stateElementsDict['confirm_no_stop_matching']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/uncovered_place]/RequestConfirm'
stateElementsDict['confirm_no_stop_matching']['Stack'] = '''//_ExplicitConfirm[/LetsGoPublic/uncovered_place]/RequestConfirm
  /_ExplicitConfirm[/LetsGoPublic/uncovered_place]
  /LetsGoPublic/PerformTask/GetQuerySpecs/AskHowMayIHelpYou
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['confirm_no_stop_matching']['Agenda'] = '''0:O[dtmf_one]V,O[dtmf_three]V,O[no]V,O[yes]V
1:
2:
3:O[0_covered_route]S,X[0_covered_route]S,O[0_discontinued_route]S,X[0_discontinued_route]S,O[0_uncovered_route]S,X[0_uncovered_route]S,O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,O[1_singleplace.stop_name.uncovered_place]S,O[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,O[2_departureplace.stop_name.covered_place.covered_neighborhood]S,O[2_departureplace.stop_name.covered_place.monument]S,O[2_departureplace.stop_name.covered_place.registered_stop]S,O[2_departureplace.stop_name.uncovered_place]S,O[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,O[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,O[3_arrivalplace.stop_name.covered_place.monument]S,O[3_arrivalplace.stop_name.covered_place.registered_stop]S,O[3_arrivalplace.stop_name.uncovered_place]S,O[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,O[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
4:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
5:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['confirm_no_stop_matching']['LineConfig'] = 'set_dtmf_len = 1, set_lm = yes_no'

#===============================================================================
# Inform
#===============================================================================
stateElementsDict['inform_welcome']['DialogState'] = '/LetsGoPublic/GiveIntroduction/InformWelcome'
stateElementsDict['inform_welcome']['Stack'] = '''/LetsGoPublic/GiveIntroduction/InformWelcome
  /LetsGoPublic/GiveIntroduction
  /LetsGoPublic'''
stateElementsDict['inform_welcome']['Agenda'] = '''0:
1:O[repeat]V
2:O[0_covered_route]S,O[0_discontinued_route]S,O[0_uncovered_route]S,O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,O[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,O[2_departureplace.stop_name.covered_place.covered_neighborhood]S,O[2_departureplace.stop_name.covered_place.monument]S,O[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,O[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,O[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,O[3_arrivalplace.stop_name.covered_place.monument]S,O[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,O[4_busafterthatrequest]S,X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,O[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_one]V,X[dtmf_three]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[finalquit]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[quit]V,O[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,X[startover]V,X[stop_name.monument]S,X[stop_name.registered_stop]S,O[turn_timeout:timeout]V,O[yes]V,X[yes]V'''
stateElementsDict['inform_welcome']['LineConfig'] = 'set_dtmf_len = 1, set_lm = first_query'

stateElementsDict['inform_confirm_okay_route']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/query.arrival_place]/AcknowledgeConfirm'
stateElementsDict['inform_confirm_okay_route']['Stack'] = '''/_ExplicitConfirm[/LetsGoPublic/query.arrival_place]/AcknowledgeConfirm
  /_ExplicitConfirm[/LetsGoPublic/query.arrival_place]
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_confirm_okay_route']['Agenda'] = '''0:
1:X[dtmf_one]V,X[dtmf_three]V,X[no]V,X[yes]V
2:X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dtmf_one]V,X[dtmf_three]V
3:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[dontknow]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
4:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
5:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_confirm_okay_route']['LineConfig'] = ''

stateElementsDict['inform_confirm_okay_departure_place']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/query.arrival_place]/AcknowledgeConfirm'
stateElementsDict['inform_confirm_okay_departure_place']['Stack'] = '''/_ExplicitConfirm[/LetsGoPublic/query.arrival_place]/AcknowledgeConfirm
  /_ExplicitConfirm[/LetsGoPublic/query.arrival_place]
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_confirm_okay_departure_place']['Agenda'] = '''0:
1:X[dtmf_one]V,X[dtmf_three]V,X[no]V,X[yes]V
2:X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dtmf_one]V,X[dtmf_three]V
3:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[dontknow]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
4:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
5:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_confirm_okay_departure_place']['LineConfig'] = ''

stateElementsDict['inform_confirm_okay_arrival_place']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/query.arrival_place]/AcknowledgeConfirm'
stateElementsDict['inform_confirm_okay_arrival_place']['Stack'] = '''/_ExplicitConfirm[/LetsGoPublic/query.arrival_place]/AcknowledgeConfirm
  /_ExplicitConfirm[/LetsGoPublic/query.arrival_place]
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_confirm_okay_arrival_place']['Agenda'] = '''0:
1:X[dtmf_one]V,X[dtmf_three]V,X[no]V,X[yes]V
2:X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dtmf_one]V,X[dtmf_three]V
3:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[dontknow]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
4:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
5:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_confirm_okay_arrival_place']['LineConfig'] = ''

stateElementsDict['inform_confirm_okay_travel_time']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/query.travel_time.time]/AcknowledgeConfirm'
stateElementsDict['inform_confirm_okay_travel_time']['Stack'] = '''/_ExplicitConfirm[/LetsGoPublic/query.travel_time.time]/AcknowledgeConfirm
  /_ExplicitConfirm[/LetsGoPublic/query.travel_time.time]
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_confirm_okay_travel_time']['Agenda'] = '''0:
1:X[dtmf_one]V,X[dtmf_three]V,X[no]V,X[yes]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,O[finalquit]V,O[quit]V,O[repeat]V,X[startover]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_confirm_okay_travel_time']['LineConfig'] = ''

stateElementsDict['inform_confirm_okay_uncovered_place']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/uncovered_place]/AcknowledgeConfirm'
stateElementsDict['inform_confirm_okay_uncovered_place']['Stack'] = '''/_ExplicitConfirm[/LetsGoPublic/uncovered_place]/AcknowledgeConfirm
  /_ExplicitConfirm[/LetsGoPublic/uncovered_place]
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_confirm_okay_uncovered_place']['Agenda'] = '''0:
1:X[dtmf_one]V,X[dtmf_three]V,X[no]V,X[yes]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
4:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_confirm_okay_uncovered_place']['LineConfig'] = ''

stateElementsDict['inform_confirm_okay_uncovered_route']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/uncovered_route]/AcknowledgeConfirm'
stateElementsDict['inform_confirm_okay_uncovered_route']['Stack'] = '''/_ExplicitConfirm[/LetsGoPublic/uncovered_route]/AcknowledgeConfirm
  /_ExplicitConfirm[/LetsGoPublic/uncovered_route]
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_confirm_okay_uncovered_route']['Agenda'] = '''0:
1:X[dtmf_one]V,X[dtmf_three]V,X[no]V,X[yes]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
4:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_confirm_okay_uncovered_route']['LineConfig'] = ''

stateElementsDict['inform_confirm_okay_discontinued_route']['DialogState'] = '/_ExplicitConfirm[/LetsGoPublic/discontinued_route]/AcknowledgeConfirm'
stateElementsDict['inform_confirm_okay_discontinued_route']['Stack'] = '''/_ExplicitConfirm[/LetsGoPublic/discontinued_route]/AcknowledgeConfirm
  /_ExplicitConfirm[/LetsGoPublic/discontinued_route]
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_confirm_okay_discontinued_route']['Agenda'] = '''0:
1:X[dtmf_one]V,X[dtmf_three]V,X[no]V,X[yes]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
4:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_confirm_okay_discontinued_route']['LineConfig'] = ''

stateElementsDict['inform_processing']['DialogState'] = '/LetsGoPublic/PerformTask/ProcessQuery/InformFirstProcessing'
stateElementsDict['inform_processing']['Stack'] = '''/LetsGoPublic/PerformTask/ProcessQuery/InformFirstProcessing
  /LetsGoPublic/PerformTask/ProcessQuery
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_processing']['Agenda'] = '''0:
1:
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,O[finalquit]V,O[quit]V,O[repeat]V,X[startover]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_processing']['LineConfig'] = 'set_dtmf_len = 1, set_lm = first_query'

stateElementsDict['inform_success']['DialogState'] = '/LetsGoPublic/PerformTask/GiveResults/InformSuccess'
stateElementsDict['inform_success']['Stack'] = '''/LetsGoPublic/PerformTask/GiveResults/InformSuccess
  /LetsGoPublic/PerformTask/GiveResults
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_success']['Agenda'] = '''0:
1:O[4_busafterthatrequest]V,O[4_busbeforethatrequest]V,O[finalquit]V,O[quit]V,O[repeat]V,O[startover]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_success']['LineConfig'] = 'set_dtmf_len = 0, set_lm = next_query'

stateElementsDict['inform_error']['DialogState'] = '/LetsGoPublic/PerformTask/GiveResults/InformError'
stateElementsDict['inform_error']['Stack'] = '''/LetsGoPublic/PerformTask/GiveResults/InformError
  /LetsGoPublic/PerformTask/GiveResults
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_error']['Agenda'] = '''0:
1:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,O[finalquit]V,O[quit]V,O[repeat]V,O[startover]V,X[startover]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_error']['LineConfig'] = 'set_dtmf_len = 0, set_lm = next_query'

stateElementsDict['inform_subsequent_processing']['DialogState'] = '/LetsGoPublic/PerformTask/ProcessQuery/InformSubsequentProcessing'
stateElementsDict['inform_subsequent_processing']['Stack'] = '''/LetsGoPublic/PerformTask/ProcessQuery/InformSubsequentProcessing
  /LetsGoPublic/PerformTask/ProcessQuery
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_subsequent_processing']['Agenda'] = '''0:
1:
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,O[finalquit]V,O[quit]V,O[repeat]V,X[startover]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_subsequent_processing']['LineConfig'] = 'set_dtmf_len = 1, set_lm = first_query'

stateElementsDict['inform_starting_new_query']['DialogState'] = '/LetsGoPublic/PerformTask/GiveResults/InformStartingNewQuery'
stateElementsDict['inform_starting_new_query']['Stack'] = '''/LetsGoPublic/PerformTask/GiveResults/InformStartingNewQuery
  /LetsGoPublic/PerformTask/GiveResults
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_starting_new_query']['Agenda'] = '''0:
1:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,O[finalquit]V,O[quit]V,O[repeat]V,X[startover]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_starting_new_query']['LineConfig ']= 'set_dtmf_len = 0, set_lm = next_query'

stateElementsDict['inform_uncovered_place']['DialogState'] = '/LetsGoPublic/PerformTask/GetQuerySpecs/HandleUncoveredPlace/InformUncoveredPlace'
stateElementsDict['inform_uncovered_place']['Stack'] = '''/LetsGoPublic/PerformTask/GetQuerySpecs/HandleUncoveredPlace/InformUncoveredPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs/HandleUncoveredPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_uncovered_place']['Agenda'] = '''0:
1:X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.uncovered_place]S
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
4:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_uncovered_place']['LineConfig'] = 'set_dtmf_len = 0, set_lm = first_query'

stateElementsDict['inform_uncovered_route']['DialogState'] = '/LetsGoPublic/PerformTask/GetQuerySpecs/GetRoute/InformUncoveredRoute'
stateElementsDict['inform_uncovered_route']['Stack'] = '''/LetsGoPublic/PerformTask/GetQuerySpecs/GetRoute/InformUncoveredRoute
  /_ExplicitConfirm[/LetsGoPublic/discontinued_route]
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_uncovered_route']['Agenda'] = '''0:
1:X[dtmf_one]V,X[dtmf_three]V,X[no]V,X[yes]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
4:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_uncovered_route']['LineConfig'] = 'set_dtmf_len = 1, set_lm = first_query'

stateElementsDict['inform_discontinued_route']['DialogState'] = '/LetsGoPublic/PerformTask/GetQuerySpecs/GetRoute/InformDiscontinuedRoute'
stateElementsDict['inform_discontinued_route']['Stack'] = '''/LetsGoPublic/PerformTask/GetQuerySpecs/GetRoute/InformDiscontinuedRoute
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_discontinued_route']['Agenda'] = '''0:
1:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
2:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''
stateElementsDict['inform_discontinued_route']['LineConfig'] = 'set_dtmf_len = 1, set_lm = first_query'

stateElementsDict['inform_quit']['DialogState'] = '/LetsGoPublic/GreetGoodbye'
stateElementsDict['inform_quit']['Stack'] = '''/LetsGoPublic/GreetGoodbye
  /LetsGoPublic'''
stateElementsDict['inform_quit']['Agenda'] = '''0:
1:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_one]V,X[dtmf_three]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[finalquit]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[quit]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,X[startover]V,X[stop_name.monument]S,X[stop_name.registered_stop]S,O[turn_timeout:timeout]V,O[yes]V,X[yes]V'''
stateElementsDict['inform_quit']['LineConfig'] = 'set_dtmf_len = 1, set_lm = first_query'

stateElementsDict['inform_generic_tips']['DialogState'] = '/LetsGoPublic/InformGenericTips'
stateElementsDict['inform_generic_tips']['Stack'] = '''/LetsGoPublic/InformGenericTips
  /LetsGoPublic'''
stateElementsDict['inform_generic_tips']['Agenda'] = '''0:
1:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_one]V,X[dtmf_three]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[finalquit]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[quit]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,X[startover]V,X[stop_name.monument]S,X[stop_name.registered_stop]S,O[turn_timeout:timeout]V,O[yes]V,X[yes]V'''
stateElementsDict['inform_generic_tips']['LineConfig'] = 'set_dtmf_len = 1, set_lm = first_query'

stateElementsDict['inform_no_stop_matching']['DialogState'] = '/LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace/RetrieveArrivalStops/InformNoArrivalStopMatching'
stateElementsDict['inform_no_stop_matching']['Stack'] = '''/LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace/RetrieveArrivalStops/InformNoArrivalStopMatching
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace/RetrieveArrivalStops
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
stateElementsDict['inform_no_stop_matching']['Agenda'] = '''0:
1:
2:X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dtmf_one]V,X[dtmf_three]V
3:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[dontknow]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
4:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
5:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V
'''
stateElementsDict['inform_no_stop_matching']['LineConfig'] = 'set_dtmf_len = 0, set_lm = first_query'

#===============================================================================
# Utterance
#===============================================================================
utterElementsDict = {'inform_welcome':{},'inform_how_to_get_help':{},'request_all':{},\
					'request_departure_place':{},'request_arrival_place':{},'request_travel_time':{},'request_exact_travel_time':{},\
					'request_next_query':{},'request_next_query_error':{},\
					'confirm_route':{},'confirm_departure_place':{},'confirm_arrival_place':{},'confirm_travel_time':{},\
					'confirm_uncovered_place':{},'confirm_uncovered_route':{},'confirm_discontinued_route':{},'confirm_no_stop_matching':{},\
					'inform_welcome':{},'inform_confirm_okay':{},'inform_processing':{},'inform_success':{},'inform_error':{},\
					'inform_subsequent_processing':{},'inform_starting_new_query':{},'inform_uncovered_place':{},\
					'inform_uncovered_route':{},'inform_discontinued_route':{},'inform_no_stop_matching':{},\
                    'inform_quit':{},'inform_generic_tips':{}}

#===============================================================================
# Initial
#===============================================================================
utterElementsDict['inform_welcome']['DialogAct'] = 'inform'
utterElementsDict['inform_welcome']['FloorState'] = 'system'
utterElementsDict['inform_welcome']['Object'] = 'welcome'
utterElementsDict['inform_welcome']['Query'] = ''
utterElementsDict['inform_welcome']['Result'] = ''
utterElementsDict['inform_welcome']['Agent'] = ''
utterElementsDict['inform_welcome']['Version'] = ''
utterElementsDict['inform_welcome']['Option'] = '''   :non-listening "true"
   :non-repeatable "true"
'''

utterElementsDict['inform_how_to_get_help']['DialogAct'] = 'inform'
utterElementsDict['inform_how_to_get_help']['FloorState'] = 'free'
utterElementsDict['inform_how_to_get_help']['Object'] = 'how_to_get_help'
utterElementsDict['inform_how_to_get_help']['Query'] = ''
utterElementsDict['inform_how_to_get_help']['Result'] = ''
utterElementsDict['inform_how_to_get_help']['Agent'] = ''
utterElementsDict['inform_how_to_get_help']['Version'] = ''
utterElementsDict['inform_how_to_get_help']['Option'] = ''

#===============================================================================
# Request
#===============================================================================
utterElementsDict['request_all']['DialogAct'] = 'request'
utterElementsDict['request_all']['FloorState'] = 'user'
utterElementsDict['request_all']['Object'] = 'how_may_i_help_you_directed'
utterElementsDict['request_all']['Query'] = 'ExCount	0\n'
utterElementsDict['request_all']['Result'] = ''
utterElementsDict['request_all']['Agent'] = ''
utterElementsDict['request_all']['Version'] = ''
utterElementsDict['request_all']['Option'] = ''

utterElementsDict['request_departure_place']['DialogAct'] = 'request'
utterElementsDict['request_departure_place']['FloorState'] = 'user'
utterElementsDict['request_departure_place']['Object'] = 'query.departure_place'
utterElementsDict['request_departure_place']['Query'] = ''
utterElementsDict['request_departure_place']['Result'] = ''
utterElementsDict['request_departure_place']['Agent'] = ''
utterElementsDict['request_departure_place']['Version'] = ''
utterElementsDict['request_departure_place']['Option'] = ''

utterElementsDict['request_arrival_place']['DialogAct'] = 'request'
utterElementsDict['request_arrival_place']['FloorState'] = 'user'
utterElementsDict['request_arrival_place']['Object'] = 'query.arrival_place'
utterElementsDict['request_arrival_place']['Query'] = ''
utterElementsDict['request_arrival_place']['Result'] = ''
utterElementsDict['request_arrival_place']['Agent'] = ''
utterElementsDict['request_arrival_place']['Version'] = ''
utterElementsDict['request_arrival_place']['Option'] = ''

utterElementsDict['request_travel_time']['DialogAct'] = 'request'
utterElementsDict['request_travel_time']['FloorState'] = 'user'
utterElementsDict['request_travel_time']['Object'] = 'query.travel_time'
utterElementsDict['request_travel_time']['Query'] = ''
utterElementsDict['request_travel_time']['Result'] = ''
utterElementsDict['request_travel_time']['Agent'] = 'agent	/LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime/RequestTravelTime\n'
utterElementsDict['request_travel_time']['Version'] = ''
utterElementsDict['request_travel_time']['Option'] = ''

utterElementsDict['request_exact_travel_time']['DialogAct'] = 'request'
utterElementsDict['request_exact_travel_time']['FloorState'] = 'user'
utterElementsDict['request_exact_travel_time']['Object'] = 'exact_travel_time'
utterElementsDict['request_exact_travel_time']['Query'] = ''
utterElementsDict['request_exact_travel_time']['Result'] = ''
utterElementsDict['request_exact_travel_time']['Agent'] = ''
utterElementsDict['request_exact_travel_time']['Version'] = ''
utterElementsDict['request_exact_travel_time']['Option'] = ''

utterElementsDict['request_next_query']['DialogAct'] = 'request'
utterElementsDict['request_next_query']['FloorState'] = 'user'
utterElementsDict['request_next_query']['Object'] = 'next_query'
utterElementsDict['request_next_query']['Query'] = ''
utterElementsDict['request_next_query']['Result'] = ''
utterElementsDict['request_next_query']['Agent'] = ''
utterElementsDict['request_next_query']['Version'] = ''
utterElementsDict['request_next_query']['Option'] = '''   :non-repeatable "true"
'''

utterElementsDict['request_next_query_error']['DialogAct'] = 'request'
utterElementsDict['request_next_query_error']['FloorState'] = 'user'
utterElementsDict['request_next_query_error']['Object'] = 'next_query_error'
utterElementsDict['request_next_query_error']['Query'] = ''
utterElementsDict['request_next_query_error']['Result'] = ''
utterElementsDict['request_next_query_error']['Agent'] = ''
utterElementsDict['request_next_query_error']['Version'] = ''
utterElementsDict['request_next_query_error']['Option'] = ''

#===============================================================================
# Confirm 
#===============================================================================
utterElementsDict['confirm_route']['DialogAct'] = 'explicit_confirm'
utterElementsDict['confirm_route']['FloorState'] = 'user'
utterElementsDict['confirm_route']['Object'] = '/LetsGoPublic/query.route_number'
utterElementsDict['confirm_route']['Query'] = ''
utterElementsDict['confirm_route']['Result'] = ''
utterElementsDict['confirm_route']['Agent'] = ''
utterElementsDict['confirm_route']['Version'] = ''
utterElementsDict['confirm_route']['Option'] = ''

utterElementsDict['confirm_departure_place']['DialogAct'] = 'explicit_confirm'
utterElementsDict['confirm_departure_place']['FloorState'] = 'user'
utterElementsDict['confirm_departure_place']['Object'] = '/LetsGoPublic/query.departure_place'
utterElementsDict['confirm_departure_place']['Query'] = ''
utterElementsDict['confirm_departure_place']['Result'] = ''
utterElementsDict['confirm_departure_place']['Agent'] = ''
utterElementsDict['confirm_departure_place']['Version'] = ''
utterElementsDict['confirm_departure_place']['Option'] = ''

utterElementsDict['confirm_arrival_place']['DialogAct'] = 'explicit_confirm'
utterElementsDict['confirm_arrival_place']['FloorState'] = 'user'
utterElementsDict['confirm_arrival_place']['Object'] = '/LetsGoPublic/query.arrival_place'
utterElementsDict['confirm_arrival_place']['Query'] = ''
utterElementsDict['confirm_arrival_place']['Result'] = ''
utterElementsDict['confirm_arrival_place']['Agent'] = ''
utterElementsDict['confirm_arrival_place']['Version'] = ''
utterElementsDict['confirm_arrival_place']['Option'] = ''

utterElementsDict['confirm_travel_time']['DialogAct'] = 'explicit_confirm'
utterElementsDict['confirm_travel_time']['FloorState'] = 'user'
utterElementsDict['confirm_travel_time']['Object'] = '/LetsGoPublic/query.travel_time.time'
utterElementsDict['confirm_travel_time']['Query'] = ''
utterElementsDict['confirm_travel_time']['Result'] = ''
utterElementsDict['confirm_travel_time']['Agent'] = ''
utterElementsDict['confirm_travel_time']['Version'] = ''
utterElementsDict['confirm_travel_time']['Option'] = ''

utterElementsDict['confirm_uncovered_place']['DialogAct'] = 'explicit_confirm'
utterElementsDict['confirm_uncovered_place']['FloorState'] = 'user'
utterElementsDict['confirm_uncovered_place']['Object'] = '/LetsGoPublic/uncovered_place'
utterElementsDict['confirm_uncovered_place']['Query'] = ''
utterElementsDict['confirm_uncovered_place']['Result'] = ''
utterElementsDict['confirm_uncovered_place']['Agent'] = ''
utterElementsDict['confirm_uncovered_place']['Version'] = ''
utterElementsDict['confirm_uncovered_place']['Option'] = ''

utterElementsDict['confirm_uncovered_route']['DialogAct'] = 'explicit_confirm'
utterElementsDict['confirm_uncovered_route']['FloorState'] = 'user'
utterElementsDict['confirm_uncovered_route']['Object'] = '/LetsGoPublic/uncovered_route'
utterElementsDict['confirm_uncovered_route']['Query'] = ''
utterElementsDict['confirm_uncovered_route']['Result'] = ''
utterElementsDict['confirm_uncovered_route']['Agent'] = ''
utterElementsDict['confirm_uncovered_route']['Version'] = ''
utterElementsDict['confirm_uncovered_route']['Option'] = ''

utterElementsDict['confirm_discontinued_route']['DialogAct'] = 'explicit_confirm'
utterElementsDict['confirm_discontinued_route']['FloorState'] = 'user'
utterElementsDict['confirm_discontinued_route']['Object'] = '/LetsGoPublic/discontinued_route'
utterElementsDict['confirm_discontinued_route']['Query'] = ''
utterElementsDict['confirm_discontinued_route']['Result'] = ''
utterElementsDict['confirm_discontinued_route']['Agent'] = ''
utterElementsDict['confirm_discontinued_route']['Version'] = ''
utterElementsDict['confirm_discontinued_route']['Option'] = ''

utterElementsDict['confirm_no_stop_matching']['DialogAct'] = 'explicit_confirm'
utterElementsDict['confirm_no_stop_matching']['FloorState'] = 'user'
utterElementsDict['confirm_no_stop_matching']['Object'] = '/LetsGoPublic/uncovered_place'
utterElementsDict['confirm_no_stop_matching']['Query'] = ''
utterElementsDict['confirm_no_stop_matching']['Result'] = ''
utterElementsDict['confirm_no_stop_matching']['Agent'] = ''
utterElementsDict['confirm_no_stop_matching']['Version'] = ''
utterElementsDict['confirm_no_stop_matching']['Option'] = ''

#===============================================================================
# Inform
#===============================================================================
utterElementsDict['inform_confirm_okay']['DialogAct'] = 'inform'
utterElementsDict['inform_confirm_okay']['FloorState'] = 'free'
utterElementsDict['inform_confirm_okay']['Object'] = 'confirm_okay'
utterElementsDict['inform_confirm_okay']['Query'] = ''
utterElementsDict['inform_confirm_okay']['Result'] = ''
utterElementsDict['inform_confirm_okay']['Agent'] = ''
utterElementsDict['inform_confirm_okay']['Version'] = ''
utterElementsDict['inform_confirm_okay']['Option'] = ''

utterElementsDict['inform_processing']['DialogAct'] = 'inform'
utterElementsDict['inform_processing']['FloorState'] = 'free'
utterElementsDict['inform_processing']['Object'] = 'looking_up_database_first'
utterElementsDict['inform_processing']['Query'] = ''
utterElementsDict['inform_processing']['Result'] = ''
utterElementsDict['inform_processing']['Agent'] = ''
utterElementsDict['inform_processing']['Version'] = ''
utterElementsDict['inform_processing']['Option'] = ''

utterElementsDict['inform_success']['DialogAct'] = 'inform'
utterElementsDict['inform_success']['FloorState'] = 'free'
utterElementsDict['inform_success']['Object'] = 'result'
utterElementsDict['inform_success']['Query'] = ''
utterElementsDict['inform_success']['Result'] = ''
utterElementsDict['inform_success']['Agent'] = ''
utterElementsDict['inform_success']['Version'] = ''
utterElementsDict['inform_success']['Option'] = '''   :non-listening "true"
   :non-repeatable "true"
'''

utterElementsDict['inform_error']['DialogAct'] = 'inform'
utterElementsDict['inform_error']['FloorState'] = 'free'
utterElementsDict['inform_error']['Object'] = 'error'
utterElementsDict['inform_error']['Query'] = ''
utterElementsDict['inform_error']['Result'] = ''
utterElementsDict['inform_error']['Agent'] = ''
utterElementsDict['inform_error']['Version'] = ''
utterElementsDict['inform_error']['Option'] = ''

utterElementsDict['inform_subsequent_processing']['DialogAct'] = 'inform'
utterElementsDict['inform_subsequent_processing']['FloorState'] = 'free'
utterElementsDict['inform_subsequent_processing']['Object'] = 'looking_up_database_subsequent'
utterElementsDict['inform_subsequent_processing']['Query'] = ''
utterElementsDict['inform_subsequent_processing']['Result'] = ''
utterElementsDict['inform_subsequent_processing']['Agent'] = ''
utterElementsDict['inform_subsequent_processing']['Version'] = ''
utterElementsDict['inform_subsequent_processing']['Option'] = ''

utterElementsDict['inform_starting_new_query']['DialogAct'] = 'inform'
utterElementsDict['inform_starting_new_query']['FloorState'] = 'free'
utterElementsDict['inform_starting_new_query']['Object'] = 'starting_new_query'
utterElementsDict['inform_starting_new_query']['Query'] = ''
utterElementsDict['inform_starting_new_query']['Result'] = ''
utterElementsDict['inform_starting_new_query']['Agent'] = ''
utterElementsDict['inform_starting_new_query']['Version'] = ''
utterElementsDict['inform_starting_new_query']['Option'] = ''

utterElementsDict['inform_uncovered_place']['DialogAct'] = 'inform'
utterElementsDict['inform_uncovered_place']['FloorState'] = 'free'
utterElementsDict['inform_uncovered_place']['Object'] = 'uncovered_place'
utterElementsDict['inform_uncovered_place']['Query'] = ''
utterElementsDict['inform_uncovered_place']['Result'] = ''
utterElementsDict['inform_uncovered_place']['Agent'] = ''
utterElementsDict['inform_uncovered_place']['Version'] = ''
utterElementsDict['inform_uncovered_place']['Option'] = ''

utterElementsDict['inform_uncovered_route']['DialogAct'] = 'inform'
utterElementsDict['inform_uncovered_route']['FloorState'] = 'free'
utterElementsDict['inform_uncovered_route']['Object'] = 'uncovered_route'
utterElementsDict['inform_uncovered_route']['Query'] = ''
utterElementsDict['inform_uncovered_route']['Result'] = ''
utterElementsDict['inform_uncovered_route']['Agent'] = ''
utterElementsDict['inform_uncovered_route']['Version'] = ''
utterElementsDict['inform_uncovered_route']['Option'] = ''

utterElementsDict['inform_discontinued_route']['DialogAct'] = 'inform'
utterElementsDict['inform_discontinued_route']['FloorState'] = 'free'
utterElementsDict['inform_discontinued_route']['Object'] = 'discontinued_route'
utterElementsDict['inform_discontinued_route']['Query'] = ''
utterElementsDict['inform_discontinued_route']['Result'] = ''
utterElementsDict['inform_discontinued_route']['Agent'] = ''
utterElementsDict['inform_discontinued_route']['Version'] = ''
utterElementsDict['inform_discontinued_route']['Option'] = ''

utterElementsDict['inform_no_stop_matching']['DialogAct'] = 'inform'
utterElementsDict['inform_no_stop_matching']['FloorState'] = 'free'
utterElementsDict['inform_no_stop_matching']['Object'] = 'no_stop_matching'
utterElementsDict['inform_no_stop_matching']['Query'] = ''
utterElementsDict['inform_no_stop_matching']['Result'] = ''
utterElementsDict['inform_no_stop_matching']['Agent'] = ''
utterElementsDict['inform_no_stop_matching']['Version'] = ''
utterElementsDict['inform_no_stop_matching']['Option'] = ''

utterElementsDict['inform_quit']['DialogAct'] = 'inform'
utterElementsDict['inform_quit']['FloorState'] = 'free'
utterElementsDict['inform_quit']['Object'] = 'goodbye'
utterElementsDict['inform_quit']['Query'] = ''
utterElementsDict['inform_quit']['Result'] = ''
utterElementsDict['inform_quit']['Agent'] = ''
utterElementsDict['inform_quit']['Version'] = ''
utterElementsDict['inform_quit']['Option'] = ''

utterElementsDict['inform_generic_tips']['DialogAct'] = 'inform'
utterElementsDict['inform_generic_tips']['FloorState'] = 'free'
utterElementsDict['inform_generic_tips']['Object'] = 'generic_tips'
utterElementsDict['inform_generic_tips']['Query'] = ''
utterElementsDict['inform_generic_tips']['Result'] = ''
utterElementsDict['inform_generic_tips']['Agent'] = ''
utterElementsDict['inform_generic_tips']['Version'] = ''
utterElementsDict['inform_generic_tips']['Option'] = '''   :non-listening "true"
   :non-repeatable "true"
'''

#===============================================================================
# Dialog State Template
#===============================================================================
dialogStateTemplate = '''"turn_number = ${turn_number}
notify_prompts = ${notify_prompts}
dialog_state = ${dialog_state}
nonu_threshold = 0.0000
stack = {
${stack}
}
agenda = {
${agenda}
}
input_line_config = {
${input_line_config}
}"'''

def MakeDialogState(stateType,turnNumber,notifyPrompts):
	import logging
	appLogger = logging.getLogger('DialogThread')

#	appLogger.info('%s'%stateType)

	content = dialogStateTemplate
#	appLogger.info('%s'%content)
	elements = stateElementsDict[stateType]  
	
	content = content.replace('${turn_number}',str(turnNumber))
#	appLogger.info('%s'%content)
	content = content.replace('${notify_prompts}',notifyPrompts)
#	appLogger.info('%s'%content)
	content = content.replace('${dialog_state}',elements['DialogState'])
#	appLogger.info('%s'%content)
	content = content.replace('${stack}',elements['Stack'])
#	appLogger.info('%s'%content)
	content = content.replace('${agenda}',elements['Agenda'])
#	appLogger.info('%s'%content)
	content = content.replace('${input_line_config}',elements['LineConfig'])
#	appLogger.info('%s'%content)

	return content

#===============================================================================
# Dialog State Message Template
#===============================================================================
dialogStateMessage = '''{c main
     :dialog_state ${dialog_state}}'''
#'''
#{c main
#    :event_level "high"
#    :event_type "dialog_state_change"
#    :properties {c properties
#                   :dialog_state ${dialog_state}}}'''

def MakeDialogStateMessage(stateType,turnNumber,notifyPrompts):
	content = dialogStateMessage

	content = content.replace('${dialog_state}',MakeDialogState(stateType,turnNumber,notifyPrompts))

	message = {'type':'GALAXYACTIONCALL',
			   'content':content}
	return message

#===============================================================================
# System Utterance Message Template
#===============================================================================
systemUtterance = '''
{c main
    :action_level "high"
    :action_type "system_utterance"
    :properties {c properties
                   :dialog_act "${dialog_act}"
                   :dialog_state ${dialog_state}
       :dialog_state_index "${dialog_state_index}"
       :final_floor_status "${final_floor_status}"
       :id "DialogManager-${sess_id}:${id_suffix}"
       :inframe "start
{
act	${dialog_act}
object	${object}
_repeat_counter	0
${query}${result}${agent}${version}system_version	1
}
end
"
${option}   :utt_count "${utt_count}" }}'''

def MakeSystemUtterance(utterType,stateType,turnNumber,notifyPrompts,dialogStateIndex,sessionID,idSuffix,uttCount,query,result,version):
	import logging
	appLogger = logging.getLogger('DialogThread')
	content = systemUtterance
	appLogger.info('%s'%utterType)
	if utterType.startswith('inform_confirm_okay'):
		utterType = 'inform_confirm_okay'
	elements = utterElementsDict[utterType]  
	appLogger.info('0')
	
	content = content.replace('${dialog_act}',elements['DialogAct'])
	appLogger.info('1')
	content = content.replace('${final_floor_status}',elements['FloorState'])
	appLogger.info('2')
	content = content.replace('${object}',elements['Object'])
	appLogger.info('3')
	if query == '' and elements['Query'] != '':
		query = elements['Query']
	content = content.replace('${query}',query)
	appLogger.info('4')
	content = content.replace('${result}',result)
	appLogger.info('5')
	content = content.replace('${agent}',elements['Agent'])
	appLogger.info('6')
	content = content.replace('${version}',version)
	appLogger.info('7')
	content = content.replace('${option}',elements['Option'])
	appLogger.info('8')
	content = content.replace('${dialog_state}',MakeDialogState(stateType,turnNumber,notifyPrompts))
	appLogger.info('9')
	content = content.replace('${dialog_state_index}',str(dialogStateIndex))
	appLogger.info('10')
	content = content.replace('${sess_id}',sessionID)
	appLogger.info('11')
	content = content.replace('${id_suffix}','%03d'%idSuffix)
	appLogger.info('12')
	content = content.replace('${utt_count}',str(uttCount))
	appLogger.info('13')

	message = {'type':'GALAXYACTIONCALL',
			   'content':content}
	return message


#===============================================================================
# Backend Query Template
#===============================================================================
placeQuery = '{c gal_be.launch_query\n\
:inframe "{\n\
query {\n\
type\t100\n\
place\t{\n\
name\t${name}\n\
type\t${type}\n\
}\n\
}\n\
}\n\
"\n\
}'

def MakeDeparturePlaceQuery(querySpec):
	import logging
	appLogger = logging.getLogger('DialogThread')
	appLogger.info('Make query for %s %s'%(querySpec['departure_place_type'],querySpec['departure_place']))
	content = placeQuery
	
	content = content.replace('${name}',querySpec['departure_place'])
	content = content.replace('${type}',querySpec['departure_place_type'])

	appLogger.info('Done')

	message = {'type':'GALAXYCALL',
			   'content':content}
	return message

def MakeArrivalPlaceQuery(querySpec):
	import logging
	appLogger = logging.getLogger('DialogThread')
	appLogger.info('Make query for %s %s'%(querySpec['arrival_place_type'],querySpec['arrival_place']))
	content = placeQuery
	
	content = content.replace('${name}',querySpec['arrival_place'])
	content = content.replace('${type}',querySpec['arrival_place_type'])

	appLogger.info('Done')

	message = {'type':'GALAXYCALL',
			   'content':content}
	return message


#tempQuery = '''{c gal_be.launch_query
#:inframe "{
#query {
#type	2
#travel_time	{
#date	{
#month	12
#day	10
#year	2011
#weekday	6
#}
#
#period_spec	now 
#time	{
#value	1305
#now	true
#type	departure
#}
#
#}
#
#departure_place	{
#name	CMU
#type	stop
#}
#
#arrival_place	{
#name	AIRPORT
#type	stop
#}
#
#route_number	28X
#}
#
#departure_stops	:3
#{
#{
#name	FORBES AVENUE AT MOREWOOD AVENUE  CARNEGIE MELL
#id	2418
#}
#{
#id	2417
#name	FORBES AVENUE AT MOREWOOD AVENUE  CARNEGIE MELL
#}
#{
#id	2442
#name	FORBES AVENUE OPPOSITE MOREWOOD  CARNEGIE MELLON
#}
#}
#
#arrival_stops	:2
#{
#{
#name	PITTSBURGH INTERNATIONAL AIRPORT LOWER LEVE
#id	5290
#}
#{
#id	3731
#name	LEBANON CHURCH ROAD AT COUNTY AIRPORT ENTRANCE
#}
#}
#
#result	{
#}
#
#}
#"
#}
#'''

#temp2Query = '''{c gal_be.launch_query
#:inframe "{
#query {
#type	2
#travel_time	{
#date	{
#month	12
#day	9
#year	2011
#weekday	5
#}
#
#period_spec	now
#time	{
#value	1421
#now	true
#type	departure
#}
#
#}
#departure_place	{
#name	CMU
#type	stop
#}
#
#arrival_place	{
#name	AIRPORT
#type	stop
#}
#
#route_number	28X
#}
#
#departure_stops :3
#{
#{
#id	2418
#name	FORBES AVENUE AT MOREWOOD AVENUE  CARNEGIE MELL
#}
#{
#id	2417
#name	FORBES AVENUE AT MOREWOOD AVENUE  CARNEGIE MELL
#}
#{
#id	2442
#name	FORBES AVENUE OPPOSITE MOREWOOD  CARNEGIE MELLON
#}
#}
#
#arrival_stops :2
#{
#{
#id	5290
#name	PITTSBURGH INTERNATIONAL AIRPORT LOWER LEVE
#}
#{
#id	3731
#name	LEBANON CHURCH ROAD AT COUNTY AIRPORT ENTRANCE
#}
#}
#
#result {
#}
#
#}
#"
#}
#'''

fullTimeSpec = 'travel_time\t{\n\
date\t{\n\
month\t${month}\n\
day\t${day}\n\
year\t${year}\n\
weekday\t${weekday}\n\
}\n\
\n\
period_spec\t${period_spec}\n\
time\t{\n\
value\t${value}\n\
now\t${now}\n\
type\t${time_type}\n\
}\n\
\n\
}\n\
'

briefTimeSpec = 'travel_time\t{\n\
period_spec\t${period_spec}\n\
time\t{\n\
now\t${now}\n\
type\t${time_type}\n\
}\n\
\n\
}\n\
'

veryBriefTimeSpec = 'travel_time\t{\n\
time\t{\n\
value\t${value}\n\
type\t${time_type}\n\
}\n\
\n\
}\n\
'

scheduleQuery = '{c gal_be.launch_query\n\
:inframe "{\n\
query {\n\
type\t${type}\n\
${time_spec}\n\
departure_place\t{\n\
name\t${departure_place_name}\n\
type\t${departure_place_type}\n\
}\n\
\n\
arrival_place\t{\n\
name\t${arrival_place_name}\n\
type\t${arrival_place_type}\n\
}\n\
\n\
${route_number}\
}\n\
\n\
${departure_stops}\n\
\n\
${arrival_stops}\n\
\n\
result\t{\n\
${result}\n\
}\n\
\n\
}\n\
"\n\
}'

def MakeScheduleQuery(querySpec,result=None,next=None):
	import logging
	appLogger = logging.getLogger('DialogThread')
	content = scheduleQuery
	
#	appLogger.info('Make query for schedule: %s',str(querySpec))
	appLogger.info('Make query for schedule')

	if 'day' in querySpec:
		timeSpec = fullTimeSpec
		timeSpec = timeSpec.replace('${month}',querySpec['month'])
		appLogger.info('1')
		timeSpec = timeSpec.replace('${day}',querySpec['day'])
		appLogger.info('2')
		timeSpec = timeSpec.replace('${year}',querySpec['year'])
		appLogger.info('3')
		timeSpec = timeSpec.replace('${weekday}',querySpec['weekday'])
		appLogger.info('4')
		timeSpec = timeSpec.replace('${period_spec}',querySpec['period_spec'])
		appLogger.info('5')
		timeSpec = timeSpec.replace('${now}',querySpec['now'])
		appLogger.info('7')
		timeSpec = timeSpec.replace('${value}',querySpec['value'])
		appLogger.info('6')
		timeSpec = timeSpec.replace('${time_type}',querySpec['time_type'])
		appLogger.info('8')
	elif 'now' in querySpec:
		timeSpec = briefTimeSpec
		timeSpec = timeSpec.replace('${period_spec}',querySpec['period_spec'])
		appLogger.info('9')
		timeSpec = timeSpec.replace('${now}',querySpec['now'])
		appLogger.info('10')
		timeSpec = timeSpec.replace('${time_type}',querySpec['time_type'])
		appLogger.info('11')
	else:
		timeSpec = veryBriefTimeSpec
		timeSpec = timeSpec.replace('${value}',querySpec['value'])
		appLogger.info('12')
		timeSpec = timeSpec.replace('${time_type}',querySpec['time_type'])
		appLogger.info('13')

	appLogger.info('next %s'%next)
	if not next: type = '2'
	elif next == 'NEXT BUS': type = '4'
	elif next == 'PREVIOUS BUS': type = '5' 
	else: appLogger.info('next %s'%next)

	content = content.replace('${type}',type)
	appLogger.info('0')
	content = content.replace('${time_spec}',timeSpec)
	appLogger.info('88')
	content = content.replace('${departure_place_name}',querySpec['departure_place'])
	appLogger.info('9')
	content = content.replace('${departure_place_type}',querySpec['departure_place_type'])
	appLogger.info('10')
	content = content.replace('${arrival_place_name}',querySpec['arrival_place'])
	appLogger.info('11')
	content = content.replace('${arrival_place_type}',querySpec['arrival_place_type'])
	appLogger.info('12')
	if querySpec['route'] != '':
		content = content.replace('${route_number}','route_number\t%s\n'%querySpec['route'])
	else:
		content = content.replace('${route_number}','')
	appLogger.info('13')
#	querySpec['departure_stops'] = \
	departure_stops = \
	'\n'.join([x.strip() for x in querySpec['departure_stops'].split('\n')[2:-3]]).replace('stops','departure_stops')
	content = content.replace('${departure_stops}',departure_stops)
#	content = content.replace('${departure_stops}',querySpec['departure_stops'])
	appLogger.info('14')
#	querySpec['arrival_stops'] = \
	arrival_stops = \
	'\n'.join([x.strip() for x in querySpec['arrival_stops'].split('\n')[2:-3]]).replace('stops','arrival_stops')
	content = content.replace('${arrival_stops}',arrival_stops)
#	content = content.replace('${arrival_stops}',querySpec['arrival_stops'])

	appLogger.info('15')

	if result:
		content = content.replace('${result}','\n'.join([x.strip() for x in result.split('\n')[2:-3]]))
	else:
		content = content.replace('${result}','')

	appLogger.info('%s'%content)
		
	appLogger.info('Done')
	
	message = {'type':'GALAXYCALL',
			   'content':content}
	return message

querySection = '\nquery\t{\n\
type\t${type}\n\
${time_spec}\n\
\n\
departure_place\t{\n\
name\t${departure_place_name}\n\
type\t${departure_place_type}\n\
}\n\
\n\
arrival_place\t{\n\
name\t${arrival_place_name}\n\
type\t${arrival_place_type}\n\
}\n\
\n\
${route_number}\
}\n'

def MakeScheduleSection(querySpec,result,next=None):
	import logging
	appLogger = logging.getLogger('DialogThread')
	query = querySection

	if not next: type = '2'
	elif next == 'NEXT BUS': type = '4'
	elif next == 'PREVIOUS BUS': type = '5' 
	query = query.replace('${type}',type)
	

	if 'day' in querySpec:
		timeSpec = fullTimeSpec
		timeSpec = timeSpec.replace('${month}',querySpec['month'])
		appLogger.info('1')
		timeSpec = timeSpec.replace('${day}',querySpec['day'])
		appLogger.info('2')
		timeSpec = timeSpec.replace('${year}',querySpec['year'])
		appLogger.info('3')
		timeSpec = timeSpec.replace('${weekday}',querySpec['weekday'])
		appLogger.info('4')
		timeSpec = timeSpec.replace('${period_spec}',querySpec['period_spec'])
		appLogger.info('5')
		timeSpec = timeSpec.replace('${now}',querySpec['now'])
		appLogger.info('7')
		timeSpec = timeSpec.replace('${value}',querySpec['value'])
		appLogger.info('6')
		timeSpec = timeSpec.replace('${time_type}',querySpec['time_type'])
		appLogger.info('8')
	elif 'now' in querySpec:
		timeSpec = briefTimeSpec
		timeSpec = timeSpec.replace('${period_spec}',querySpec['period_spec'])
		appLogger.info('9')
		timeSpec = timeSpec.replace('${now}',querySpec['now'])
		appLogger.info('10')
		timeSpec = timeSpec.replace('${time_type}',querySpec['time_type'])
		appLogger.info('11')
	else:
		timeSpec = veryBriefTimeSpec
		timeSpec = timeSpec.replace('${value}',querySpec['value'])
		appLogger.info('12')
		timeSpec = timeSpec.replace('${time_type}',querySpec['time_type'])
		appLogger.info('13')

	query = query.replace('${time_spec}',timeSpec)
#	appLogger.info('88')
#	query = query.replace('${month}',querySpec['month'])
#	query = query.replace('${day}',querySpec['day'])
#	query = query.replace('${year}',querySpec['year'])
#	query = query.replace('${weekday}',querySpec['weekday'])
#	query = query.replace('${period_spec}',querySpec['period_spec'])
#	query = query.replace('${value}',querySpec['value'])
#	query = query.replace('${now}',querySpec['now'])
#	query = query.replace('${time_type}',querySpec['time_type'])

	query = query.replace('${departure_place_name}',querySpec['departure_place'])
	query = query.replace('${departure_place_type}',querySpec['departure_place_type'])
	query = query.replace('${arrival_place_name}',querySpec['arrival_place'])
	query = query.replace('${arrival_place_type}',querySpec['arrival_place_type'])
	appLogger.info('8')
	if querySpec['route'] != '':
		query = query.replace('${route_number}','route_number\t%s\n'%querySpec['route'])
	else:
		query = query.replace('${route_number}','')
	appLogger.info('9')
	
	result = '\n'.join([x.strip() for x in result.split('\n')[1:-2]]).replace('new_result','result')
	appLogger.info('10')
	
	return query,'\n'+result+'\n'

#===============================================================================
# Parse date and time
#===============================================================================
parseDateTime = '{c datetime.ParseDateTime\n\
:Date_Time_Parse "{c parse :slots ${gal_slotsframe}}"}'

def MakeParseDateTimeMessage(galSlotsFrame):
	import logging
	appLogger = logging.getLogger('DialogThread')
	content = parseDateTime

	galSlotsFrame = galSlotsFrame.replace('"','\\"')	
	content = content.replace('${gal_slotsframe}',galSlotsFrame)

	message = {'type':'GALAXYCALL',
			   'content':content}
	return message
