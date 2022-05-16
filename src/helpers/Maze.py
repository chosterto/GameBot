from random import randrange, choice
from helpers.Cell import Cell

class Maze:
    def __init__(self):
        self.length = randrange(3, 7)
        self.wall = "🟩"
        self.empty = "⬛"
        self.grid = [[self.wall for _ in range(2 * self.length + 1)] for _ in range(2 * self.length + 1)]
        self.completed = False

        self.player = "😊"
        self.x = None
        self.y = None

        self.end_x = None
        self.end_y = None

        self.flag_x = None
        self.flag_y = None


    def initialize_pos(self):
        cap = 2 * self.length - 1
        corners = [
            (1, 1), # Upper left corner
            (1, cap), # Upper right corner  
            (cap, 1), # Lower left corner
            (cap, cap) # Lower right corner
            ]

        # In case the player spawns on top of the flag
        flag_pos = (self.flag_y, self.flag_x)
        if flag_pos in corners:
            corners.remove(flag_pos)
            
        corner_y, corner_x = choice(corners)
        self.grid[corner_y][corner_x] = self.player
        self.x = corner_x
        self.y = corner_y

        opposite_x = 0 if corner_x == cap else cap + 1
        opposite_y = 1 if corner_y == cap else cap
        self.grid[opposite_y][opposite_x] = "🟥"
        self.end_x = opposite_x
        self.end_y = opposite_y

    
    def _place_flag(self, deadends):
        deadend_y, deadend_x = choice(deadends)
        self.grid[2 * deadend_y + 1][2 * deadend_x + 1] = "🚩"
        self.flag_x = 2 * deadend_x + 1
        self.flag_y = 2 * deadend_y + 1

    
    def _neighbouring_cells(self, cells, y, x):
        neighbours = []

        if y > 0 and not cells[y - 1][x].visited:
            neighbours.append((cells[y - 1][x], "up"))

        if y < self.length - 1 and not cells[y + 1][x].visited:
            neighbours.append((cells[y + 1][x], "down"))

        if x > 0 and not cells[y][x - 1].visited:
            neighbours.append((cells[y][x - 1], "left"))

        if x < self.length - 1 and not cells[y][x + 1].visited:
            neighbours.append((cells[y][x + 1], "right"))
        
        return neighbours

    
    def generate_maze(self):
        cell_grid = [[Cell(r, c) for c in range(self.length)] for r in range(self.length)]

        deadends = []
        backtracking = False

        cell_grid[0][0].visited = True
        stack = []
        stack.append(cell_grid[0][0])

        # Recursive backtracking algorithm        
        while stack:
            current = stack.pop()
            adjacent = self._neighbouring_cells(cell_grid, current.y, current.x)
            if adjacent:
                if backtracking:
                    backtracking = False
                stack.append(current)
                chosen, wall = adjacent[randrange(0, len(adjacent))]
                current.walls[wall] = False
                chosen.visited = True
                stack.append(chosen)
            elif not backtracking:
                deadends.append((current.y, current.x))
                backtracking = True

        i = 0
        for r in range(1, 2 * self.length + 1, 2):
            for c in range(1, 2 * self.length + 1, 2):
                self.grid[r][c] = self.empty
                cell = cell_grid[i // self.length][i % self.length]
                for key, value in cell.walls.items():
                    if value:
                        continue
                    if key == "up":
                        self.grid[r - 1][c] = self.empty
                    elif key == "down":
                        self.grid[r + 1][c] = self.empty
                    elif key == "left":
                        self.grid[r][c - 1] = self.empty
                    else:
                        self.grid[r][c + 1] = self.empty
                i += 1
        
        self._place_flag(deadends)
    

    def remove_barrier(self):
        if self.completed:
            return
        self.grid[self.end_y][self.end_x] = self.empty
        for r in range(-1, 2):
            for c in range(-1, 2):
                if self.grid[self.y + r][self.x + c] == "🚩":
                    self.grid[self.y + r][self.x + c] = self.empty
        self.completed = True
    

    def is_flag_reached(self):
        return self.x == self.flag_x and self.y == self.flag_y
    

    def is_end_reached(self):
        return self.x == self.end_x and self.y == self.end_y


    def display(self):
        return "".join(j for i in self.grid for j in i + ["\n"])


    def move_player(self, emote):
        r = self.y
        c = self.x
        board = self.grid

        if emote == "⬆️" and board[r - 1][c] != self.wall:
            board[r][c], board[r - 1][c] = board[r - 1][c], board[r][c]
            self.y -= 1

        elif emote == "⬇️" and board[r + 1][c] != self.wall:
            board[r][c], board[r + 1][c] = board[r + 1][c], board[r][c]
            self.y += 1

        elif emote == "⬅️" and "🟥" != board[r][c - 1] != self.wall:
            board[r][c], board[r][c - 1] = board[r][c - 1], board[r][c]
            self.x -= 1

        elif emote == "➡️" and "🟥" != board[r][c + 1] != self.wall:
            board[r][c], board[r][c + 1] = board[r][c + 1], board[r][c]
            self.x += 1
