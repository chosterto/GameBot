from random import randrange, choice
from helpers.Cell import Cell

class Maze:
    def __init__(self):
        self.length = randrange(4, 7)
        self.wall = "🟩"
        self.empty = "⬛"
        self.flag = "🚩"
        self.grid = [[self.wall for _ in range(2 * self.length + 1)] for _ in range(2 * self.length + 1)]

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

        opposite_x, opposite_y = choice(corners)
        opposite_x += (1 if opposite_x > 1 else -1)
        self.grid[opposite_y][opposite_x] = self.wall
        self.end_x = opposite_x
        self.end_y = opposite_y

    
    def _place_flag(self, deadends):
        deadend_y, deadend_x = choice(deadends)
        self.grid[2 * deadend_y + 1][2 * deadend_x + 1] = self.flag
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
        self.grid[self.end_y][self.end_x] = self.empty
    

    def is_flag_reached(self):
        return self.x == self.flag_x and self.y == self.flag_y
    

    def is_end_reached(self):
        return self.x == self.end_x and self.y == self.end_y


    def display_hidden(self):
        shadow_grid = [[self.empty] * (2 * self.length + 1) for _ in range(2 * self.length + 1)]
        for i in range(-1, 2):
            for j in range(-1, 2):
                r = self.y + i
                c = self.x + j
                if c < 0 or c > 2 * self.length:
                    continue
                shadow_grid[r][c] = self.grid[r][c]

        return "".join(j for i in shadow_grid for j in i + ["\n"])
    

    def display_unhidden(self):
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

        elif emote == "⬅️" and board[r][c - 1] != self.wall:
            board[r][c], board[r][c - 1] = board[r][c - 1], board[r][c]
            self.x -= 1

        elif emote == "➡️" and board[r][c + 1] != self.wall:
            board[r][c], board[r][c + 1] = board[r][c + 1], board[r][c]
            self.x += 1
        
        if board[r][c] == self.flag:
            board[r][c] = self.empty
