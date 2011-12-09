#===============================================================================
# Dialog State
#===============================================================================
stateElementsDict = {'initial':{},'request_all':{},'request_departure_place':{},'request_arrival_place':{},'request_travel_time':{},\
					'request_next_query':{},'confirm_route':{},'confirm_departure_place':{},'confirm_arrival_place':{},'confirm_travel_time':{},\
					'inform_welcome':{},'inform_confirm_okay_route':{},'inform_confirm_okay_departure_place':{},'inform_confirm_okay_arrival_place':{},'inform_confirm_okay_travel_time':{},\
					'inform_processing':{},'inform_success':{},'inform_subsequent_processing':{},'inform_starting_new_query':{},'inform_uncovered_place':{}}

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

#===============================================================================
# Inform
#===============================================================================
stateElementsDict['inform_welcome']['DialogState'] = '/LetsGoPublic/GiveIntroduction/InformWelcome'
stateElementsDict['inform_welcome']['informWelcomeStack'] = '''/LetsGoPublic/GiveIntroduction/InformWelcome
  /LetsGoPublic/GiveIntroduction
  /LetsGoPublic'''
stateElementsDict['inform_welcome']['informWelcomeAgenda'] = '''0:
1:O[repeat]V
2:O[0_covered_route]S,O[0_discontinued_route]S,O[0_uncovered_route]S,O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,O[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,O[2_departureplace.stop_name.covered_place.covered_neighborhood]S,O[2_departureplace.stop_name.covered_place.monument]S,O[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,O[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,O[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,O[3_arrivalplace.stop_name.covered_place.monument]S,O[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,O[4_busafterthatrequest]S,X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,O[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_one]V,X[dtmf_three]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[finalquit]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[quit]V,O[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,X[startover]V,X[stop_name.monument]S,X[stop_name.registered_stop]S,O[turn_timeout:timeout]V,O[yes]V,X[yes]V'''
stateElementsDict['inform_welcome']['informWelcomeLineConfig'] = 'set_dtmf_len = 1, set_lm = first_query'

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


#===============================================================================
# Utterance
#===============================================================================
utterElementsDict = {'inform_welcome':{},'inform_how_to_get_help':{},'request_all':{},'request_departure_place':{},'request_arrival_place':{},'request_travel_time':{},\
'request_next_query':{},'confirm_route':{},'confirm_departure_place':{},'confirm_arrival_place':{},'confirm_travel_time':{},\
'inform_welcome':{},'inform_confirm_okay':{},'inform_processing':{},'inform_success':{},'inform_subsequent_processing':{},'inform_starting_new_query':{},'inform_uncovered_place':{}}

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
utterElementsDict['request_all']['Query'] = 'ExCount	0'
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
utterElementsDict['request_travel_time']['Agent'] = 'agent	/LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime/RequestTravelTime'
utterElementsDict['request_travel_time']['Version'] = ''
utterElementsDict['request_travel_time']['Option'] = ''

utterElementsDict['request_next_query']['DialogAct'] = 'request'
utterElementsDict['request_next_query']['FloorState'] = 'user'
utterElementsDict['request_next_query']['Object'] = 'next_query'
utterElementsDict['request_next_query']['Query'] = ''
utterElementsDict['request_next_query']['Result'] = ''
utterElementsDict['request_next_query']['Agent'] = ''
utterElementsDict['request_next_query']['Version'] = ''
utterElementsDict['request_next_query']['Option'] = '''   :non-repeatable "true"
'''

#===============================================================================
# Confirm 
#===============================================================================
utterElementsDict['confirm_route']['DialogAct'] = 'explicit_confirm'
utterElementsDict['confirm_route']['FloorState'] = 'user'
utterElementsDict['confirm_route']['Object'] = '/LetsGoPublic/query.route_number'
utterElementsDict['confirm_route']['Query'] = 'query.route_number	28X'
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
utterElementsDict['inform_success']['Option'] = ''

# inform_failure

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

##	appLogger.info('%s'%stateType)

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

def MakeSystemUtterance(utterType,stateType,turnNumber,notifyPrompts,dialogStateIndex,sessionID,idSuffix,uttCount):
	import logging
	appLogger = logging.getLogger('DialogThread')
	content = systemUtterance
	appLogger.info('%s'%utterType)
	if utterType.startswith('inform_confirm_okay'):
		utterType = 'inform_confirm_okay'
	elements = utterElementsDict[utterType]  
	
	content = content.replace('${dialog_act}',elements['DialogAct'])
#	appLogger.info('%s'%content)
	content = content.replace('${final_floor_status}',elements['FloorState'])
#	appLogger.info('%s'%content)
	content = content.replace('${object}',elements['Object'])
#	appLogger.info('%s'%content)
	content = content.replace('${query}',elements['Query'])
#	appLogger.info('%s'%content)
	content = content.replace('${result}',elements['Result'])
#	appLogger.info('%s'%content)
	content = content.replace('${agent}',elements['Agent'])
#	appLogger.info('%s'%content)
	content = content.replace('${version}',elements['Version'])
#	appLogger.info('%s'%content)
	content = content.replace('${option}',elements['Option'])
#	appLogger.info('%s'%content)
	content = content.replace('${dialog_state}',MakeDialogState(stateType,turnNumber,notifyPrompts))
#	appLogger.info('%s'%content)
	content = content.replace('${dialog_state_index}',str(dialogStateIndex))
#	appLogger.info('%s'%content)
	content = content.replace('${sess_id}',sessionID)
#	appLogger.info('%s'%content)
	content = content.replace('${id_suffix}','%03d'%idSuffix)
#	appLogger.info('%s'%content)
	content = content.replace('${utt_count}',str(uttCount))
#	appLogger.info('%s'%content)

	message = {'type':'GALAXYACTIONCALL',
			   'content':content}
	return message


#===============================================================================
# Backend Query Template
#===============================================================================
backendQuery = '''{c gal_be.launch_query 
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

