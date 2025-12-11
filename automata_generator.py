from Automata import Automata
from Transitions import Transitions

stack_vars = [f"Z{i:04d}" for i in range(1000)]

def stack_vars_reset():
    global stack_vars
    stack_vars = [f"Z{i:04d}" for i in range(1000)]

def base(a):
    alphabet=[]
    states=[]
    transitions=[]
    start_states=0
    final_states=[]
    stack_symbols=[]

    alphabet.append(a)
    states.append(0)
    states.append(1)
    transitions.append(Transitions(0,a,"&",1,"&"))
    final_states.append(1)

    return Automata(alphabet,states,transitions,start_states,final_states,stack_symbols)

def concatenation(automata1,automata2):
    alphabet=[]
    states=[]
    transitions=[]
    start_states=0
    final_states=[]
    stack_symbols=[]

    for item in automata1.alphabet:
        alphabet.append(item)
    for item in automata2.alphabet:
        flag=1
        for aux in automata1.alphabet:
            if item==aux:
                flag=0
                break
        if flag==1:   
            alphabet.append(item)
    flag=1
    for aux in alphabet:
        if item=="&":
            flag=0
            break
    if flag==1:
        alphabet.append("&")

    for i in range(len(automata1.states)+len(automata2.states)):
        states.append(i)    

    for item in automata1.transitions:
        transitions.append(Transitions(item.get_arg(1),item.get_arg(2),item.get_arg(3),item.get_arg(4),item.get_arg(5)))
    transitions.append(Transitions(len(automata1.states)-1,"&","&",len(automata1.states),"&"))
    for item in automata2.transitions:
        transitions.append(Transitions(item.get_arg(1)+len(automata1.states),item.get_arg(2),item.get_arg(3),item.get_arg(4)+len(automata1.states),item.get_arg(5)))
    
    final_states.append(len(states)-1)

    for item in automata1.stack_symbols:
        stack_symbols.append(item)
    for item in automata2.stack_symbols:
        stack_symbols.append(item)

    return Automata(alphabet,states,transitions,start_states,final_states,stack_symbols)

def union(automata1,automata2):
    alphabet=[]
    states=[]
    transitions=[]
    start_states=0
    final_states=[]
    stack_symbols=[]
    for item in automata1.alphabet:
        alphabet.append(item)
    for item in automata2.alphabet:
        flag=1
        for aux in automata1.alphabet:
            if item==aux:
                flag=0
                break
        if flag==1:   
            alphabet.append(item)
    flag=1
    for aux in alphabet:
        if item=="&":
            flag=0
            break
    if flag==1:
        alphabet.append("&")

    for i in range(len(automata1.states)+len(automata2.states)+2):
        states.append(i)    

    transitions.append(Transitions(0,"&","&",1,"&"))
    transitions.append(Transitions(0,"&","&",len(automata1.states)+1,"&"))
    for item in automata1.transitions:
        transitions.append(Transitions(item.get_arg(1)+1,item.get_arg(2),item.get_arg(3),item.get_arg(4)+1,item.get_arg(5)))
    for item in automata2.transitions:
        transitions.append(Transitions(item.get_arg(1)+len(automata1.states)+1,item.get_arg(2),item.get_arg(3),item.get_arg(4)+len(automata1.states)+1,item.get_arg(5)))
    transitions.append(Transitions(len(automata1.states),"&","&",len(automata1.states)+len(automata2.states)+1,"&"))
    transitions.append(Transitions(len(automata1.states)+len(automata2.states),"&","&",len(automata1.states)+len(automata2.states)+1,"&"))

    final_states.append(len(automata1.states)+len(automata2.states)+1)

    for item in automata1.stack_symbols:
        stack_symbols.append(item)
    for item in automata2.stack_symbols:
        stack_symbols.append(item)

    return Automata(alphabet,states,transitions,start_states,final_states,stack_symbols)

def kleene_star(automata1):
    alphabet=[]
    states=[]
    transitions=[]
    start_states=0
    final_states=[]
    stack_symbols=[]
    
    for item in automata1.alphabet:
        alphabet.append(item)
    flag=1
    for aux in alphabet:
        if aux=="&":
            flag=0
            break
    if flag==1:
        alphabet.append("&")

    states.append(0)
    for i in range(len(automata1.states)+1):
        states.append(i+1)    
    i=len(states)-1

    transitions.append(Transitions(0,"&","&",1,"&"))
    transitions.append(Transitions(0,"&","&",i,"&"))
    transitions.append(Transitions(i-1,"&","&",1,"&"))
    transitions.append(Transitions(i-1,"&","&",i,"&"))

    for item in automata1.transitions:
        transitions.append(Transitions(item.get_arg(1)+1,item.get_arg(2),item.get_arg(3),item.get_arg(4)+1,item.get_arg(5)))

    final_states.append(i)
    
    for item in automata1.stack_symbols:
        stack_symbols.append(item)

    return Automata(alphabet,states,transitions,start_states,final_states,stack_symbols)

def sharp(automata1, automata2, origin=None):
    alphabet=[]
    states=[0, ]
    transitions=[]
    start_states=0
    final_states=[]
    stack_symbols=[]
    if automata1.tag!="sharp" and automata2.tag!="sharp":
        for state in automata1.states:
            states.append(state+1)
            if state == automata1.start_states:
                transitions.append(Transitions(0, '&', '&', state+1, '&'))
            else:
                continue
        
        num = len(states)
        for state in automata2.states:
            if state == automata1.start_states:
                states.append(state+num)
                transitions.append(Transitions(0, '&', '&', state+num, '&'))
            else:
                states.append(state+num)
                continue
        
        for transition in automata1.transitions:
            transitions.append(Transitions(transition.get_arg(1)+1, transition.get_arg(2), transition.get_arg(3), transition.get_arg(4)+1, transition.get_arg(5)))

        for transition in automata2.transitions:
            transitions.append(Transitions(transition.get_arg(1)+num, transition.get_arg(2), transition.get_arg(3), transition.get_arg(4)+num, transition.get_arg(5)))
        
        states.append(len(states))
        
        auxVar = stack_vars.pop()
        for state in automata1.final_states:
            transitions.append(Transitions(state+1, '&', '&', len(states)-1, auxVar))
        stack_symbols.append(auxVar)
        
        temp = auxVar
        auxVar = stack_vars.pop()
        for state in automata2.final_states:
            transitions.append(Transitions(state+num, '&', '&', len(states)-1, auxVar))
        transitions.append(Transitions(len(states)-1, '&', (temp+'#'+auxVar), len(states)-1, '#'))
        transitions.append(Transitions(len(states)-1, '&', '&', 0, '&'))
        stack_symbols.append(auxVar)

        final_states.append(len(states)-1)

        for aux in automata1.stack_symbols:
            stack_symbols.append(aux)
        
        for aux in automata2.stack_symbols:
            if aux not in stack_symbols:
                stack_symbols.append(aux)
        
        for item in automata1.alphabet:
            alphabet.append(item)
        for item in automata2.alphabet:
            if item not in alphabet:
                alphabet.append(item)
        
        if "&" not in alphabet:
            alphabet.append("&")
    else:
        automata_sharp = automata1
        automata_normal = automata2

        if automata2.tag == "sharp":
            automata_sharp = automata2
            automata_normal = automata1
        

        if automata_normal.tag != "sharp":
            num = len(automata_sharp.states)
            for state in automata_normal.states:
                automata_sharp.states.append(state+num)
                if state == automata_normal.start_states:
                    automata_sharp.transitions.append(Transitions(automata_sharp.start_states,'&','&',state+num,'&'))
                if state in automata_normal.final_states:
                    auxVar = '#'
                    if origin==None:
                        auxVar = stack_vars.pop()
                        for transitions in automata_sharp.transitions:
                            if transitions.get_arg(1)==automata_sharp.final_states[0] and transitions.get_arg(2)=='&' and transitions.get_arg(3)!='&' and transitions.get_arg(4)==automata_sharp.final_states[0] and transitions.get_arg(5)=='#':
                                transitions.set_transition(automata_sharp.final_states[0],'&', (auxVar+'#'+transitions.get_arg(3)),automata_sharp.final_states[0],'#')
                        automata_sharp.stack_symbols.append(auxVar)
                        
                    automata_sharp.transitions.append(Transitions(state+num,'&','&',automata_sharp.final_states[0],auxVar))

            for item in automata_normal.transitions:
                automata_sharp.transitions.append(Transitions(item.get_arg(1)+num,item.get_arg(2),item.get_arg(3),item.get_arg(4)+num,item.get_arg(5)))
            
            for item in automata_normal.alphabet:
                if item not in automata_sharp.alphabet:
                    automata_sharp.alphabet.append(item)
            
            for item in automata_normal.stack_symbols:
                if item not in automata_sharp.stack_symbols:
                    automata_sharp.stack_symbols.append(item)

            alphabet = automata_sharp.alphabet
            states = automata_sharp.states
            transitions = automata_sharp.transitions
            start_states = automata_sharp.start_states
            final_states = automata_sharp.final_states
            stack_symbols = automata_sharp.stack_symbols
        else:
            if len(automata_sharp.states) < len(automata_normal.states):
                aux = automata_normal
                automata_normal = automata_sharp
                automata_sharp = aux
            num = len(automata_sharp.states)
            for state in automata_normal.states:
                if (state != automata_normal.start_states and state not in automata_normal.final_states):
                    automata_sharp.states.append(state + num - 1)
            for item in automata_normal.transitions:
                origem = item.get_arg(1)
                simbolo = item.get_arg(2)
                pop = item.get_arg(3)
                destino = item.get_arg(4)
                push = item.get_arg(5)

                origem_eh_ini = origem == automata_normal.start_states
                destino_eh_ini = destino == automata_normal.start_states

                origem_eh_final = origem in automata_normal.final_states
                destino_eh_final = destino in automata_normal.final_states

                origem_interna = (not origem_eh_ini) and (not origem_eh_final)
                destino_interno = (not destino_eh_ini) and (not destino_eh_final)

                if origem_interna and destino_interno:
                    automata_sharp.transitions.append(Transitions(origem + num -1, simbolo, pop, destino + num -1, push))

                elif origem_eh_ini and destino_interno:
                    automata_sharp.transitions.append(Transitions(automata_sharp.start_states, simbolo, pop, destino + num-1, push))

                elif origem_eh_ini and destino_eh_final:
                    automata_sharp.transitions.append(
                        Transitions(automata_sharp.start_states, simbolo, pop, automata_sharp.final_states[0], push))

                elif origem_eh_final and destino_interno:
                    automata_sharp.transitions.append(
                        Transitions(automata_sharp.final_states[0], simbolo, pop, destino + num-1, push))

                elif origem_eh_final and destino_eh_ini:
                    if simbolo == "&" and pop == "&" and push == "&":
                        pass
                    else:
                        automata_sharp.transitions.append(Transitions(automata_sharp.final_states[0], simbolo, pop, automata_sharp.start_states, push))

                elif origem_eh_final and destino_eh_final:
                    automata_sharp.transitions.append(Transitions(automata_sharp.final_states[0], simbolo, pop, automata_sharp.final_states[0], push))

                elif (not origem_eh_ini) and destino_eh_final:
                    automata_sharp.transitions.append(Transitions(origem + num-1, simbolo, pop, automata_sharp.final_states[0], push))

                    for item in automata_normal.alphabet:
                        if item not in automata_sharp.alphabet:
                            automata_sharp.alphabet.append(item)
                    
                    for item in automata_normal.stack_symbols:
                        if item not in automata_sharp.stack_symbols:
                            automata_sharp.stack_symbols.append(item)
                    
                    alphabet = automata_sharp.alphabet
                    states = automata_sharp.states
                    transitions = automata_sharp.transitions
                    start_states = automata_sharp.start_states
                    final_states = automata_sharp.final_states
                    stack_symbols = automata_sharp.stack_symbols

    return Automata(alphabet, states, transitions, start_states, final_states, stack_symbols, "sharp")

def two_points(automata1, automata2):
    alphabet=[]
    states=[0, ]
    transitions=[]
    start_states=0
    final_states=[]
    stack_symbols=[]

    aux_automatan = sharp(automata1, automata2, 1)

    num = len(states)
    for state in aux_automatan.states:
        states.append(state+num)
    
    penultimate_state = len(states)
    states.append(penultimate_state)

    ultimate_state = len(states)
    states.append(ultimate_state)
    final_states.append(ultimate_state)
    
    transitions.append(Transitions(penultimate_state,'&','Z',ultimate_state,'&'))
    transitions.append(Transitions(0,'&','&',aux_automatan.start_states+num,'Z'))

    for transition in aux_automatan.transitions:
        transitions.append(Transitions(transition.get_arg(1)+num, transition.get_arg(2), transition.get_arg(3), transition.get_arg(4)+num, transition.get_arg(5)))
    
    transitions.append(Transitions(aux_automatan.final_states[0]+num,'&','#',penultimate_state,'&'))

    alphabet = aux_automatan.alphabet
    stack_symbols = aux_automatan.stack_symbols

    return Automata(alphabet, states, transitions, start_states, final_states, stack_symbols)
