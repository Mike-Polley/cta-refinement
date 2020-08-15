#!/usr/bin/env python3

"""Go code generator

This takes processed automata and its notation.
The processed automata is stored in a namedTuple structure denoted in Automata_Structures.

For each automaton in automata, it creates a function in Go. This is designed to be instantiated in a goroutine.
Along with a goroutine for each automaton, a main() method is generated to instantiate the goroutines and crudely setup the channels required for communication.

This can likely deal with all automata as it is designed to deal with communicating timed automata (CTA).

Methodology:
1. Goes through each automaton, generates basic wrappings. For this I decided to avoid the rabbit-hole of all the branching paths and emulate the process of an automaton objectively. I have a current state, and keep iterating through until I reach the end state. (An oversight is that I have not added functionality for multiple end states).
TODO: add multiple end states

2. In the main loop, whilst waiting to reach the end state, I check the outward transitions for the current state I am in. To avoid issues during runtime, I record the value of x (time), at the start of each iteration. This avoids ambiguity for the rare cases where x changes whilst between checking outward transitions.

3. Once an outward transition is possible, it goes about executing the transition. Any data/communications occur and the current state is updated for the next iteration. If there are multiple outward transitions, I check if they are all true. I do this incase there is any ambiguity and to avoid any bias to the generation of the transitions. If all are possible, I randomally choose which one to transition to.

4. This all keeps happening until the end state is reached, when it terminates.
"""


from Automata_Structures import *

# keep track of which channels go where and which type
# dictionary of automata returns list where it is used, some redundant data but is easier
channel_dictionary = {}
channel_directory = []


# returns a list of lines
def generate_go_lang(automata):
    global channel_dictionary
    global channel_directory

    # head of go file
    file_head = 'package main\n\n' \
                'import (\n' \
                '\t"time"\n' \
                '\t"fmt"\n)\n\n/* for the automata:'

    clocks = []
    notifiers = []
    automata_param = []

    goroutines = []
    # generate each function
    for a in automata:
        print('Generating: ' + a.label)

        file_head += a.text


        clock_name = a.label + '_clock'
        notifier_name = a.label + '_fin'

        # global vars
        clocks.append(clock_name)
        notifiers.append(notifier_name)

        # set up automata
        initial_state = a.initial_state
        end_states = a.end_states
        state_list = a.state_list
        transition_dictionary = a.transition_dictionary

        # channel names
        channels = []

        goroutine = '\t'*1 + '// initial state\n' + \
                    '\t'*1 + 'current_state := "' + initial_state + '"\n' + \
                    '\t'*1 + '// set up clock\n' + \
                    '\t'*1 + 'x := ' + clock_name + '\n' + \
                    '\t'*1 + 'fmt.Printf("automata_' + a.label + ': %s: %v: Starting...\\n", current_state, x)\n' + \
                    '\t'*1 + '// repeat until end state reached\n' + \
                    '\t'*1 + 'for {\n' + \
                    '\t'*2 + '// update clock\n' + \
                    '\t'*2 + 'if x != ' + clock_name + ' {\n' + \
                    '\t'*3 + 'x = ' + clock_name + '\n' + \
                    '\t'*3 + 'switch current_state {\n'

        for state in state_list:
            # if state isnt end state
            if state in transition_dictionary:
                goroutine += '\t'*3 + 'case "' + str(state) + '":\n'
                # for each transition
                for transition in transition_dictionary[state]:
                    goroutine += '\t'*4 + 'if ' + transition.condition + ' {\n'
                    current_channel = str(channel_communication(a.label, transition))
                    channels.append(current_channel)
                    # if send
                    if transition.communication_sr == 'send':
                        # write transition code
                        goroutine += '\t'*5 + 'fmt.Printf("automata_' + a.label + ': %s: %v: Checking ' + state + '.\\n", current_state, x)\n' + \
                                     '\t'*5 + '// send\n' + \
                                     '\t'*5 + current_channel + ' <- "' + transition.communication_datatype + '"\n' + \
                                     '\t'*5 + '// next state\n' + \
                                     '\t'*5 + 'current_state = "' + transition.end_state + '"\n'

                        # check if reset x
                        if transition.reset_x:
                            goroutine += '\t'*5 + '// reset x\n' + \
                                         '\t'*5 + clock_name + ' = 0\n'

                        goroutine += '\t'*5 + 'fmt.Printf("automata_' + a.label + ': %s: %v: Left ' + state + '.\\n", current_state, x)\n' + \
                                     '\t'*5 + 'continue\n' + \
                                     '\t'*4 + '}\n'

                    elif transition.communication_sr == 'receive':
                        # write transition code
                        goroutine += '\t'*6 + 'fmt.Printf("automata_' + a.label + ': %s: %v: Checking ' + state + '.\\n", current_state, x)\n' + \
                                     '\t'*6 + '// check if receive is available\n' + \
                                     '\t'*6 + 'select {\n' + \
                                     '\t'*6 + 'case receive, ok := <-' + current_channel + ':\n' + \
                                     '\t'*7 + 'if ok {\n' + \
                                     '\t'*8 + '// received\n' + \
                                     '\t'*8 + '_ = receive\n' + \
                                     '\t'*8 + '// next state\n' + \
                                     '\t'*8 + 'current_state = "' + transition.end_state + '"\n'

                        # check if reset x
                        if transition.reset_x:
                            goroutine += '\t'*8 + '// reset x\n' + \
                                         '\t'*8 + clock_name + ' = 0\n'

                        goroutine += '\n' + '\t'*8 + 'fmt.Printf("automata_' + a.label + ': %s: %v: Left ' + state + '.\\n", current_state, x)\n' + \
                                     '\t'*8 + 'continue\n' + \
                                     '\t'*7 + '} else {\n' + \
                                     '\t'*8 + '// channel closed\n' + \
                                     '\t'*8 + 'fmt.Printf("automata_' + a.label + ': %s: %v: ERROR: channel not open.\\n", current_state, x)\n' + \
                                     '\t'*7 + '}\n' + \
                                     '\t'*6 + 'default:\n' + \
                                     '\t'*7 + '// nothing in channel\n' + \
                                     '\t'*7 + 'fmt.Printf("automata_' + a.label + ': %s: %v: Waiting to receive.\\n", current_state, x)\n' + \
                                     '\t'*6 + '}\n' + \
                                     '\t'*4 + '}\n'
                    else:
                        print("ERROR, transition not sent or receive.")

        # set up end condition
        goroutine += '\t'*3 + '}\n' + \
                     '\t'*3 + '// check if end state has been reached\n' + \
                     '\t'*3 + 'if '
        for end in end_states:
            goroutine += 'current_state == "' + str(end) + '" || '
        goroutine = goroutine[0:-3] + '{\n' + \
                                      '\t'*4 + 'fmt.Printf("automata_' + a.label + ': %s: %v: End state Reached.\\n", current_state, x)\n' + \
                                      '\t'*4 + notifier_name + ' = true\n' + \
                                      '\t'*4 + 'break\n' + \
                                      '\t'*3 + '}\n' + \
                                      '\t'*2 + '}\n' + \
                                      '\t'*1 + '}\n'

        # set up func header (with channel names)
        function_header = 'automata_' + a.label + '('
        a_param = 'automata_' + a.label + '('
        for chan in channels:
            function_header += chan + ' chan string, '
            a_param += chan + ', '
        function_header = function_header[0:-2] + ') {\n'
        automata_param.append(a_param[0:-2] + ')')

        function_header = '// ' + a.text + '\nfunc ' + function_header
        goroutines.append(function_header + goroutine)

    main_function = 'func main() {\n' + \
                    '\t'*1 + '// set up channels\n'
    for chan in channel_directory:
        transition = channel_dictionary[chan]
        main_function += '\t'*1 + chan + ' := make(chan string, 2)\n'
    main_function += '\n'

    main_function += '\t'*1 + '// run goroutines\n'
    for go in automata_param:
        main_function += '\tgo ' + go + '\n'
    main_function += '\n'

    main_function += '\t'*1 + '// run clocks\n' + \
                     '\t'*1 + 'for {\n' + \
                     '\t'*2 + 'time.Sleep(time.Second * clock_speed)\n' + \
                     '\t'*2 + '//increment clocks\n'
    for clock in clocks:
        main_function += '\t'*2 + clock + ' += clock_increment\n'
    main_function += '\t'*2 + '// check if goroutines have ended\n' + \
                     '\t'*2 + 'if '
    for notifier in notifiers:
        main_function += notifier + ' && '
    main_function = main_function[0:-3] + '{\n' + \
                     '\t'*3 + 'break\n' + \
                     '\t'*2 + '}\n' + \
                     '\t'*1 + '}\n\n' + \
                     '\t'*1 + 'fmt.Println("CTA finished running.")\n' + \
                     '\t'*0 + '}\n'

    # build entire program
    program = file_head + '\n*/\n\n' \
                     '// speed of system\n' \
                     'const clock_speed = 1\n' \
                     'const clock_increment = 1\n\n' \
                     '// set up clocks\n'
    for clock in clocks:
        program += 'var ' + clock + ' int = 0\n'

    program += '\n// set up notifiers\n'
    for notifier in notifiers:
        program += 'var ' + notifier + ' bool = false\n'
    program += '\n'

    # add main and functions
    program += main_function + '\n'
    for goroutine in goroutines:
        program += goroutine + '}\n\n'

    print('Finished generating program.\n\n')
    return program


# helper function for setting up channels
# returns the code needed to implement the communication
def channel_communication(automata, transition):
    global channel_dictionary
    global channel_directory
    # details
    transition_sr = transition.communication_sr
    transition_datatype = transition.communication_datatype
    transition_other = transition.communication_other

    proposed_channel_name = 'channel_'# + automata + '_' + transition_end + '_' + transition_datatype

    if transition_sr == 'send':
        proposed_channel_name += automata.upper() + '_' + transition_other.upper() + '_' + transition_datatype
    else:
        proposed_channel_name += transition_other.upper() + '_' + automata.upper() + '_' + transition_datatype

    if proposed_channel_name not in channel_directory:
        channel_directory.append(proposed_channel_name)

    channel_dictionary[proposed_channel_name] = transition

    return proposed_channel_name
