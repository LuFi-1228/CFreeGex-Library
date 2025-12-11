class Transitions:   
    def __init__(self,a,b,c,d,e):
        self.initial_state_transition=a
        self.read_rule=b
        self.pop_rule=c
        self.final_transition_state=d
        self.push_rule=e
        
    def set_transition(self,a,b,c,d,e):
        self.initial_state_transition=a
        self.read_rule=b
        self.pop_rule=c
        self.final_transition_state=d
        self.push_rule=e
    
    def get_arg(self,i):
        if i==1:
            return self.initial_state_transition
        if i==2:
            return self.read_rule
        if i==3:
            return self.pop_rule
        if i==4:
            return self.final_transition_state
        if i==5:
            return self.push_rule
        return -1
