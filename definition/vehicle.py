from typing import List, Tuple

class Vehicle:
    BOARD_WIDTH = 6 # Fixed board width 
    BOARD_HEIGHT = 6 # Fixed board height
    
    def __init__(self, length, orientation, row, col):
        """
        Initializes a Vehicle instance.
        Attributes:
        - length: Length of the vehicle in grid cells.
        - orientation: Orientation of the vehicle ('H' for horizontal or 'V' for vertical).
        - row: Starting row position of the vehicle in the grid.
        - col: Starting column position of the vehicle in the grid.
        """

        # I check these based on the project requirements 
        if orientation not in ['H', 'V']:
            raise ValueError("Orientation must be 'H' or 'V'")
        if length not in [2, 3]:
            raise ValueError("Length must be 2 or 3")
        if row < 0 or row >= self.BOARD_HEIGHT or col < 0 or col >= self.BOARD_WIDTH:
            raise ValueError("Row and column must be within the grid")
        if orientation == 'H' and col - length + 1 < 0:
            raise ValueError("Horizontal vehicle cannot extend beyond the left edge of the board")
        if orientation == 'V' and row - length + 1 < 0:
            raise ValueError("Vertical vehicle cannot extend beyond the top edge of the board")

        self.length = length
        self.orientation = orientation
        self.row = row
        self.col = col
    
    def get_coordinates(self) -> List[Tuple[int, int]]:
        """
        Returns list of coordinates occupied by the vehicle in the grid.
        Each coordinate is a tuple (row, col).
        """
        if self.orientation == 'H':
            return [(self.row, self.col - i) for i in range(self.length)]
        else:
            return [(self.row - i, self.col) for i in range(self.length)]
