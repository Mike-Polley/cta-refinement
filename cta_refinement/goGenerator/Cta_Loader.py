#!/usr/bin/env python3

"""CTA Loader
Given a list of automata notations, loads them in the data structures defined in Automata_Structures.
"""

from Automata_Structures import *


# loads a string automata (multiple)
def load_automata(automata):
    automata_list = []

    for current_automata in automata:
        end_clause = seek_seq(current_automata, '=')

        automata_label = current_automata[4:end_clause - 1]

        # check for manual replacement of label
        # user_label = input('For the current automaton, the identified label is:\t\t ' + str(automata_label)
        #                    + '\n\t\tPress ENTER to accept this, or type a new label.\t')
        # if user_label != '':
        #     print('\tOverriding "' + str(automata_label) + '" with "' + str(automata_label) + '".')
        #     automata_label = user_label
        # else:
        #     print('\tUsing default label')

        end_clause = seek_seq(current_automata, ';')
        initial_state = current_automata[13:end_clause]
        state_list = []
        transition_dictionary = {}

        # find all transitions in this automata
        start_clause = end_clause + 1
        print('Parsing every transition in the current automaton:')
        transition_index = end_clause + seek_seq(current_automata[end_clause + 1:], ';') + 1
        while transition_index < len(current_automata):
            current_transition = current_automata[start_clause:transition_index + 1]
            print('\tCurrent transition: ' + str(current_transition))

            # transition consists of:
            # - start state
            # - send/recieve
            # - condition
            # - end state
            # check these are present
            if '!' not in current_transition and '?' not in current_transition:
                print('WARNING: Does not include send/receive of data.')
            if '(' and ')' not in current_transition:
                print('WARNING: Make sure to include a time constraint in (), following the send/receive of data.')

            start_clause = seek_seq(current_transition, ' ')
            current_transition_start_state = current_transition[:start_clause]
            start_clause += 1

            current_transition_communication_content = current_transition[
                                                       start_clause:seek_seq(current_transition, '(')]
            if '?' in current_transition_communication_content:
                current_transition_communication_type = 'receive'
            else:
                current_transition_communication_type = 'send'

            # patch communication content and split
            if current_transition_communication_type == 'receive':
                current_transition_communication_other = current_transition_communication_content[
                                                         :seek_seq(current_transition_communication_content, '?')]
            else:
                current_transition_communication_other = current_transition_communication_content[
                                                         :seek_seq(current_transition_communication_content, '!')]
            current_transition_communication_content = current_transition_communication_content[
                                                       (len(current_transition_communication_other) + 1):]

            start_clause = seek_seq(current_transition, '(') + 1

            current_transition_condition = current_transition[start_clause:seek_seq(current_transition, ')')]
            start_clause = seek_seq(current_transition, ')') + 2
            # check if there is a reset x
            if ',{x}' in current_transition_condition:
                print('\t\tThis transition resets this automatons clock')
                current_transition_reset_x = True
                current_transition_condition = current_transition_condition[:-4]
            else:
                print('\t\tNo clock reset')
                current_transition_reset_x = False

            current_transition_end_state = current_transition[start_clause:seek_seq(current_transition, ';')]

            # build data tuple
            current_transition = Transition(current_transition_start_state,
                                            current_transition_communication_type,
                                            current_transition_communication_content,
                                            current_transition_communication_other,
                                            current_transition_condition,
                                            current_transition_reset_x,
                                            current_transition_end_state)
            # add state to list
            if current_transition_start_state not in state_list:
                state_list.append(current_transition_start_state)
            # make sure end state is added to state list
            if current_transition_end_state not in state_list:
                state_list.append(current_transition_end_state)
            # update dictionary
            if current_transition_start_state not in transition_dictionary.keys():
                transition_dictionary[current_transition_start_state] = [current_transition]
            else:
                transition_dictionary[current_transition_start_state].append(current_transition)

            start_clause = transition_index + 1
            transition_index += seek_seq(current_automata[transition_index + 1:], ';') + 1

        print('Finished loading current automatons transitions, finishing up.')

        print('\tIdentifying end states:')
        end_states = []
        for state in state_list:
            if state not in transition_dictionary:
                # log(str(_state) + ' must be an end state, no outward transitions')
                end_states.append(state)
                print('\t\t' + str(state))

        automata_list.append(Automata(automata_label, initial_state, end_states, state_list, transition_dictionary, current_automata))

        print('Finished the current automaton.\n')

    print('Finished loading automata: ' + str(len(automata_list)) + '\n\n')

    return automata_list


# finds the first instance of character
def seek_seq(string, seq):
    # log('seeking end: ' + _string)
    index = 0
    while index < len(string) and string[index:index + len(seq)] != seq:
        index += 1
    return index
