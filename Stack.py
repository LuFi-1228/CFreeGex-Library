class Stack:
    def __init__(self):
        self.string = ''
    
    def push(self, item):
        self.string += item
    
    def pop(self):
        item = self.string[len(self.string)-1]
        self.string = self.string[:-1]
        return item
    
    def top(self):
        return self.string[len(self.string)-1]
    
    def len(self):
        return len(self.string)