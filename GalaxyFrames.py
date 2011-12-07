
initDialogState = '/LetsGoPublic'
initStack = '/LetsGoPublic'
initAgenda = '0:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_one]V,X[dtmf_three]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[finalquit]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[quit]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,X[startover]V,X[stop_name.monument]S,X[stop_name.registered_stop]S,O[turn_timeout:timeout]V,O[yes]V,X[yes]V'
initLineConfig = 'set_dtmf_len = 1, set_lm = first_query'

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

#${turn_number}${notify_prompts}${sess_id}${msg_idx}${object}${utt_count}
#nonu_threshold = 16676381918920442000.0000
introMessage = '''
{c main
    :action_level "high"
    :action_type "system_utterance"
    :properties {c properties
                   :dialog_act "inform"
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
act	inform
object	%s
_repeat_counter	0
system_version	1
}
end
"
   :non-listening "true"
   :non-repeatable "true"
   :utt_count "%d" }}'''

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
   
#${sess_id}${msg_idx}${object}${utt_count}
systemRequest = '''
{c main
    :action_level "high"
    :action_type "system_utterance"
    :properties {c properties
                   :dialog_act "request"
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
       :dialog_state_index "%s"
       :final_floor_status "user"
       :id "DialogManager-%s:%03d"
       :inframe "start
{
act	request
object	%s
_repeat_counter	0
%s
system_version	1
}
end
"
   :utt_count "%d" }}'''

#${sess_id}${msg_idx}${object}${utt_count}
systemConfirm = '''
{c main
    :action_level "high"
    :action_type "system_utterance"
    :properties {c properties
                   :dialog_act "explicit_confirm"
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
set_dtmf_len = 1, set_lm = yes_no
}"
       :dialog_state_index "%s"
       :final_floor_status "user"
       :id "DialogManager-%s:%03d"
       :inframe "start
{
act	explicit_confirm
object	/LetsGoPublic/query.departure_place
_repeat_counter	0
query.departure_place	{
%s
}
system_version	1
}
end
"
   :utt_count "%d" }}'''
   
#${sess_id}${msg_idx}${object}${utt_count}
systemConfirmOkay = '''
{c main
    :action_level "high"
    :action_type "system_utterance"
    :properties {c properties
                   :dialog_act "inform"
                   :dialog_state "turn_number = %s
notify_prompts = %s
dialog_state = /LetsGoPublic
nonu_threshold = 0.0000
stack = {
/LetsGoPublic
}
agenda = {
0:X[0_covered_route]S,X[0_discontinued_route]S,X[0_uncovered_route]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.ambiguous_covered_place]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.covered_neighborhood]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.monument]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.covered_place.registered_stop]S,X[1_singleplace.stop_name.uncovered_place]S,X[2_departureplace.stop_name.covered_place.ambiguous_covered_place]S,X[2_departureplace.stop_name.covered_place.covered_neighborhood]S,X[2_departureplace.stop_name.covered_place.monument]S,X[2_departureplace.stop_name.covered_place.registered_stop]S,X[2_departureplace.stop_name.uncovered_place]S,X[3_arrivalplace.stop_name.covered_place.ambiguous_covered_place]S,X[3_arrivalplace.stop_name.covered_place.covered_neighborhood]S,X[3_arrivalplace.stop_name.covered_place.monument]S,X[3_arrivalplace.stop_name.covered_place.registered_stop]S,X[3_arrivalplace.stop_name.uncovered_place]S,X[4_busafterthatrequest]S,X[4_busafterthatrequest]V,X[4_busbeforethatrequest]V,X[ambiguous_covered_place]S,X[anystop]V,X[covered_neighborhood]S,X[date_time]S,X[disambiguatearrival]V,X[disambiguatedeparture]V,X[dontknow]V,X[dtmf_one]V,X[dtmf_one]V,X[dtmf_three]V,X[dtmf_three]V,O[dtmf_zero]V,O[establishcontext]V,O[finalquit]V,O[help.general_help]V,O[help.give_me_tips]V,O[help.what_can_i_say]V,O[help.where_are_we]V,X[no]V,O[quit]V,O[repeat]V,X[repeat]V,O[session:session_timeout]V,O[session:terminatesession]V,O[startover]V,X[startover]V,X[stop_name.monument]S,X[stop_name.registered_stop]S,O[turn_timeout:timeout]V,O[yes]V,X[yes]V
}
input_line_config = {
set_dtmf_len = 1, set_lm = yes_no
}"
       :dialog_state_index "%s"
       :final_floor_status "free"
       :id "DialogManager-%s:%03d"
       :inframe "start
{
act	inform
object	confirm_okay
_repeat_counter	0
system_version	1
}
end
"
   :utt_count "%d" }}'''