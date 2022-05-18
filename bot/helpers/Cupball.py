from random import sample

class Cup:
    def __init__(self, x, y, ball):
        self.x = x
        self.y = y
        self.ball = ball


class Cupball:
    ROWS = 5
    COLS = 15
    LEFT = 2
    MID = 7
    RIGHT = 12

    def __init__(self):
        self.bg = "⬛"
        self.green_ball = "🟢"
        self.red_ball = "🔴"
        self.cup = "🟨"
        self.is_hidden = False
        self.count = 5
        self.cup1 = None
        self.cup2 = None
        self.temp = None
        
        self.cups = [
            Cup(2, self.LEFT, self.red_ball),
            Cup(2, self.MID, self.green_ball),
            Cup(2, self.RIGHT, self.red_ball)
        ]
    

    def display(self):
        gameboard = [[self.bg] * self.COLS for _ in range(self.ROWS)]
        for cup in self.cups:
            obj = self.cup if self.is_hidden else cup.ball
            gameboard[cup.x][cup.y] = obj

        return "".join(j for i in gameboard for j in i + ['\n'])
    

    def hide_balls(self):
        self.is_hidden = True
    
    def reveal_balls(self):
        self.is_hidden = False

    def is_swapping_done(self):
        return self.count == 0


    def select_cups(self):
        self.cup1, self.cup2 = sample(range(3), 2)
        self.cups[self.cup1].x -= 1
        self.cups[self.cup2].x += 1
    

    def swap_cup1(self):
        self.temp = self.cups[self.cup1].y
        self.cups[self.cup1].y = self.cups[self.cup2].y
    

    def swap_cup2(self):
        self.cups[self.cup2].y = self.temp
    

    def place_cups(self):
        self.cups[self.cup1].x += 1
        self.cups[self.cup2].x -= 1
        self.count -= 1
    

    def has_green_ball(self, guess):
        pos = [self.LEFT, self.MID, self.RIGHT][guess - 1]
        for cup in self.cups:
            if pos == cup.y:
                selected_ball = cup.ball
        return selected_ball == self.green_ball