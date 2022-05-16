
class Cell:
    """
    Represents a cell in a maze generated grid. 
    """
    def __init__(self, y, x):
        # Indices
        self.y = y
        self.x = x
        
        #If the cell has been visited
        self.visited = False

        # Walls of cell
        self.walls = {
            "up": True, 
            "down": True, 
            "left": True, 
            "right": True
            }
        