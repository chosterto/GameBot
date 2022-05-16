from random import shuffle

class RPS:
    def __init__(self):
        self.s = False
        self.p = False
        self.r = False
    
    def choose_shape(self, shape):
        if shape == "rock":
            self.r = True
        elif shape == "paper":
            self.p = True
        elif shape == "scissors":
            self.s = True

    def choose_random_shape(self):
        choices = [True, False, False]
        shuffle(choices)
        self.s, self.p, self.r = choices
    
    def shape(self):
        if self.r:
            return "Rock :rock:"
        if self.p:
            return "Paper :newspaper:"
        return "Scissors :scissors:"
    
    def is_same_as(self, other):
        return any([
            self.r == other.r == True, 
            self.p == other.p == True, 
            self.s == other.s == True
            ])

    def is_winner(self, other):
        if self.r:
            return other.s
        elif self.p:
            return other.r
        elif self.s:
            return other.p
