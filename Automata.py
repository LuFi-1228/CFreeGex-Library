from graphviz import Digraph
from assets import *

class Automata:
    def __init__(self,alphabet,states,transitions,start_states,final_states,stack_symbols,tag=None):
        self.alphabet=alphabet
        self.states=states
        self.transitions=transitions
        self.start_states=start_states
        self.final_states=final_states
        self.stack_symbols=stack_symbols
        self.tag = tag
        
    def print(self):
        print("Alphabet = { ",end="")
        for item in self.alphabet:
            print(item, end=" ")
        print("}\nStates = { ",end="")
        for item in self.states:
            print(item,end=" ")
        print("}\nTransitions = ")
        for item in self.transitions:
            print("\tf(",item.get_arg(1),",",item.get_arg(2),",",item.get_arg(3),")={",item.get_arg(4),",",item.get_arg(5),"}")   
        print("Start state= ",end="")
        print(self.start_states)
        print("Final states = { ",end="")
        for item in self.final_states:
            print(item,end=" ")
        print("}\n Stack_symbols = { ",end="")
        for item in self.stack_symbols:
            print(item,end=" ")
        print("}")

    def print_image(self, name='automata_output'):
        dot = Digraph("automata", format="png")
        dot.attr(rankdir="LR") 
        dot.attr("node", shape="circle")

        for state in self.states:
            if state in self.final_states:
                dot.node(str(state), shape="doublecircle")
            else:
                dot.node(str(state), shape="circle")

        for item in self.transitions:
            origin = str(item.get_arg(1))
            destiny = str(item.get_arg(4))
            label = make_label(item.get_arg(2), item.get_arg(3), item.get_arg(5))
            label = label.replace("&", "ε")

            dot.edge(origin, destiny, label=label)

        dot.node("start", shape="point")
        dot.edge("start", str(self.start_states))

        output = dot.render(f"static/{name}", cleanup=True)
        print(f"Image: {output}")

    def prepare_xml(self):
        string=""
        string=string+"<?xml version=\"1.0\" encoding=\"UTF-8\"?><structure type=\"editor_panel\">\n"
        string=string+"\t<structure type=\"transition_graph\">\n"
        string=string+"\t\t<structure mode=\"Default mode\" type=\"pda\">\n"
        string=string+"\t\t\t<structure type=\"state_set\">\n"
        for item in self.states:
            string=string+"\t\t\t\t<state>\n"
            string=string+"\t\t\t\t\t<name>q"+str(item)+"</name>\n"
            string=string+"\t\t\t\t\t<id>"+str(item)+"</id>\n"
            string=string+"\t\t\t\t</state>\n"
        string=string+"\t\t\t</structure>\n"
        string=string+"\t\t\t<structure type=\"BOS_symbol\">\n"
        string=string+"\t\t\t\t<value>Z</value>\n"
        string=string+"\t\t\t</structure>\n"
        string=string+"\t\t\t<structure type=\"transition_set\">\n"
        for item in self.transitions:
            string=string+"\t\t\t\t<transition>\n"
            if item.get_arg(3)!="&":
                string=string+"\t\t\t\t\t<pop>"+item.get_arg(3)+"</pop>\n"
            else:
                string=string+"\t\t\t\t\t<pop/>\n"      
            if item.get_arg(2)!="&":
                string=string+"\t\t\t\t\t<input>"+item.get_arg(2)+"</input>\n"
            else:
                string=string+"\t\t\t\t\t<input/>\n" 
            string=string+"\t\t\t\t\t<from>\n"
            string=string+"\t\t\t\t\t\t<name>q"+str(item.get_arg(1))+"</name>\n"
            string=string+"\t\t\t\t\t\t<id>"+str(item.get_arg(1))+"</id>\n"
            string=string+"\t\t\t\t\t</from>\n"
            string=string+"\t\t\t\t\t<to>\n"
            string=string+"\t\t\t\t\t\t<name>q"+str(item.get_arg(4))+"</name>\n"
            string=string+"\t\t\t\t\t\t<id>"+str(item.get_arg(4))+"</id>\n"
            string=string+"\t\t\t\t\t</to>\n"
            if item.get_arg(5)!="&":
                string=string+"\t\t\t\t\t<push>"+item.get_arg(5)+"</push>\n"
            else:
                string=string+"\t\t\t\t\t<push/>\n"  
            string=string+"\t\t\t\t</transition>\n"
        string=string+"\t\t\t</structure>\n"
        string=string+"\t\t\t<structure type=\"input_alph\">\n"
        for item in self.alphabet:
            if item!="&":
                string=string+"\t\t\t\t<symbol>"+item+"</symbol>\n"
        string=string+"\t\t\t</structure>\n"
        string=string+"\t\t\t<structure type=\"stack_alph\">\n"
        for item in self.stack_symbols:
            string=string+"\t\t\t\t<symbol>"+item+"</symbol>\n"
        string=string+"\t\t\t\t<symbol>Z</symbol>\n"
        string=string+"\t\t\t</structure>\n"
        string=string+"\t\t\t<structure type=\"start_state\">\n"
        string=string+"\t\t\t\t<state>\n"
        string=string+"\t\t\t\t\t<name>q"+str(self.start_states)+"</name>\n"
        string=string+"\t\t\t\t\t<id>"+str(self.start_states)+"</id>\n"
        string=string+"\t\t\t\t</state>\n"
        string=string+"\t\t\t</structure>\n"
        string=string+"\t\t\t<structure type=\"final_states\">\n"
        for item in self.final_states:
            string=string+"\t\t\t\t<state>\n"
            string=string+"\t\t\t\t\t<name>q"+str(item)+"</name>\n"
            string=string+"\t\t\t\t\t<id>"+str(item)+"</id>\n"
            string=string+"\t\t\t\t</state>\n"
        string=string+"\t\t\t</structure>\n"
        string=string+"\t\t</structure>\n"
        string=string+"\t\t<state_point_map>\n"
        for item in self.states:
            string=string+"\t\t\t<state_point>\n"
            string=string+"\t\t\t\t<state>"+str(item)+"</state>\n"
            string=string+"\t\t\t\t<point>\n"
            string=string+"\t\t\t\t\t<x>"+str(item*20+10)+"</x>\n"
            string=string+"\t\t\t\t\t<y>100.00</y>\n"
            string=string+"\t\t\t\t</point>\n"
            string=string+"\t\t\t</state_point>\n"        
        string=string+"\t\t</state_point_map>\n"
        string=string+"\t\t<control_point_map>\n"
        for item in self.transitions:
            string=string+"\t\t\t<control_point>\n"
            string=string+"\t\t\t\t<from>"+str(item.get_arg(1))+"</from>\n"
            string=string+"\t\t\t\t<to>"+str(item.get_arg(4))+"</to>\n"
            string=string+"\t\t\t\t<point>\n"
            string=string+"\t\t\t\t\t<x>"+str(((item.get_arg(1)*20+10)+(item.get_arg(4)*20+10))/2.0)+"</x>\n"
            string=string+"\t\t\t\t\t<y>100.0</y>\n"
            string=string+"\t\t\t\t</point>\n"
            string=string+"\t\t\t</control_point>\n"
        string=string+"\t\t</control_point_map>\n"
        string=string+"\t</structure>\n"
        string=string+"\t<state_label_map/>\n"
        string=string+"\t<note_map/>\n"
        string=string+"</structure>\n"
        return string
    
    def save_xml(self,path, verbose=False):
        output = self.prepare_xml()
        with open(path, 'w') as archive:
            archive.write(output)
        if verbose:
            print("<?xml version=\"1.0\" encoding=\"UTF-8\"?><structure type=\"editor_panel\">")
            print("\t<structure type=\"transition_graph\">")
            print("\t\t<structure mode=\"Default mode\" type=\"pda\">")
            print("\t\t\t<structure type=\"state_set\">")
            for item in self.states:
                print("\t\t\t\t<state>")
                print("\t\t\t\t\t<name>q%d</name>"%item)
                print("\t\t\t\t\t<id>%d</id>"%item)
                print("\t\t\t\t</state>")
            print("\t\t\t</structure>")
            print("\t\t\t<structure type=\"BOS_symbol\">")
            print("\t\t\t\t<value>Z</value>")
            print("\t\t\t</structure>")
            print("\t\t\t<structure type=\"transition_set\">")
            for item in self.transitions:
                print("\t\t\t\t<transition>")
                if(item.get_arg(3)!="&"):
                    print("\t\t\t\t\t<pop>%s</pop>"%item.get_arg(3))
                else:
                    print("\t\t\t\t\t<pop/>")      
                if(item.get_arg(2)!="&"):
                    print("\t\t\t\t\t<input>%s</input>"%item.get_arg(2))
                else:
                    print("\t\t\t\t\t<input/>") 
                print("\t\t\t\t\t<from>")
                print("\t\t\t\t\t\t<name>q%d</name>"%item.get_arg(1))
                print("\t\t\t\t\t\t<id>%d</id>"%item.get_arg(1))
                print("\t\t\t\t\t</from>")
                print("\t\t\t\t\t<to>")
                print("\t\t\t\t\t\t<name>q%d</name>"%item.get_arg(4))
                print("\t\t\t\t\t\t<id>%d</id>"%item.get_arg(4))
                print("\t\t\t\t\t</to>")
                if(item.get_arg(5)!="&"):
                    print("\t\t\t\t\t<push>%s</push>"%item.get_arg(5))
                else:
                    print("\t\t\t\t\t<push/>")  
                print("\t\t\t\t</transition>")
            print("\t\t\t</structure>")
            print("\t\t\t<structure type=\"input_alph\">")
            for item in self.alphabet:
                if item!="&":
                    print("\t\t\t\t<symbol>%s</symbol>"%item)
            print("\t\t\t</structure>")
            print("\t\t\t<structure type=\"stack_alph\">")
            for item in self.stack_symbols:
                print("\t\t\t\t<symbol>%s</symbol>"%item)
            print("\t\t\t\t<symbol>Z</symbol>")
            print("\t\t\t</structure>")
            print("\t\t\t<structure type=\"start_state\">")
            print("\t\t\t\t<state>")
            print("\t\t\t\t\t<name>q%d</name>"%self.start_states)
            print("\t\t\t\t\t<id>%d</id>"%self.start_states)
            print("\t\t\t\t</state>")
            print("\t\t\t</structure>")
            print("\t\t\t<structure type=\"final_states\">")
            for item in self.final_states:
                print("\t\t\t\t<state>")
                print("\t\t\t\t\t<name>q%d</name>"%item)
                print("\t\t\t\t\t<id>%d</id>"%item)
                print("\t\t\t\t</state>")
            print("\t\t\t</structure>")
            print("\t\t</structure>")
            print("\t\t<state_point_map>")
            for item in self.states:
                print("\t\t\t<state_point>")
                print("\t\t\t\t<state>%d</state>"%item)
                print("\t\t\t\t<point>")
                print("\t\t\t\t\t<x>%f</x>"%(item*20+10))
                print("\t\t\t\t\t<y>100.00</y>")
                print("\t\t\t\t</point>")
                print("\t\t\t</state_point>")        
            print("\t\t</state_point_map>")
            print("\t\t<control_point_map>")
            for item in self.transitions:
                print("\t\t\t<control_point>")
                print("\t\t\t\t<from>%d</from>"%item.get_arg(1))
                print("\t\t\t\t<to>%d</to>"%item.get_arg(4))
                print("\t\t\t\t<point>")
                print("\t\t\t\t\t<x>%f</x>"%(((item.get_arg(1)*20+10)+(item.get_arg(4)*20+10))/2.0))
                print("\t\t\t\t\t<y>100.0</y>")
                print("\t\t\t\t</point>")
                print("\t\t\t</control_point>")
            print("\t\t</control_point_map>")
            print("\t</structure>")
            print("\t<state_label_map/>")
            print("\t<note_map/>")
            print("</structure>")

    def execute(self, input_string, debug=False):
        table = []
        for t in self.transitions:
            table.append((
                t.get_arg(1), t.get_arg(2), t.get_arg(3), t.get_arg(4), t.get_arg(5)
            ))

        def is_pattern_with_hash(pop_rule):
            if not isinstance(pop_rule, str):
                return False
            if "#" not in pop_rule:
                return False
            parts = pop_rule.split("#")
            return all(p != "" for p in parts)

        def required_length_for_pop(pop_rule):
            if pop_rule == "&":
                return 0
            if is_pattern_with_hash(pop_rule):
                parts = pop_rule.split("#")
                return 2 * len(parts) - 1
            return 1

        def top_matches(pop_rule, stack):
            if pop_rule in [None, "&", ""]:
                return True, stack[:]

            pop_rule = str(pop_rule)

            if "#" in pop_rule:
                parts = pop_rule.split("#")

                if any(p == "" for p in parts):
                    if len(stack) == 0:
                        return False, stack
                    if stack[-1] == pop_rule:
                        return True, stack[:-1]
                    return False, stack

                seq = []
                for i, part in enumerate(parts):
                    seq.append(part)
                    if i < len(parts) - 1:
                        seq.append("#")

                L = len(seq)
                if len(stack) < L:
                    return False, stack

                if stack[-L:] == seq:
                    return True, stack[:-L]

                return False, stack

            if len(stack) == 0:
                return False, stack

            if stack[-1] == pop_rule:
                return True, stack[:-1]

            return False, stack

        configurations = [(self.start_states, 0, [])]
        history = {}
        step = 0

        while configurations:
            if debug:
                print(f"--- step {step} | configurations: {len(configurations)}")

            new_configs = []

            for state, pos, stack in configurations:
                history_key = (state, pos)
                history[history_key] = history.get(history_key, 0) + 1

                if history[history_key] >= 10000000:
                    if debug:
                        print(f"discarding looped config: {history_key}")
                    continue

                if pos == len(input_string) and state in self.final_states:
                    if debug:
                        print(f"ACCEPTED: final configuration reached {state}, {pos}, {stack}")
                    return True

                current_symbol = input_string[pos] if pos < len(input_string) else "&"

                outgoing = [tr for tr in table if tr[0] == state]

                consume = []
                for (q, read, pop_rule, q2, push) in outgoing:
                    if read == "&":
                        continue
                    if read != current_symbol:
                        continue

                    ok, stack_after_pop = top_matches(pop_rule, stack)
                    if not ok:
                        continue

                    consume.append((q, read, pop_rule, q2, push, stack_after_pop))

                consume.sort(key=lambda tr: required_length_for_pop(tr[2]), reverse=True)

                for (q, read, pop_rule, q2, push, stack_after_pop) in consume:
                    new_stack = stack_after_pop[:]
                    if push not in [None, "&", ""]:
                        new_stack.append(push)
                    new_pos = pos + 1

                    if debug:
                        print(f"apply: {q}->{q2} read='{read}' pop='{pop_rule}' push='{push}' | "
                            f"({state},{pos},{stack}) -> ({q2},{new_pos},{new_stack})")

                    new_configs.append((q2, new_pos, new_stack))

                eps_pop = []
                for (q, read, pop_rule, q2, push) in outgoing:
                    if read != "&":
                        continue
                    if pop_rule == "&":
                        continue

                    ok, stack_after_pop = top_matches(pop_rule, stack)
                    if not ok:
                        continue

                    eps_pop.append((q, read, pop_rule, q2, push, stack_after_pop))

                eps_pop.sort(key=lambda tr: required_length_for_pop(tr[2]), reverse=True)

                for (q, read, pop_rule, q2, push, stack_after_pop) in eps_pop:
                    new_stack = stack_after_pop[:]
                    if push not in [None, "&", ""]:
                        new_stack.append(push)
                    new_pos = pos

                    if debug:
                        print(f"apply: {q}->{q2} read='&' pop='{pop_rule}' push='{push}' | "
                            f"({state},{pos},{stack}) -> ({q2},{new_pos},{new_stack})")

                    new_configs.append((q2, new_pos, new_stack))

                for (q, read, pop_rule, q2, push) in outgoing:
                    if read != "&" or pop_rule != "&":
                        continue

                    new_stack = stack[:]
                    if push not in [None, "&", ""]:
                        new_stack.append(push)
                    new_pos = pos

                    if debug:
                        print(f"apply: {q}->{q2} read='&' pop='&' push='{push}' | "
                            f"({state},{pos},{stack}) -> ({q2},{new_pos},{new_stack})")

                    new_configs.append((q2, new_pos, new_stack))

            seen = set()
            dedup = []
            for (q, p, stk) in new_configs:
                key = (q, p, tuple(stk))
                if key not in seen:
                    seen.add(key)
                    dedup.append((q, p, stk))

            configurations = dedup
            step += 1

        if debug:
            print("REJECTED: no configuration reached a final state.")
        return False
