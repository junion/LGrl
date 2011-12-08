

introDialogAct = 'inform'
introDialogState = '/LetsGoPublic'
introStack = '/LetsGoPublic'
introAgenda = '0:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_one]V,X[dtmf_three]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[finalquit]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[quit]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,X[startover]V,X[stop_name.monument]S,X[stop_name.registered_stop]S,O[turn_timeout:timeout]V,O[yes]V,X[yes]V'
introLineConfig = 'set_dtmf_len = 1, set_lm = first_query'
introFirstFloorState = 'system'
introSecondFloorState = 'free'
introFirstObject = 'welcome'
introSecondObject = 'how_to_get_help'
introContent = ''
introFirstOption = '''   :non-listening "true"
   :non-repeatable "true"
'''



#===============================================================================
# 
#===============================================================================
requestDialogAct = 'request'

requestAllDialogState = '/LetsGoPublic/GiveIntroduction/InformWelcome'
requestAllStack = '''/LetsGoPublic/GiveIntroduction/InformWelcome
  /LetsGoPublic/GiveIntroduction
  /LetsGoPublic'''
requestAllAgenda = '''0:
1:O[repeat]V
2:O[0_covered_route]S,O[0_discontinued_route]S,O[0_uncovered_route]S,O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,O[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,O[2_departureplace.stop_name.covered_place.covered_neighborhood]S,O[2_departureplace.stop_name.covered_place.monument]S,O[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,O[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,O[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,O[3_arrivalplace.stop_name.covered_place.monument]S,O[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,O[4_busafterthatrequest]S,X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,O[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_one]V,X[dtmf_three]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[finalquit]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[quit]V,O[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,X[startover]V,X[stop_name.monument]S,X[stop_name.registered_stop]S,O[turn_timeout:timeout]V,O[yes]V,X[yes]V'''

requestDeparturePlaceDialogState = ''
requestDeparturePlaceStack = ''
requestDeparturePlaceAgenda = ''

requestArrivalPlaceDialogState = '/LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace/RequestArrivalPlace'
requestArrivalPlaceStack = '''/LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace/RequestArrivalPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
requestArrivalPlaceAgenda = '''0:O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,O[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,O[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,O[3_arrivalplace.stop_name.covered_place.monument]S,O[3_arrivalplace.stop_name.covered_place.registered_stop]S
1:X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dtmf_one]V,X[dtmf_three]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,O[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,O[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[dontknow]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
4:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''

requestTravelTimeDialogState = '/LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime/RequestTravelTime'
requestTravelTimeStack = '''/LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime/RequestTravelTime
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
requestTravelTimeAgenda = '''0:O[4_busafterthatrequest]S,O[date_time]S
1:X[4_busafterthatrequest]S,X[date_time]S
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
4:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''

requestNextQueryDialogState = '/LetsGoPublic/PerformTask/GiveResults/RequestNextQuery'
requestNextQueryStack = '''/LetsGoPublic/PerformTask/GiveResults/RequestNextQuery
  /LetsGoPublic/PerformTask/GiveResults
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
requestNextQueryAgenda = '''0:O[4_busafterthatrequest]V,O[4_busbeforethatrequest]V,O[startover]V
1:O[finalquit]V,O[quit]V,O[repeat]V,X[startover]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''

requestAllLineConfig = 'set_dtmf_len = 1, set_lm = first_query'
requestPlaceLineConfig = 'set_dtmf_len = 1, set_lm = place'
requestTravelTimeLineConfig = 'set_dtmf_len = 1, set_lm = time'
requestNextQueryLineConfig = 'set_dtmf_len = 1, set_lm = next_query'

requestFloorState = 'user'

requestAllObject = 'how_may_i_help_you_directed'
requestDeparturePlaceObject = ''
requestArrivalPlaceObject = 'query.arrival_place'
requestTravelTimeObject = 'query.travel_time'
requestNextQueryObject = 'next_query'

requestAllQuery = 'ExCount	0'
requestDeparturePlaceQuery = ''
requestArrivalPlaceQuery = '''query	{
departure_place	{
name	DOWNTOWN
type	neighborhood
}
'''
requestTravelTimeQuery = '''query	{
departure_place	{
name	DOWNTOWN
type	neighborhood
}
'''
requestNextQueryQuery = ''

requestResult = ''
requestAllResult = ''
requestDeparturePlaceResult = ''
requestArrivalPlaceResult = ''
requestTravelTimeResult = ''
requestNextQueryResult = ''

requestAgent = ''
requestTravelTimeAgent = 'agent	/LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime/RequestTravelTime'

requestVersion = ''

requestOption = ''
requestNextQueryOption = '''   :non-repeatable "true"
'''



#===============================================================================
# 
#===============================================================================
confirDialogAct = 'explicit_confirm'

confirmDeparturePlaceDialogState = '/_ExplicitConfirm[/LetsGoPublic/query.departure_place]/RequestConfirm'
confirmDeparturePlaceStack = '''/_ExplicitConfirm[/LetsGoPublic/query.departure_place]/RequestConfirm
  /_ExplicitConfirm[/LetsGoPublic/query.departure_place]
  /LetsGoPublic/PerformTask/GetQuerySpecs/AskHowMayIHelpYou
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
confirmDeparturePlaceAgenda = '''0:O[dtmf_one]V,O[dtmf_three]V,O[no]V,O[yes]V
1:
2:
3:O[0_covered_route]S,X[0_covered_route]S,O[0_discontinued_route]S,X[0_discontinued_route]S,O[0_uncovered_route]S,X[0_uncovered_route]S,O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,O[1_singleplace.stop_name.uncovered_place]S,O[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,O[2_departureplace.stop_name.covered_place.covered_neighborhood]S,O[2_departureplace.stop_name.covered_place.monument]S,O[2_departureplace.stop_name.covered_place.registered_stop]S,O[2_departureplace.stop_name.uncovered_place]S,O[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,O[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,O[3_arrivalplace.stop_name.covered_place.monument]S,O[3_arrivalplace.stop_name.covered_place.registered_stop]S,O[3_arrivalplace.stop_name.uncovered_place]S,O[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,O[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
4:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
5:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''

confirmArrivalPlaceDialogState = '/_ExplicitConfirm[/LetsGoPublic/query.arrival_place]/RequestConfirm'
confirmArrivalPlaceStack = '''/_ExplicitConfirm[/LetsGoPublic/query.arrival_place]/RequestConfirm
  /_ExplicitConfirm[/LetsGoPublic/query.arrival_place]
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace/RequestArrivalPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
confirmArrivalPlaceAgenda = '''0:O[dtmf_one]V,O[dtmf_three]V,O[no]V,O[yes]V
1:
2:O[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,O[1_singleplace.stop_name.covered_place.covered_neighborhood]S,O[1_singleplace.stop_name.covered_place.monument]S,O[1_singleplace.stop_name.covered_place.registered_stop]S,O[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,O[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,O[3_arrivalplace.stop_name.covered_place.monument]S,O[3_arrivalplace.stop_name.covered_place.registered_stop]S
3:X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dtmf_one]V,X[dtmf_three]V
4:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,O[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,O[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[dontknow]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
5:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
6:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''

confirmTravelTimeDialogState = '/_ExplicitConfirm[/LetsGoPublic/query.travel_time.time]/RequestConfirm'
confirmTravelTimeStack = '''/_ExplicitConfirm[/LetsGoPublic/query.travel_time.time]/RequestConfirm
  /_ExplicitConfirm[/LetsGoPublic/query.travel_time.time]
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime/RequestTravelTime
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetTravelTime
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
confirmTravelTimeAgenda = '''0:O[dtmf_one]V,O[dtmf_three]V,O[no]V,O[yes]V
1:
2:O[4_busafterthatrequest]S,O[date_time]S
3:X[4_busafterthatrequest]S,X[date_time]S
4:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
5:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
6:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''

confirmLineConfig = 'set_dtmf_len = 1, set_lm = yes_no'

confirmFloorState = 'user'

confirmObject = ''
confirmDeparturePlaceObject = '/LetsGoPublic/query.departure_place'
confirmArrivalPlaceObject = '/LetsGoPublic/query.arrival_place'
confirmTravelTimeObject = '/LetsGoPublic/query.travel_time.time'

confirmQuery = ''
confirmDeparturePlaceQuery = '''query.departure_place	{
%s
}'''
confirmArrivalPlaceQuery = '''query.arrival_place	{
%s
}'''
confirmTravelTimeQuery = '''query.arrival_place	{
%s
}'''

confirmResult = ''

confirmAgent = ''

confirmVersion = ''

confirmOption = ''



#===============================================================================
# 
#===============================================================================
confirmOkayDialogAct = 'inform'   

confirmOkayDeparturePlaceDialogState = '/_ExplicitConfirm[/LetsGoPublic/query.arrival_place]/AcknowledgeConfirm'
confirmOkayDeparturePlaceStack = '''/_ExplicitConfirm[/LetsGoPublic/query.arrival_place]/AcknowledgeConfirm
  /_ExplicitConfirm[/LetsGoPublic/query.arrival_place]
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
confirmOkayDeparturePlaceAgenda = '''0:
1:X[dtmf_one]V,X[dtmf_three]V,X[no]V,X[yes]V
2:X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dtmf_one]V,X[dtmf_three]V
3:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[dontknow]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
4:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
5:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''

confirmOkayArrivalPlaceDialogState = '/_ExplicitConfirm[/LetsGoPublic/query.arrival_place]/AcknowledgeConfirm'
confirmOkayArrivalPlaceStack = '''/_ExplicitConfirm[/LetsGoPublic/query.arrival_place]/AcknowledgeConfirm
  /_ExplicitConfirm[/LetsGoPublic/query.arrival_place]
  /LetsGoPublic/PerformTask/GetQuerySpecs/GetArrivalPlace
  /LetsGoPublic/PerformTask/GetQuerySpecs
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
confirmOkayArrivalPlaceAgenda = '''0:
1:X[dtmf_one]V,X[dtmf_three]V,X[no]V,X[yes]V
2:X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dtmf_one]V,X[dtmf_three]V
3:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[dontknow]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
4:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[finalquit]V,X[quit]V,X[repeat]V,X[startover]V
5:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''

confirmOkayLineConfig = ''

confirmOkayFloorState = 'free'

confirmOkayObject = 'confirm_okay'

confirmOkayAgent = ''

confirmOkayVersion = ''

confirmOkayQuery = ''

confirmOkayResult = ''

confirmOkayOption = ''




#===============================================================================
# 
#===============================================================================
informDialogAct = 'inform'

informProcessingDialogState = '/LetsGoPublic/PerformTask/ProcessQuery/InformFirstProcessing'
informProcessingStack = '''/LetsGoPublic/PerformTask/ProcessQuery/InformFirstProcessing
  /LetsGoPublic/PerformTask/ProcessQuery
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
informProcessingAgenda = '''0:
1:
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,O[finalquit]V,O[quit]V,O[repeat]V,X[startover]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''

informSuccessDialogState = '/LetsGoPublic/PerformTask/GiveResults/InformSuccess'
informSuccessStack = '''/LetsGoPublic/PerformTask/GiveResults/InformSuccess
  /LetsGoPublic/PerformTask/GiveResults
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
informSuccessAgenda = '''0:
1:O[4_busafterthatrequest]V,O[4_busbeforethatrequest]V,O[finalquit]V,O[quit]V,O[repeat]V,O[startover]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''

informSubsequentProcessingDialogState = '/LetsGoPublic/PerformTask/ProcessQuery/InformSubsequentProcessing'
informSubsequentProcessingStack = '''/LetsGoPublic/PerformTask/ProcessQuery/InformSubsequentProcessing
  /LetsGoPublic/PerformTask/ProcessQuery
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
informSubsequentProcessingAgenda = '''0:
1:
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,O[finalquit]V,O[quit]V,O[repeat]V,X[startover]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''

informStartingNewQueryDialogState = '/LetsGoPublic/PerformTask/GiveResults/InformStartingNewQuery'
informStartingNewQueryStack = '''/LetsGoPublic/PerformTask/GiveResults/InformStartingNewQuery
  /LetsGoPublic/PerformTask/GiveResults
  /LetsGoPublic/PerformTask
  /LetsGoPublic'''
informStartingNewQueryAgenda = '''0:
1:X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,O[finalquit]V,O[quit]V,O[repeat]V,X[startover]V
2:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_three]V,X[stop_name.monument]S,X[stop_name.registered_stop]S
3:X[dtmf_one]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,O[turn_timeout:timeout]V,X[turn_timeout:timeout]V,X[yes]V,X[yes]V'''

informProcessingLineConfig = 'set_dtmf_len = 1, set_lm = first_query'
informSuccessLineConfig = 'set_dtmf_len = 0, set_lm = next_query'
informSubsequentProcessingLineConfig = 'set_dtmf_len = 1, set_lm = first_query'
informStartingNewQueryLineConfig = 'set_dtmf_len = 0, set_lm = next_query'

informProcessingFloorState = 'free'
informSuccessFloorState = 'system'
informSubsequentProcessingFloorState = 'free'
informStartingNewQueryFloorState = 'free'

informProcessingObject = 'looking_up_database_first'
informSuccessObject = 'result'
informSubsequentProcessingObject = 'looking_up_database_subsequent'
informStartingNewQueryObject = 'starting_new_query'

informAgent = ''

informVersion = ''

informQuery = ''

informResult = ''

informOption = ''




#===============================================================================
# 
#===============================================================================
systemUtterance = '''
{c main
    :action_level "high"
    :action_type "system_utterance"
    :properties {c properties
                   :dialog_act "%s"
                   :dialog_state "turn_number = %s
notify_prompts = %s
dialog_state = %s
nonu_threshold = 0.0000
stack = {
%s
}
agenda = {
%s
}
input_line_config = {
%s
}"
       :dialog_state_index "%d"
       :final_floor_status "%s"
       :id "DialogManager-%s:%03d"
       :inframe "start
{
act	%s
object	%s
_repeat_counter	0
%s%s%s%ssystem_version	1
}
end
"
%s   :utt_count "%d" }}'''

dialogStateMessage = '''
{c main
    :event_level "high"
    :event_type "dialog_state_change"
    :properties {c properties
                   :dialog_state "turn_number = %s
notify_prompts = %s
dialog_state = %s
nonu_threshold = 0.0000
stack = {
%s
}
agenda = {
%s
}
input_line_config = {
%s
}"
}}'''


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

